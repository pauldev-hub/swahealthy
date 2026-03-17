import os
import json
from functools import wraps
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from db import init_db, get_db_connection, haversine, upsert_user
from engine import diagnose

load_dotenv()

# --- Debug: verify .env is loading ---
_client_id = os.environ.get('GOOGLE_CLIENT_ID', '')
_client_secret = os.environ.get('GOOGLE_CLIENT_SECRET', '')
print(f"[DEBUG] GOOGLE_CLIENT_ID loaded: '{_client_id[:30]}...' (ends with .apps.googleusercontent.com: {_client_id.endswith('.apps.googleusercontent.com')})")
print(f"[DEBUG] GOOGLE_CLIENT_SECRET loaded: '{_client_secret[:10]}...' (present: {bool(_client_secret)})")

# Force OAUTHLIB to allow HTTP on localhost (must be set before oauth is used)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = os.environ.get('OAUTHLIB_INSECURE_TRANSPORT', '0')

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-CHANGE-THIS')

# Register custom Jinja filters
@app.template_filter('from_json')
def from_json_filter(s):
    return json.loads(s)

# Authlib reads client_id/secret from app.config with naming convention:
# GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET
app.config['GOOGLE_CLIENT_ID'] = _client_id
app.config['GOOGLE_CLIENT_SECRET'] = _client_secret

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=_client_id,
    client_secret=_client_secret,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

# Initialize database
with app.app_context():
    init_db()

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/google-login')
def google_login():
    # Explicitly use localhost to match what is registered in Google Cloud Console.
    # Flask may infer 127.0.0.1 which Google treats as a different origin.
    redirect_uri = url_for('callback', _external=True).replace('127.0.0.1', 'localhost')
    return google.authorize_redirect(redirect_uri)

@app.route('/callback')
def callback():
    token = google.authorize_access_token()
    user_info = token.get('userinfo')
    if user_info:
        user = upsert_user(user_info)
        session['user'] = user
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/debug-oauth')
def debug_oauth():
    """Debug route - shows first 20 chars of credentials. Remove before deploying."""
    cid = os.environ.get('GOOGLE_CLIENT_ID', 'NOT SET')
    csecret = os.environ.get('GOOGLE_CLIENT_SECRET', 'NOT SET')
    redirect_uri = url_for('callback', _external=True).replace('127.0.0.1', 'localhost')
    return f"""
    <pre>
    GOOGLE_CLIENT_ID (first 20):   '{cid[:20]}...'
    Ends with correct suffix:       {cid.endswith('.apps.googleusercontent.com')}
    GOOGLE_CLIENT_SECRET present:   {bool(csecret and csecret != 'NOT SET')}
    OAUTHLIB_INSECURE_TRANSPORT:    {os.environ.get('OAUTHLIB_INSECURE_TRANSPORT', 'not set')}
    Redirect URI Flask will use:    {redirect_uri}

    Checklist:
    [ ] Client ID ends with .apps.googleusercontent.com  --> {cid.endswith('.apps.googleusercontent.com')}
    [ ] Client Secret is present                         --> {bool(csecret)}
    [ ] OAUTHLIB_INSECURE_TRANSPORT=1 for localhost      --> {os.environ.get('OAUTHLIB_INSECURE_TRANSPORT') == '1'}
    [ ] Redirect URI matches Google Console              --> {redirect_uri}
         (Must add exactly this to Google Console!)
    </pre>
    """

@app.route('/')
def index():
    lang = request.args.get('lang', 'en')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM symptoms ORDER BY body_area, name_en")
    symptoms = cursor.fetchall()
    conn.close()
    
    # Group symptoms by body_area
    grouped = {
        'head': [],
        'chest': [],
        'stomach': [],
        'general': [],
        'skin': []
    }
    
    for s in symptoms:
        area = s['body_area']
        name_col = f"name_{lang}"
        # fallback to english if translation missing somehow
        display_name = s[name_col] if name_col in s.keys() else s['name_en']
        
        # for frontend to display "English / Bangla" simultaneously if needed,
        # but the prompt states specific names should be used.
        if area in grouped:
            grouped[area].append({
                'symptom_id': s['symptom_id'],
                'display': f"{s['name_en']} / {s['name_bn']}" if lang == 'bn' else (f"{s['name_en']} / {s['name_hi']}" if lang == 'hi' else s['name_en']),
                'name_en': s['name_en']
            })
            
    return render_template('index.html', symptoms_group=grouped, lang=lang)

@app.route('/diagnose', methods=['POST'])
def run_diagnosis():
    data = request.get_json()
    if not data or 'symptom_ids' not in data:
        return jsonify({"error": "Invalid payload format"}), 400
        
    symptom_ids = data['symptom_ids']
    language = data.get('language', 'en')
    
    result = diagnose(symptom_ids, language)
    
    # Save to session_log
    try:
        user_id = session['user']['user_id'] if 'user' in session else None
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO session_log (user_id, symptoms_json, result_condition, severity, language)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, json.dumps(symptom_ids), result['condition'], result['severity'], language))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error logging session: {e}")
        
    return jsonify(result)

@app.route('/facilities')
def facilities():
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    
    if lat is None or lng is None:
        return jsonify({"error": "Missing lat/lng parameters"}), 400
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM facilities")
    facs = cursor.fetchall()
    conn.close()
    
    results = []
    for f in facs:
        dist = haversine(lat, lng, f['latitude'], f['longitude'])
        f_dict = dict(f)
        f_dict['distance'] = round(dist, 2)
        results.append(f_dict)
        
    # Sort by distance
    results.sort(key=lambda x: x['distance'])
    return jsonify(results[:5]) # Return 5 nearest

@app.route('/history', methods=['GET', 'POST', 'DELETE'])
@login_required
def history():
    conn = get_db_connection()
    cursor = conn.cursor()
    user_id = session['user']['user_id']
    
    if request.method == 'GET':
        cursor.execute("SELECT * FROM session_log WHERE user_id = ? ORDER BY session_date DESC LIMIT 10", (user_id,))
        logs = cursor.fetchall()
        # Build a symptom lookup {id: name_en} and resolve each log's symptoms
        cursor.execute("SELECT symptom_id, name_en FROM symptoms")
        symptom_lookup = {str(row['symptom_id']): row['name_en'] for row in cursor.fetchall()}
        conn.close()

        # Pre-resolve symptom names for each log (done in Python, not Jinja2)
        import json as _json
        resolved_logs = []
        for log in logs:
            row = dict(log)
            try:
                ids = _json.loads(row.get('symptoms_json') or '[]')
                row['symptom_names'] = ', '.join(
                    symptom_lookup.get(str(i), str(i)) for i in ids
                ) or '—'
            except Exception:
                row['symptom_names'] = row.get('symptoms_json', '—')
            resolved_logs.append(row)

        return render_template('history.html', logs=resolved_logs)
        
    if request.method == 'POST':
        data = request.get_json()
        cursor.execute("""
            INSERT INTO session_log (user_id, symptoms_json, result_condition, severity, language)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, data.get('symptoms_json', '[]'), data.get('result_condition', ''), data.get('severity', ''), data.get('language', 'en')))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"}), 201

    if request.method == 'DELETE':
        cursor.execute("DELETE FROM session_log WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
        return jsonify({"status": "cleared"}), 200

@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    """Handle appointment listing and booking."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'GET':
        cursor.execute("SELECT * FROM doctors")
        doctors = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return render_template('appointments.html', doctors=doctors)
        
    if request.method == 'POST':
        data = request.get_json()
        required = ['doctor_id', 'patient_name', 'patient_phone', 'date', 'time']
        if not all(k in data for k in required):
            return jsonify({'error': 'Missing required fields'}), 400
            
        cursor.execute('''
            INSERT INTO appointments (doctor_id, patient_name, patient_phone, appointment_date, appointment_time, reason, language)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (data['doctor_id'], data['patient_name'], data['patient_phone'], data['date'], data['time'], data.get('reason', ''), data.get('language', 'en')))
        
        appointment_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return jsonify({'appointment_id': appointment_id, 'status': 'pending'})

@app.route('/appointments/slots')
def get_slots():
    """Get available slots for a doctor on a specific date."""
    doctor_id = request.args.get('doctor_id')
    date = request.args.get('date')
    if not doctor_id or not date:
        return jsonify({'error': 'Missing parameters'}), 400
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get doctor's standard slots
    cursor.execute("SELECT slots_json FROM doctors WHERE doctor_id = ?", (doctor_id,))
    doctor = cursor.fetchone()
    if not doctor:
        return jsonify({'error': 'Doctor not found'}), 404
        
    import json as _json_slots
    all_slots = _json_slots.loads(doctor['slots_json'])
    
    # Get booked slots for this date (excluding cancelled)
    cursor.execute('''
        SELECT appointment_time FROM appointments 
        WHERE doctor_id = ? AND appointment_date = ? AND status != 'cancelled'
    ''', (doctor_id, date))
    booked_slots = [row['appointment_time'] for row in cursor.fetchall()]
    
    # Filter available
    available_slots = [s for s in all_slots if s not in booked_slots]
    conn.close()
    return jsonify({'slots': available_slots})

@app.route('/appointments/my')
def my_appointments():
    """Fetch all appointments, optionally filtered by phone number."""
    phone = request.args.get('phone')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if phone:
        cursor.execute('''
            SELECT a.*, d.name as doctor_name, d.specialisation 
            FROM appointments a
            JOIN doctors d ON a.doctor_id = d.doctor_id
            WHERE a.patient_phone = ?
            ORDER BY a.appointment_date DESC, a.appointment_time DESC
        ''', (phone,))
    else:
        cursor.execute('''
            SELECT a.*, d.name as doctor_name, d.specialisation 
            FROM appointments a
            JOIN doctors d ON a.doctor_id = d.doctor_id
            ORDER BY a.appointment_date DESC, a.appointment_time DESC
        ''')
    
    apps = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(apps)

@app.route('/appointments/<int:app_id>', methods=['DELETE'])
def cancel_appointment(app_id):
    """Cancel an appointment."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE appointments SET status = 'cancelled' WHERE appointment_id = ?", (app_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/admin')
@login_required
def admin():
    return "Admin page - WIP"

@app.route('/results')
def results_page():
    return render_template('results.html')

@app.route('/medicines')
def nearby_medicines():
    """Return nearby Jan Aushadhi facilities stocking OTC medicines for a condition."""
    condition_id = request.args.get('condition_id', type=int)
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    lang = request.args.get('lang', 'en')

    if condition_id is None or lat is None or lng is None:
        return jsonify({'error': 'Missing condition_id, lat, or lng parameters'}), 400

    name_col = f'name_{lang}' if lang in ('en', 'bn', 'hi') else 'name_en'

    conn = get_db_connection()
    cursor = conn.cursor()

    # Get OTC medicines for this condition
    cursor.execute(f'''
        SELECT m.medicine_id, m.{name_col} as medicine_name, m.name_en as medicine_name_en
        FROM medicines m
        WHERE m.condition_id = ? AND m.otc_available = 1
    ''', (condition_id,))
    medicines = cursor.fetchall()

    if not medicines:
        conn.close()
        return jsonify([])

    med_ids = [m['medicine_id'] for m in medicines]
    med_names = {m['medicine_id']: m['medicine_name'] for m in medicines}

    # Get facilities stocking any of these medicines
    placeholders = ','.join('?' * len(med_ids))
    cursor.execute(f'''
        SELECT DISTINCT f.facility_id, f.name, f.type, f.district,
               f.latitude, f.longitude, f.contact
        FROM facilities f
        JOIN facility_medicines fm ON f.facility_id = fm.facility_id
        WHERE fm.medicine_id IN ({placeholders})
    ''', med_ids)
    facilities = cursor.fetchall()

    # For each facility, get which of the relevant medicines they stock
    results = []
    for fac in facilities:
        dist = haversine(lat, lng, fac['latitude'], fac['longitude'])
        # Get medicine names stocked by this facility
        cursor.execute(f'''
            SELECT fm.medicine_id FROM facility_medicines fm
            WHERE fm.facility_id = ? AND fm.medicine_id IN ({placeholders})
        ''', [fac['facility_id']] + med_ids)
        stocked_meds = [med_names[row['medicine_id']] for row in cursor.fetchall()]

        results.append({
            'facility_id': fac['facility_id'],
            'name': fac['name'],
            'type': fac['type'],
            'district': fac['district'],
            'distance': round(dist, 2),
            'contact': fac['contact'],
            'medicines': stocked_meds
        })

    results.sort(key=lambda x: x['distance'])
    conn.close()
    return jsonify(results[:10])

if __name__ == '__main__':
    app.run(host='localhost', debug=True)
