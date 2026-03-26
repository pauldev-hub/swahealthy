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

CURATED_HOSPITALS = [
    {
        "name": "Medical College Hospital",
        "type": "Hospital",
        "district": "Kolkata",
        "latitude": 22.5735,
        "longitude": 88.3629,
        "contact": "+91 33 2212 3000",
        "ownership": "Government",
    },
    {
        "name": "NRS Medical College and Hospital",
        "type": "Hospital",
        "district": "Kolkata",
        "latitude": 22.5645,
        "longitude": 88.3683,
        "contact": "+91 33 2286 0033",
        "ownership": "Government",
    },
    {
        "name": "SSKM Hospital",
        "type": "Hospital",
        "district": "Kolkata",
        "latitude": 22.5395,
        "longitude": 88.3444,
        "contact": "+91 33 2204 1100",
        "ownership": "Government",
    },
    {
        "name": "Howrah District Hospital",
        "type": "Hospital",
        "district": "Howrah",
        "latitude": 22.58,
        "longitude": 88.3299,
        "contact": "+91 33 2641 3400",
        "ownership": "Government",
    },
    {
        "name": "Bidhannagar State General Hospital",
        "type": "Healthcare Facility",
        "district": "North 24 Parganas",
        "latitude": 22.5937,
        "longitude": 88.4206,
        "contact": "N/A",
        "ownership": "Government",
    },
    {
        "name": "Salt Lake Sub Divisional Hospital",
        "type": "Hospital",
        "district": "North 24 Parganas",
        "latitude": 22.5866,
        "longitude": 88.4116,
        "contact": "+91 33 2321 2323",
        "ownership": "Government",
    },
    {
        "name": "Barasat District Hospital",
        "type": "Hospital",
        "district": "North 24 Parganas",
        "latitude": 22.7214,
        "longitude": 88.4735,
        "contact": "+91 33 2552 2011",
        "ownership": "Government",
    },
    {
        "name": "Dum Dum Municipal Specialised Hospital",
        "type": "Healthcare Facility",
        "district": "North 24 Parganas",
        "latitude": 22.6241,
        "longitude": 88.4187,
        "contact": "+91 33 2551 3241",
        "ownership": "Government",
    },
    {
        "name": "Apollo Multispeciality Hospitals",
        "type": "Hospital",
        "district": "Kolkata",
        "latitude": 22.5122,
        "longitude": 88.3927,
        "contact": "+91 33 2320 3040",
        "ownership": "Private",
    },
    {
        "name": "Fortis Hospital Anandapur",
        "type": "Hospital",
        "district": "Kolkata",
        "latitude": 22.5018,
        "longitude": 88.4011,
        "contact": "+91 33 6628 4444",
        "ownership": "Private",
    },
    {
        "name": "Peerless Hospital",
        "type": "Hospital",
        "district": "Kolkata",
        "latitude": 22.4965,
        "longitude": 88.3923,
        "contact": "+91 33 2462 0071",
        "ownership": "Private",
    },
    {
        "name": "AMRI Hospital Dhakuria",
        "type": "Hospital",
        "district": "Kolkata",
        "latitude": 22.5132,
        "longitude": 88.3668,
        "contact": "+91 33 6626 0000",
        "ownership": "Private",
    },
]

MEDICINE_NAME_MAP = {
    'Paracetamol': {'bn': 'প্যারাসিটামল', 'hi': 'पैरासिटामोल'},
    'Paracetamol 500mg': {'bn': 'প্যারাসিটামল ৫০০ মি.গ্রা.', 'hi': 'पैरासिटामोल 500 मि.ग्रा.'},
    'Cetirizine': {'bn': 'সিটিরিজিন', 'hi': 'सेटिरिज़िन'},
    'Cetirizine 10mg': {'bn': 'সিটিরিজিন ১০ মি.গ্রা.', 'hi': 'सेटिरिज़िन 10 मि.ग्रा.'},
    'Guaifenesin Syrup': {'bn': 'গুয়াইফেনেসিন সিরাপ', 'hi': 'गुआइफेनेसिन सिरप'},
    'Vitamin C 500mg': {'bn': 'ভিটামিন সি ৫০০ মি.গ্রা.', 'hi': 'विटामिन C 500 मि.ग्रा.'},
    'ORS (Oral Rehydration Salts)': {'bn': 'ওআরএস', 'hi': 'ओआरएस'},
    'ORS Sachets': {'bn': 'ওআরএস স্যাশে', 'hi': 'ओआरएस सैशे'},
    'Activated Charcoal': {'bn': 'অ্যাক্টিভেটেড চারকোল', 'hi': 'एक्टिवेटेड चारकोल'},
    'Domperidone': {'bn': 'ডমপেরিডন', 'hi': 'डोम्पेरिडोन'},
    'Domperidone 10mg': {'bn': 'ডমপেরিডন ১০ মি.গ্রা.', 'hi': 'डोम्पेरिडोन 10 मि.ग्रा.'},
    'Electrolyte Powder': {'bn': 'ইলেক্ট্রোলাইট পাউডার', 'hi': 'इलेक्ट्रोलाइट पाउडर'},
    'Antacid (Gelusil)': {'bn': 'অ্যান্টাসিড (জেলুসিল)', 'hi': 'एंटासिड (जेलुसिल)'},
    'Loperamide': {'bn': 'লোপেরামাইড', 'hi': 'लोपरामाइड'},
    'Loperamide 2mg': {'bn': 'লোপেরামাইড ২ মি.গ্রা.', 'hi': 'लोपरामाइड 2 मि.ग्रा.'},
    'Zinc Sulfate': {'bn': 'জিঙ্ক সালফেট', 'hi': 'जिंक सल्फेट'},
    'Zinc Sulfate 20mg': {'bn': 'জিঙ্ক সালফেট ২০ মি.গ্রা.', 'hi': 'जिंक सल्फेट 20 मि.ग्रा.'},
    'Ibuprofen': {'bn': 'আইবুপ্রোফেন', 'hi': 'इबुप्रोफेन'},
    'Ibuprofen 400mg': {'bn': 'আইবুপ্রোফেন ৪০০ মি.গ্রা.', 'hi': 'इबुप्रोफेन 400 मि.ग्रा.'},
    'Potassium Citrate': {'bn': 'পটাশিয়াম সাইট্রেট', 'hi': 'पोटैशियम साइट्रेट'},
    'Potassium Citrate Sachets': {'bn': 'পটাশিয়াম সাইট্রেট স্যাশে', 'hi': 'पोटैशियम साइट्रेट सैशे'},
    'Cranberry Extract Tablet': {'bn': 'ক্র্যানবেরি এক্সট্র্যাক্ট ট্যাবলেট', 'hi': 'क्रैनबेरी एक्सट्रैक्ट टैबलेट'},
    'Clotrimazole Cream': {'bn': 'ক্লোট্রিমাজল ক্রিম', 'hi': 'क्लोट्रिमाज़ोल क्रीम'},
    'Calamine Lotion': {'bn': 'ক্যালামাইন লোশন', 'hi': 'कैलामाइन लोशन'},
    'Hydrocortisone Cream': {'bn': 'হাইড্রোকর্টিসন ক্রিম', 'hi': 'हाइड्रोकार्टिसोन क्रीम'},
    'Hydrocortisone 1% Cream': {'bn': 'হাইড্রোকর্টিসন ১% ক্রিম', 'hi': 'हाइड्रोकार्टिसोन 1% क्रीम'},
    'Betadine Ointment': {'bn': 'বেটাডিন মলম', 'hi': 'बेटाडीन मलहम'},
    'Povidone Iodine Gargle': {'bn': 'পোভিডোন আয়োডিন গার্গল', 'hi': 'पोविडोन आयोडीन गरारे'},
    'Strepsils': {'bn': 'স্ট্রেপসিলস', 'hi': 'स्ट्रेप्सिल्स'},
    'Salbutamol Inhaler': {'bn': 'সালবিউটামল ইনহেলার', 'hi': 'सालब्यूटामोल इनहेलर'},
    'Sodium Chloride Eye Drops': {'bn': 'সোডিয়াম ক্লোরাইড আই ড্রপ', 'hi': 'सोडियम क्लोराइड आई ड्रॉप्स'},
    'Chloramphenicol Eye Drops': {'bn': 'ক্লোরামফেনিকল আই ড্রপ', 'hi': 'क्लोरैम्फेनिकोल आई ड्रॉप्स'},
    'Otocain Ear Drops': {'bn': 'অটোকেইন ইয়ার ড্রপ', 'hi': 'ओटोकैन ईयर ड्रॉप्स'},
    'Iron + Folic Acid Tablets': {'bn': 'আয়রন + ফলিক অ্যাসিড ট্যাবলেট', 'hi': 'आयरन + फोलिक एसिड टैबलेट'},
}


def decode_mojibake_text(value):
    if not isinstance(value, str) or not value:
        return value
    if not any(marker in value for marker in ('Ã', 'Â', 'â', 'à¦', 'à¤', 'ðŸ')):
        return value

    current = value
    for _ in range(3):
        try:
            decoded = current.encode('latin1').decode('utf-8')
        except (UnicodeEncodeError, UnicodeDecodeError):
            break
        if decoded == current:
            break
        current = decoded
    return current


def normalize_i18n_key(value):
    if not isinstance(value, str):
        return ''
    return decode_mojibake_text(value).strip().lower()


def localize_medicine_name(name_en, lang, fallback=None):
    if lang not in ('bn', 'hi'):
        return decode_mojibake_text(fallback or name_en)
    localized = MEDICINE_NAME_MAP.get(name_en, {}).get(lang)
    return decode_mojibake_text(localized or fallback or name_en)


def with_distance(rows, lat, lng):
    results = []
    for row in rows:
        item = dict(row)
        item["distance"] = round(haversine(lat, lng, item["latitude"], item["longitude"]), 2)
        results.append(item)
    results.sort(key=lambda x: x["distance"])
    return results


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
    user = session.get('user') or {}
    raw_name = (user.get('name') or '').strip()
    first_name = raw_name.split()[0] if raw_name else None

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
            if lang == 'bn':
                symptom_display = s['name_bn']
            elif lang == 'hi':
                symptom_display = s['name_hi']
            else:
                symptom_display = s['name_en']

            grouped[area].append({
                'symptom_id': s['symptom_id'],
                'display': symptom_display,
                'name_en': s['name_en'],
                'name_bn': s['name_bn'],
                'name_hi': s['name_hi'],
            })

    return render_template('pages/index.html', symptoms_group=grouped, lang=lang, first_name=first_name)


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
    try:
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
                recommended.append(localize_medicine_name(row['name_en'], language, row['medicine_name']))
            result['recommended_medicines'] = recommended
            conn.close()
        except Exception as e:
            print(f"[WARNING] Error fetching medicines: {e}")
            result['recommended_medicines'] = []

        # Save to session_log
        try:
            user_id = session.get('user', {}).get('user_id') if 'user' in session else None
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
            print(f"[WARNING] Error logging session: {e}")

        return jsonify(result)
    except Exception as e:
        print(f"[ERROR] Diagnose endpoint error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Failed to analyze symptoms", "details": str(e)}), 500


@main_bp.route('/summary/<int:log_id>')
def summary(log_id):
    req_lang = request.args.get('lang')
    if req_lang in ('en', 'bn', 'hi'):
        lang = req_lang
    else:
        lang = g.lang if g.lang in ('en', 'bn', 'hi') else 'en'
    log = get_log_by_id(log_id)
    if not log:
        return "Summary not found", 404
        
    symptom_ids = json.loads(log['symptoms_json']) if log['symptoms_json'] else []
    symptoms = [decode_mojibake_text(item) for item in get_symptoms_by_ids(symptom_ids, lang)]
    condition = get_condition_by_name(log['result_condition'], lang)
    if condition:
        condition['translated_name'] = decode_mojibake_text(condition.get('translated_name'))
        condition['first_aid_text'] = decode_mojibake_text(condition.get('first_aid_text'))
    
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
        cursor.execute(
            "SELECT name_en FROM medicines WHERE condition_id = ? AND otc_available = 1",
            (condition['condition_id'],),
        )
        m_rows = cursor.fetchall()
        medicines = [localize_medicine_name(row['name_en'], lang, row['name_en']) for row in m_rows]
        
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
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    print(f"DEBUG: Received payload keys: {data.keys()}")
    print(f"DEBUG: Image length: {len(data.get('image', ''))}")
    print(f"DEBUG: Media type: {data.get('media_type')}")
    
    if not data or 'image' not in data or 'media_type' not in data:
        return jsonify({"error": "Invalid payload format. Expected base64 image and media_type."}), 400
    
    image_data = data['image'].strip()
    if not image_data:
        return jsonify({"error": "Image data is empty."}), 400
    
    # Optional size validation (rough check on base64 string length)
    # 2MB is roughly 2.8MB base64 encoded
    if len(image_data) > 2.8 * 1024 * 1024:
        return jsonify({"error": "Image file too large. Max 2MB allowed."}), 400
        
    language = data.get('language', g.lang if hasattr(g, 'lang') else 'en')
    result = analyze_photo(image_data, data['media_type'], language=language)
    return jsonify(result)


@main_bp.route('/facilities')
def facilities():
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    limit = request.args.get('limit', default=10, type=int)

    if lat is None or lng is None:
        return jsonify({"error": "Missing lat/lng parameters"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM facilities")
    facs = cursor.fetchall()
    conn.close()

    results = with_distance(facs, lat, lng)
    return jsonify(results[:max(1, min(limit, 20))])


@main_bp.route('/nearby-hospitals')
def nearby_hospitals():
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    limit = request.args.get('limit', default=10, type=int)

    if lat is None or lng is None:
        return jsonify({"error": "Missing lat/lng parameters"}), 400

    hospitals = with_distance(CURATED_HOSPITALS, lat, lng)
    return jsonify(hospitals[:max(1, min(limit, 20))])


@main_bp.route('/ai-analysis')
def ai_analysis():
    return render_template('pages/ai_analysis.html', lang=g.lang)


@main_bp.route('/assistant')
def assistant():
    return render_template('pages/assistant.html', lang=g.lang)


@main_bp.route('/history', methods=['GET', 'POST', 'DELETE'])
@login_required
def history():
    conn = get_db_connection()
    cursor = conn.cursor()
    user_id = session['user']['user_id']

    if request.method == 'GET':
        ui_lang = request.args.get('lang')
        if ui_lang not in ('en', 'bn', 'hi'):
            ui_lang = g.lang if getattr(g, 'lang', None) in ('en', 'bn', 'hi') else 'en'
        cursor.execute(
            "SELECT * FROM session_log WHERE user_id = ? ORDER BY session_date DESC LIMIT 10",
            (user_id,),
        )
        logs = cursor.fetchall()
        cursor.execute("SELECT symptom_id, name_en, name_bn, name_hi FROM symptoms")
        symptom_rows = cursor.fetchall()
        supported_langs = ('en', 'bn', 'hi')
        symptom_lookup = {lang: {} for lang in supported_langs}
        symptom_alias_lookup = {lang: {} for lang in supported_langs}
        for s in symptom_rows:
            en_name = decode_mojibake_text((s['name_en'] or '').strip())
            bn_name = decode_mojibake_text((s['name_bn'] or '').strip())
            hi_name = decode_mojibake_text((s['name_hi'] or '').strip())
            localized_names = {'en': en_name, 'bn': bn_name, 'hi': hi_name}
            for lang_code in supported_langs:
                target_name = localized_names.get(lang_code, en_name) or en_name or str(s['symptom_id'])
                symptom_lookup[lang_code][str(s['symptom_id'])] = target_name
            for key in (en_name, bn_name, hi_name):
                if key:
                    normalized_key = normalize_i18n_key(key)
                    for lang_code in supported_langs:
                        symptom_alias_lookup[lang_code][normalized_key] = (
                            localized_names.get(lang_code, en_name) or en_name or key
                        )

        cursor.execute("SELECT name_en, name_bn, name_hi FROM conditions")
        condition_rows = cursor.fetchall()
        condition_lookup = {lang: {} for lang in supported_langs}
        for c in condition_rows:
            en_name = decode_mojibake_text((c['name_en'] or '').strip())
            bn_name = decode_mojibake_text((c['name_bn'] or '').strip())
            hi_name = decode_mojibake_text((c['name_hi'] or '').strip())
            localized_names = {'en': en_name, 'bn': bn_name, 'hi': hi_name}
            for key in (en_name, bn_name, hi_name):
                if key:
                    normalized_key = normalize_i18n_key(key)
                    for lang_code in supported_langs:
                        condition_lookup[lang_code][normalized_key] = (
                            localized_names.get(lang_code, en_name) or en_name or key
                        )
        conn.close()

        resolved_logs = []
        for log in logs:
            row = dict(log)
            symptom_names_by_lang = {lang: [] for lang in supported_langs}
            try:
                raw_items = json.loads(row.get('symptoms_json') or '[]')
                for item in raw_items:
                    item_text = str(item).strip()
                    if not item_text:
                        continue
                    decoded_item = decode_mojibake_text(item_text)
                    normalized_item = normalize_i18n_key(decoded_item)
                    for lang_code in supported_langs:
                        if item_text in symptom_lookup[lang_code]:
                            symptom_names_by_lang[lang_code].append(symptom_lookup[lang_code][item_text])
                        else:
                            symptom_names_by_lang[lang_code].append(
                                symptom_alias_lookup[lang_code].get(normalized_item, decoded_item)
                            )
            except Exception:
                fallback_symptom_text = decode_mojibake_text(row.get('symptoms_json', '-'))
                for lang_code in supported_langs:
                    symptom_names_by_lang[lang_code] = [fallback_symptom_text]

            for lang_code in supported_langs:
                row[f'symptom_names_{lang_code}'] = decode_mojibake_text(
                    ', '.join(symptom_names_by_lang[lang_code]) or '-'
                )
            row['symptom_names'] = row[f'symptom_names_{ui_lang}']

            condition_name = decode_mojibake_text((row.get('result_condition') or '').strip())
            if condition_name:
                matched_by_lang = {
                    lang_code: get_condition_by_name(condition_name, lang_code)
                    for lang_code in supported_langs
                }
                for lang_code in supported_langs:
                    row[f'result_condition_{lang_code}'] = decode_mojibake_text(
                        (matched_by_lang[lang_code] or {}).get('translated_name')
                        or condition_lookup[lang_code].get(normalize_i18n_key(condition_name), condition_name)
                    )
                row['result_condition'] = row[f'result_condition_{ui_lang}']
            else:
                for lang_code in supported_langs:
                    row[f'result_condition_{lang_code}'] = ''
            resolved_logs.append(row)

        return render_template('pages/history.html', logs=resolved_logs, lang=ui_lang)

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
    med_names = {
        m['medicine_id']: localize_medicine_name(m['medicine_name_en'], lang, m['medicine_name'])
        for m in medicines
    }

    placeholders = ','.join('?' * len(med_ids))
    cursor.execute(f'''
        SELECT DISTINCT f.facility_id, f.name, f.type, f.district,
               f.latitude, f.longitude, f.contact
        FROM facilities f
        JOIN facility_medicines fm ON f.facility_id = fm.facility_id
        WHERE fm.medicine_id IN ({placeholders})
    ''', med_ids)
    fac_rows = cursor.fetchall()

    # Graceful fallback: if medicine rows exist but stock-link rows are missing,
    # still show the nearest Jan Aushadhi centers with the mapped OTC labels.
    if not fac_rows:
        cursor.execute('''
            SELECT facility_id, name, type, district, latitude, longitude, contact
            FROM facilities
            WHERE type = 'Jan Aushadhi'
        ''')
        fac_rows = cursor.fetchall()

    results = []
    for fac in fac_rows:
        dist = haversine(lat, lng, fac['latitude'], fac['longitude'])
        cursor.execute(f'''
            SELECT fm.medicine_id FROM facility_medicines fm
            WHERE fm.facility_id = ? AND fm.medicine_id IN ({placeholders})
        ''', [fac['facility_id']] + med_ids)
        stocked_rows = cursor.fetchall()
        stocked_meds = [med_names[row['medicine_id']] for row in stocked_rows]
        if not stocked_meds:
            stocked_meds = [med_names[mid] for mid in med_ids]

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
    user = session.get('user') or {}
    raw_name = (user.get('name') or '').strip()
    first_name = raw_name.split()[0] if raw_name else None
    return render_template('pages/wellness.html', lang=lang, first_name=first_name)

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

    prompt_lines = [
        "You are MindCare, a compassionate mental wellness support assistant",
        "built into SwaHealthy, a rural health app for users in West Bengal, India.",
        "",
        "Rules you must always follow:",
        "- A warm, non-judgmental friend who understands mental health deeply.",
        "- You are NOT a therapist. Never diagnose. Never prescribe.",
        "- Respond ONLY in the same language the user writes in (Bengali, Hindi, or English).",
        "- Keep responses warm, non-clinical, and under 120 words.",
        "- End with either a follow-up question or a gentle encouragement — never a cold stop.",
        "- If the user seems emotionally distressed or very low, shift your response to include:",
        "  one immediate coping tip + a gentle mention of iCall (9152987821).",
        "- You may discuss: anxiety, depression, stress, sleep, relationships, loneliness,",
        "  motivation, self-care, breathing techniques, and general mental wellbeing.",
        "- If asked something unrelated to mental health, gently redirect back.",
        "- For mild stress → warm, practical, slightly upbeat",
        "- For moderate sadness → gentle, slow, validating — no rushed advice",
        "- For crisis signals → calm, grounding, human — never alarmed or robotic",
        "- Never use jargon. Write as a caring friend who happens to know about mental health.",
    ]
    if is_distressed:
        prompt_lines.append("- The user seems distressed. Prioritise warmth and one actionable tip first.")

    system_prompt = "\n".join(prompt_lines)

    messages = [{"role": "system", "content": system_prompt}]
    for h in history[-6:]:
        messages.append({"role": h.get('role', 'user'), "content": h.get('content', '')})
    
    # Only append user_message if history doesn't already end with it (frontend might have pushed it)
    if not history or history[-1].get('content') != user_message:
        messages.append({"role": "user", "content": user_message})

    try:
        from flask import current_app
        api_key = current_app.config.get('GROQ_API_KEY') or os.environ.get('GROQ_API_KEY')
        if not api_key:
            raise RuntimeError("GROQ_API_KEY is not configured")

        resp = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": messages,
                "max_tokens": 200,
                "temperature": 0.7
            },
            timeout=15
        )
        resp.raise_for_status()
        payload = resp.json()
        choices = payload.get('choices') or []
        if not choices:
            raise ValueError(f"Groq response missing choices: {payload}")

        message = choices[0].get('message') or {}
        reply = (message.get('content') or "").strip()
        if not reply:
            raise ValueError(f"Groq response missing assistant content: {payload}")
    except Exception as e:
        import traceback
        traceback.print_exc()
        reply = "I'm having trouble connecting right now. If you need immediate support, please call iCall: 9152987821 💙"

    return jsonify({'reply': reply, 'is_crisis': False})

@main_bp.route('/wellness/reflection', methods=['POST'])
def wellness_reflection():
    import requests, os, random
    from flask import current_app
    
    data = request.get_json()
    mood = data.get('mood', 'okay')
    language = data.get('language', 'en')
    
    # Varied prompt styles to get diverse responses
    prompt_styles = [
        f"The user feels '{mood}' today. Suggest ONE fresh journal reflection question (not a statement) in {language}. Max 18 words. No quotes.",
        f"Generate a warm, unique journaling prompt in {language} for someone feeling '{mood}'. Max 18 words. No quotes, no formatting.",
        f"Write one mindful observation or question for a daily journal. The person feels '{mood}'. Respond in {language}. Max 18 words.",
        f"Create a short, thought-provoking journal starter sentence in {language} for someone who feels '{mood}' today. Max 18 words. No quotes.",
        f"The user's mood today is '{mood}'. Write a gentle, introspective journal prompt in {language} to help them reflect. Max 18 words. No quotes."
        f"Given the mood '{mood}', suggest a single, simple journaling question in {language} to encourage self-reflection. Max 18 words. No quotes."
        f"Write a concise, empathetic journal prompt in {language} for someone experiencing the mood '{mood}'. Max 18 words. No quotes."
    ]
    prompt = random.choice(prompt_styles)

    try:
        api_key = current_app.config.get('GROQ_API_KEY') or os.environ.get('GROQ_API_KEY')
        resp = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "max_tokens": 60, "temperature": 0.95},
            timeout=10
        )
        content = resp.json()['choices'][0]['message']['content'].strip()
        # Remove any surrounding quotes the model might add
        content = content.strip('"').strip("'").strip()
        return jsonify({'reflection': content})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'reflection': None}), 500

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
If needed suggest or advice on general wellbeing, coping tips, or when to seek help. Always respond in the specified language.
Then on a new line write exactly "ACTIONS:" followed by exactly 3 specific actionable 
steps as a numbered list. Steps should be tailored to the answers, not generic.
Respond entirely in {language}."""

    try:
        api_key = current_app.config.get('GROQ_API_KEY') or os.environ.get('GROQ_API_KEY')
        resp = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "max_tokens": 350, "temperature": 0.6},
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
