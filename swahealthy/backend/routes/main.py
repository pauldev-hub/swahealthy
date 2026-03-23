"""
Main routes — symptom checker, diagnosis, facilities, medicines, history.
"""

import json

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, g
from functools import wraps

from backend.models.helpers import get_db_connection, haversine, get_log_by_id, get_symptoms_by_ids, get_condition_by_name
from backend.services.engine import diagnose
from backend.services.photo_analyzer import analyze_photo

main_bp = Blueprint('main', __name__)


@main_bp.before_app_request
def set_lang():
    """Set global language from URL param or cookie."""
    lang = request.args.get('lang')
    if not lang:
        lang = request.cookies.get('swahealthy_lang')
    
    if lang not in ('en', 'bn', 'hi'):
        lang = 'en'
    
    g.lang = lang


def login_required(f):
    """Redirect to login page if user is not authenticated."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


@main_bp.route('/')
def index():
    lang = g.lang

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM symptoms ORDER BY body_area, name_en")
    symptoms = cursor.fetchall()
    conn.close()

    # Group symptoms by body_area
    grouped = {
        'head': [],
        'eyes': [],
        'ears': [],
        'chest': [],
        'stomach': [],
        'joints': [],
        'urinary': [],
        'women': [],
        'skin': [],
        'general': [],
        'mental': [],
    }

    for s in symptoms:
        area = s['body_area']
        if area in grouped:
            grouped[area].append({
                'symptom_id': s['symptom_id'],
                'display': (
                    f"{s['name_en']} / {s['name_bn']}" if lang == 'bn'
                    else (f"{s['name_en']} / {s['name_hi']}" if lang == 'hi' else s['name_en'])
                ),
                'name_en': s['name_en'],
            })

    return render_template('pages/index.html', symptoms_group=grouped, lang=lang)


@main_bp.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid payload format"}), 400

    history = data.get('history', [])

    from flask import current_app
    import os

    api_key = current_app.config.get('GROQ_API_KEY') or os.environ.get('GROQ_API_KEY')
    if not api_key:
        return jsonify({"error": "Server configuration error: GROQ_API_KEY is missing."}), 500

    try:
        from groq import Groq
        client = Groq(api_key=api_key)

        system_prompt = "You are SwaHealthy Assistant, a friendly rural health AI for West Bengal, India. Help users with health questions, medicine info, general wellness, and emotional support. Always reply in the user's language: 'en' = English, 'bn' = Bengali, 'hi' = Hindi. Keep responses concise (3-5 sentences max). Never diagnose — always recommend seeing a doctor for serious issues. Add a warm, caring tone. If the user seems sad or unwell emotionally, respond with empathy first."

        messages = [{"role": "system", "content": system_prompt}]
        if isinstance(history, list):
            messages.extend(history)

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=512,
        )

        reply = response.choices[0].message.content.strip()
        return jsonify({"reply": reply})

    except Exception as e:
        import traceback
        print(f"Error in chat route: {e}")
        return jsonify({"error": "Sorry, couldn't connect. Try again."}), 500


@main_bp.route('/diagnose', methods=['POST'])
def run_diagnosis():
    data = request.get_json()
    if not data or 'symptom_ids' not in data:
        return jsonify({"error": "Invalid payload format"}), 400

    symptom_ids = data['symptom_ids']
    language = data.get('language', 'en')
    duration = data.get('duration')
    age = data.get('age')
    gender = data.get('gender')

    result = diagnose(symptom_ids, language, duration=duration, age=age, gender=gender)

    # Attach recommended OTC medicines for this condition
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        name_col = f"name_{language}" if language in ('en', 'bn', 'hi') else 'name_en'
        cursor.execute(
            f"SELECT {name_col} as medicine_name, name_en FROM medicines WHERE condition_id = ? AND otc_available = 1",
            (result.get('condition_id'),),
        )
        meds = cursor.fetchall()
        recommended = []
        for row in meds:
            recommended.append(row['medicine_name'] if row['medicine_name'] else row['name_en'])
        result['recommended_medicines'] = recommended
        conn.close()
    except Exception:
        result['recommended_medicines'] = []

    # Save to session_log
    try:
        user_id = session['user']['user_id'] if 'user' in session else None
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO session_log (user_id, age, gender, symptoms_json, result_condition, severity, language)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, age, gender, json.dumps(symptom_ids), result['condition'], result['severity'], language))
        conn.commit()
        
        log_id = cursor.lastrowid
        result['log_id'] = log_id
        
        conn.close()
    except Exception as e:
        print(f"Error logging session: {e}")

    return jsonify(result)


@main_bp.route('/summary/<int:log_id>')
def summary(log_id):
    lang = request.args.get('lang', g.lang)
    log = get_log_by_id(log_id)
    if not log:
        return "Summary not found", 404
        
    symptom_ids = json.loads(log['symptoms_json']) if log['symptoms_json'] else []
    symptoms = get_symptoms_by_ids(symptom_ids, lang)
    condition = get_condition_by_name(log['result_condition'], lang)
    
    first_aid_steps = []
    if condition and condition.get('first_aid_text'):
        first_aid_steps = [step.strip() for step in condition['first_aid_text'].split('\n') if step.strip()]
        
    patient = None
    doctor = None
    medicines = []
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if log['user_id']:
        cursor.execute("SELECT name, age, gender FROM users WHERE user_id = ?", (log['user_id'],))
        p_row = cursor.fetchone()
        if p_row:
            patient = dict(p_row)
            if patient.get('name'):
                cursor.execute("""
                    SELECT d.name, d.specialisation 
                    FROM appointments a 
                    JOIN doctors d ON a.doctor_id = d.doctor_id 
                    WHERE a.patient_name = ? 
                    ORDER BY a.created_at DESC LIMIT 1
                """, (patient['name'],))
                d_row = cursor.fetchone()
                if d_row:
                    doctor = dict(d_row)
                    
    if condition and condition.get('condition_id'):
        name_col = f'name_{lang}' if lang in ('en', 'bn', 'hi') else 'name_en'
        cursor.execute(f"SELECT {name_col} as name FROM medicines WHERE condition_id = ? AND otc_available = 1", (condition['condition_id'],))
        m_rows = cursor.fetchall()
        medicines = [r['name'] for r in m_rows]
        
    conn.close()
        
    return render_template('pages/summary.html', 
                           log=log, 
                           symptoms=symptoms, 
                           condition=condition, 
                           first_aid_steps=first_aid_steps,
                           patient=patient,
                           doctor=doctor,
                           medicines=medicines,
                           lang=lang)


@main_bp.route('/analyze-photo', methods=['POST'])
def run_photo_analysis():
    data = request.get_json()
    if not data or 'image' not in data or 'media_type' not in data:
        return jsonify({"error": "Invalid payload format. Expected base64 image and media_type."}), 400
    
    # Optional size validation (rough check on base64 string length)
    # 2MB is roughly 2.8MB base64 encoded
    if len(data['image']) > 2.8 * 1024 * 1024:
        return jsonify({"error": "Image file too large. Max 2MB allowed."}), 400
        
    result = analyze_photo(data['image'], data['media_type'])
    return jsonify(result)


@main_bp.route('/facilities')
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

    results.sort(key=lambda x: x['distance'])
    return jsonify(results[:5])


@main_bp.route('/ai-analysis')
def ai_analysis():
    return render_template('pages/ai_analysis.html', lang=g.lang)


@main_bp.route('/history', methods=['GET', 'POST', 'DELETE'])
@login_required
def history():
    conn = get_db_connection()
    cursor = conn.cursor()
    user_id = session['user']['user_id']

    if request.method == 'GET':
        cursor.execute(
            "SELECT * FROM session_log WHERE user_id = ? ORDER BY session_date DESC LIMIT 10",
            (user_id,),
        )
        logs = cursor.fetchall()
        cursor.execute("SELECT symptom_id, name_en FROM symptoms")
        symptom_lookup = {str(row['symptom_id']): row['name_en'] for row in cursor.fetchall()}
        conn.close()

        resolved_logs = []
        for log in logs:
            row = dict(log)
            try:
                ids = json.loads(row.get('symptoms_json') or '[]')
                row['symptom_names'] = ', '.join(
                    symptom_lookup.get(str(i), str(i)) for i in ids
                ) or '—'
            except Exception:
                row['symptom_names'] = row.get('symptoms_json', '—')
            resolved_logs.append(row)

        return render_template('pages/history.html', logs=resolved_logs, lang=g.lang)

    if request.method == 'POST':
        data = request.get_json()
        cursor.execute("""
            INSERT INTO session_log (user_id, symptoms_json, result_condition, severity, language)
            VALUES (?, ?, ?, ?, ?)
        """, (
            user_id,
            data.get('symptoms_json', '[]'),
            data.get('result_condition', ''),
            data.get('severity', ''),
            data.get('language', 'en'),
        ))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"}), 201

    if request.method == 'DELETE':
        cursor.execute("DELETE FROM session_log WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
        return jsonify({"status": "cleared"}), 200


@main_bp.route('/results')
def results_page():
    return render_template('pages/results.html', lang=g.lang)


@main_bp.route('/profile')
def profile_page():
    user = session.get('user')
    check_count = 0
    age = None
    gender = None

    if user:
        user_id = user.get('user_id')
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get actual check count from DB
        cursor.execute("SELECT COUNT(*) FROM session_log WHERE user_id = ?", (user_id,))
        check_count = cursor.fetchone()[0]
        
        # Get age/gender from users table
        cursor.execute("SELECT age, gender FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            age = row['age']
            gender = row['gender']
        
        conn.close()

    return render_template('pages/profile.html', 
                           lang=g.lang, 
                           check_count=check_count, 
                           age=age, 
                           gender=gender)


@main_bp.route('/update-profile', methods=['POST'])
@login_required
def update_profile():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    age = data.get('age')
    gender = data.get('gender')
    user_id = session['user']['user_id']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users
        SET age = ?, gender = ?
        WHERE user_id = ?
    ''', (age, gender, user_id))
    conn.commit()
    conn.close()
    
    # Update session user object as well
    session['user']['age'] = age
    session['user']['gender'] = gender
    session.modified = True
    
    return jsonify({"status": "success"})


@main_bp.route('/duration')
def duration_page():
    return render_template('pages/duration.html', lang=g.lang)


@main_bp.route('/medicines')
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

    placeholders = ','.join('?' * len(med_ids))
    cursor.execute(f'''
        SELECT DISTINCT f.facility_id, f.name, f.type, f.district,
               f.latitude, f.longitude, f.contact
        FROM facilities f
        JOIN facility_medicines fm ON f.facility_id = fm.facility_id
        WHERE fm.medicine_id IN ({placeholders})
    ''', med_ids)
    fac_rows = cursor.fetchall()

    results = []
    for fac in fac_rows:
        dist = haversine(lat, lng, fac['latitude'], fac['longitude'])
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
            'medicines': stocked_meds,
        })

    results.sort(key=lambda x: x['distance'])
    conn.close()
    return jsonify(results[:10])


@main_bp.route('/admin')
@login_required
def admin():
    return "Admin page - WIP"

@main_bp.route('/wellness')
def wellness():
    lang = request.args.get('lang', session.get('lang', 'en'))
    return render_template('pages/wellness.html', lang=lang)

@main_bp.route('/wellness/chat', methods=['POST'])
def wellness_chat():
    import requests, os, json
    
    data = request.get_json()
    user_message = data.get('message', '').strip()
    language = data.get('language', 'en')
    history = data.get('history', [])  # list of {role, content}

    # --- CRISIS DETECTION ---
    crisis_keywords = [
        'suicide', 'kill myself', 'end my life', 'want to die', 'no reason to live', 'better off dead',
        'আত্মহত্যা', 'মরে যেতে চাই', 'বাঁচতে চাই না',
        'खुदकुशी', 'मरना चाहता', 'मरना चाहती', 'जीना नहीं'
    ]
    msg_lower = user_message.lower()
    if any(kw in msg_lower for kw in crisis_keywords):
        return jsonify({
            'reply': (
                "I'm really concerned about you right now. "
                "Please reach out immediately:\n\n"
                "📞 iCall: 9152987821 (free, Mon–Sat)\n"
                "📞 Vandrevala Foundation: 1860-2662-345 (24/7)\n\n"
                "You don't have to face this alone. Please call now 💙"
            ),
            'is_crisis': True
        })

    # --- DISTRESS DETECTION ---
    distress_words = [
        'hopeless', 'worthless', "can't go on", 'exhausted', 'numb',
        'crying', 'alone', 'nobody cares', 'hate myself',
        'হতাশ', 'একা', 'কাঁদছি',
        'निराश', 'अकेला', 'अकेली', 'रो रहा', 'रो रही'
    ]
    is_distressed = any(w in msg_lower for w in distress_words)

    system_prompt = f"""You are MindCare, a compassionate mental wellness support assistant 
built into SwaHealthy, a rural health app for users in West Bengal, India.

Rules you must always follow:
- You are NOT a therapist. Never diagnose. Never prescribe.
- Respond ONLY in the same language the user writes in (Bengali, Hindi, or English).
- Keep responses warm, non-clinical, and under 120 words.
- If the user seems emotionally distressed or very low, shift your response to include:
  one immediate coping tip + a gentle mention of iCall (9152987821).
- You may discuss: anxiety, depression, stress, sleep, relationships, loneliness,
  motivation, self-care, breathing techniques, and general mental wellbeing.
- If asked something unrelated to mental health, gently redirect back.
- Never use jargon. Write as a caring friend who happens to know about mental health.
{"- The user seems distressed. Prioritise warmth and one actionable tip first." if is_distressed else ""}
"""

    messages = [{"role": "system", "content": system_prompt}]
    for h in history[-6:]:
        messages.append({"role": h.get('role', 'user'), "content": h.get('content', '')})
    
    # Only append user_message if history doesn't already end with it (frontend might have pushed it)
    if not history or history[-1].get('content') != user_message:
        messages.append({"role": "user", "content": user_message})

    try:
        from flask import current_app
        api_key = current_app.config.get('GROQ_API_KEY') or os.environ.get('GROQ_API_KEY')
        resp = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama3-70b-8192",
                "messages": messages,
                "max_tokens": 200,
                "temperature": 0.7
            },
            timeout=15
        )
        reply = resp.json()['choices'][0]['message']['content'].strip()
    except Exception as e:
        import traceback
        traceback.print_exc()
        reply = "I'm having trouble connecting right now. If you need immediate support, please call iCall: 9152987821 💙"

    return jsonify({'reply': reply, 'is_crisis': False})

@main_bp.route('/wellness/reflection', methods=['POST'])
def wellness_reflection():
    import requests, os
    from flask import current_app
    
    data = request.get_json()
    mood = data.get('mood', 'okay')
    language = data.get('language', 'en')

    prompt = f"The user is feeling '{mood}' today. Write a single, short, compassionate sentence (max 15 words) reflecting on this feeling as a journal entry prompt or thought. Respond entirely in {language}. Do not use quotes."

    try:
        api_key = current_app.config.get('GROQ_API_KEY') or os.environ.get('GROQ_API_KEY')
        resp = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={"model": "llama3-70b-8192", "messages": [{"role": "user", "content": prompt}], "max_tokens": 50, "temperature": 0.7},
            timeout=10
        )
        content = resp.json()['choices'][0]['message']['content'].strip()
        return jsonify({'reflection': content})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'reflection': "Taking it one day at a time. 💙"})

@main_bp.route('/wellness/analyse', methods=['POST'])
def wellness_analyse():
    import requests, os
    from flask import current_app
    
    data = request.get_json()
    assessment = data.get('assessment')   # 'PHQ-9' or 'GAD-7'
    score = data.get('score')
    severity = data.get('severity')
    language = data.get('language', 'en')
    answers = data.get('answers', [])

    if severity == 'severe':
        return jsonify({'analysis': None, 'actions': [], 'is_severe': True})

    qa_text = "\\n".join([f"Q: {a['question']}\\nA: {a['answer']} ({a['points']} pts)" for a in answers])

    prompt = f"""Assessment: {assessment}
Score: {score}
Severity: {severity.title()}
Language to respond in: {language}

User's responses:
{qa_text}

Write a warm, non-clinical, personalised 3-4 sentence analysis based on these specific 
answers — not just the score. Reference specific patterns you notice in the answers.
Do not diagnose. Do not use clinical jargon.
Then on a new line write exactly "ACTIONS:" followed by exactly 3 specific actionable 
steps as a numbered list. Steps should be tailored to the answers, not generic.
Respond entirely in {language}."""

    try:
        api_key = current_app.config.get('GROQ_API_KEY') or os.environ.get('GROQ_API_KEY')
        resp = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={"model": "llama3-70b-8192", "messages": [{"role": "user", "content": prompt}], "max_tokens": 350, "temperature": 0.6},
            timeout=20
        )
        content = resp.json()['choices'][0]['message']['content'].strip()
        parts = content.split('ACTIONS:')
        analysis = parts[0].strip()
        actions = []
        if len(parts) > 1:
            for line in parts[1].strip().split('\\n'):
                line = line.strip().lstrip('123456789.-) ')
                if line:
                    actions.append(line)
    except Exception as e:
        analysis = "Your responses have been noted. Please consider speaking with a mental health professional for a thorough evaluation."
        actions = ["Try to maintain a daily routine, even small habits help.", "Reach out to someone you trust today.", "Consider calling iCall (9152987821) for a free counselling session."]

    return jsonify({'analysis': analysis, 'actions': actions[:3], 'is_severe': False})
