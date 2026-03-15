import json
from flask import Flask, render_template, request, jsonify
from db import init_db, get_db_connection, haversine
from engine import diagnose

app = Flask(__name__)

# Initialize database
with app.app_context():
    init_db()

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
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO session_log (symptoms_json, result_condition, severity, language)
            VALUES (?, ?, ?, ?)
        """, (json.dumps(symptom_ids), result['condition'], result['severity'], language))
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
def history():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'GET':
        cursor.execute("SELECT * FROM session_log ORDER BY session_date DESC LIMIT 10")
        logs = cursor.fetchall()
        conn.close()
        return render_template('history.html', logs=logs)
        
    if request.method == 'POST':
        data = request.get_json()
        cursor.execute("""
            INSERT INTO session_log (symptoms_json, result_condition, severity, language)
            VALUES (?, ?, ?, ?)
        """, (data.get('symptoms_json', '[]'), data.get('result_condition', ''), data.get('severity', ''), data.get('language', 'en')))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"}), 201

    if request.method == 'DELETE':
        cursor.execute("DELETE FROM session_log")
        conn.commit()
        conn.close()
        return jsonify({"status": "cleared"}), 200

@app.route('/results')
def results_page():
    return render_template('results.html')

if __name__ == '__main__':
    app.run(debug=True)
