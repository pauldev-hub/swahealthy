"""
Database schema initialisation and migrations.
"""

from backend.models.helpers import get_db_connection
from backend.models.seed import seed_data, seed_doctors


def init_db():
    """Create all tables (if missing), run migrations, and seed data."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # ── Tables ──────────────────────────────────────────────────────────

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS symptoms(
            symptom_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_en TEXT NOT NULL,
            name_bn TEXT NOT NULL,
            name_hi TEXT NOT NULL,
            body_area TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conditions(
            condition_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_en TEXT NOT NULL,
            name_bn TEXT NOT NULL,
            name_hi TEXT NOT NULL,
            severity TEXT NOT NULL,
            first_aid_en TEXT NOT NULL,
            first_aid_bn TEXT NOT NULL,
            first_aid_hi TEXT NOT NULL,
            see_doctor INTEGER DEFAULT 0,
            emergency_note TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS condition_symptoms(
            condition_id INTEGER,
            symptom_id INTEGER,
            is_required INTEGER DEFAULT 0,
            weight INTEGER DEFAULT 1,
            FOREIGN KEY (condition_id) REFERENCES conditions(condition_id),
            FOREIGN KEY (symptom_id) REFERENCES symptoms(symptom_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS facilities(
            facility_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            district TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            contact TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            google_id TEXT UNIQUE,
            name TEXT,
            email TEXT,
            profile_pic TEXT,
            age INTEGER,
            gender TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS session_log(
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            age INTEGER,
            gender TEXT,
            session_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            symptoms_json TEXT NOT NULL,
            result_condition TEXT,
            severity TEXT,
            language TEXT DEFAULT 'en',
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS doctors(
            doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialisation TEXT NOT NULL,
            available_days_json TEXT NOT NULL,
            slots_json TEXT NOT NULL,
            contact TEXT,
            language TEXT DEFAULT 'en'
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments(
            appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            doctor_id INTEGER,
            patient_name TEXT NOT NULL,
            patient_phone TEXT NOT NULL,
            appointment_date TEXT NOT NULL,
            appointment_time TEXT NOT NULL,
            reason TEXT,
            status TEXT DEFAULT 'pending',
            language TEXT DEFAULT 'en',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medicines(
            medicine_id INTEGER PRIMARY KEY AUTOINCREMENT,
            condition_id INTEGER NOT NULL,
            name_en TEXT NOT NULL,
            name_bn TEXT NOT NULL,
            name_hi TEXT NOT NULL,
            otc_available INTEGER DEFAULT 1,
            FOREIGN KEY (condition_id) REFERENCES conditions(condition_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS facility_medicines(
            facility_id INTEGER NOT NULL,
            medicine_id INTEGER NOT NULL,
            FOREIGN KEY (facility_id) REFERENCES facilities(facility_id),
            FOREIGN KEY (medicine_id) REFERENCES medicines(medicine_id),
            PRIMARY KEY (facility_id, medicine_id)
        )
    ''')

    # ── Seed if empty ───────────────────────────────────────────────────

    cursor.execute('SELECT COUNT(*) FROM symptoms')
    if cursor.fetchone()[0] == 0:
        seed_data(cursor)

    cursor.execute('SELECT COUNT(*) FROM doctors')
    if cursor.fetchone()[0] == 0:
        seed_doctors(cursor)



    # ── Migrations ──────────────────────────────────────────────────────

    cursor.execute("PRAGMA table_info(session_log)")
    columns = [row[1] for row in cursor.fetchall()]
    if 'user_id' not in columns:
        cursor.execute("ALTER TABLE session_log ADD COLUMN user_id INTEGER REFERENCES users(user_id)")
        print("[MIGRATION] Added user_id column to session_log")
    if 'age' not in columns:
        cursor.execute("ALTER TABLE session_log ADD COLUMN age INTEGER")
        print("[MIGRATION] Added age column to session_log")
    if 'gender' not in columns:
        cursor.execute("ALTER TABLE session_log ADD COLUMN gender TEXT")
        print("[MIGRATION] Added gender column to session_log")

    cursor.execute("PRAGMA table_info(users)")
    user_columns = [row[1] for row in cursor.fetchall()]
    if 'age' not in user_columns:
        cursor.execute("ALTER TABLE users ADD COLUMN age INTEGER")
        print("[MIGRATION] Added age column to users")
    if 'gender' not in user_columns:
        cursor.execute("ALTER TABLE users ADD COLUMN gender TEXT")
        print("[MIGRATION] Added gender column to users")

    expand_seed_data(cursor)
    reseed_medicines(cursor)

    conn.commit()
    conn.close()


def expand_seed_data(cursor):
    """Expanded symptoms, categories and conditions — idempotent two-stage seeding."""

    # ── Stage 1: Symptoms + Conditions (only if not yet seeded) ─────────────
    cursor.execute("SELECT COUNT(*) FROM symptoms WHERE body_area = 'eyes'")
    need_symptoms = cursor.fetchone()[0] == 0

    if need_symptoms:
        new_symptoms = [
            # eyes
            ("Eye redness",       "চোখ লাল হওয়া",          "आँख लाल होना",          "eyes"),
            ("Eye discharge",     "চোখ থেকে পিচুটি",        "आँख से चिपचिपापन",      "eyes"),
            ("Blurred vision",    "ঝাপসা দৃষ্টি",           "धुंधली दृष्टि",         "eyes"),
            ("Eye itching",       "চোখে চুলকানি",           "आँख में खुजली",         "eyes"),
            ("Eye pain",          "চোখে ব্যথা",              "आँख में दर्द",          "eyes"),
            ("Sensitivity to light", "আলোয় অস্বস্তি",      "रोशनी से तकलीफ",        "eyes"),
            ("Watery eyes",       "চোখ দিয়ে জল পড়া",       "आँखों से पानी आना",     "eyes"),
            # ears
            ("Ear pain",          "কানে ব্যথা",              "कान में दर्द",          "ears"),
            ("Ringing in ears",   "কানে শোঁ শোঁ শব্দ",      "कान में घंटी बजना",     "ears"),
            ("Ear discharge",     "কান থেকে পুঁজ বা তরল",   "कान से पस या तरल",      "ears"),
            ("Hearing loss",      "শ্রবণশক্তি কমা",          "सुनने में कमी",         "ears"),
            ("Ear fullness",      "কান বন্ধ লাগা",           "कान भरा हुआ लगना",      "ears"),
            ("Itching in ear",    "কানে চুলকানি",            "कान में खुजली",         "ears"),
            # joints
            ("Joint pain",        "গাঁটে ব্যথা",             "जोड़ों में दर्द",        "joints"),
            ("Joint swelling",    "গাঁট ফোলা",               "जोड़ों में सूजन",        "joints"),
            ("Joint stiffness",   "গাঁট শক্ত হওয়া",          "जोड़ों में अकड़न",       "joints"),
            ("Muscle pain",       "মাংসপেশিতে ব্যথা",        "मांसपेशियों में दर्द",   "joints"),
            ("Back pain",         "পিঠে ব্যথা",              "पीठ में दर्द",          "joints"),
            ("Knee pain",         "হাঁটুতে ব্যথা",           "घुटने में दर्द",        "joints"),
            ("Difficulty walking","হাঁটতে কষ্ট",             "चलने में तकलीफ",        "joints"),
            # urinary
            ("Burning urination", "প্রস্রাবে জ্বালা",        "पेशाब में जलन",         "urinary"),
            ("Frequent urination","ঘন ঘন প্রস্রাব",          "बार-बार पेशाब",         "urinary"),
            ("Blood in urine",    "প্রস্রাবে রক্ত",          "पेशाब में खून",         "urinary"),
            ("Cloudy urine",      "ঘোলা প্রস্রাব",           "गंदला पेशाब",           "urinary"),
            ("Lower abdominal pain","তলপেটে ব্যথা",         "पेट के निचले हिस्से में दर्द","urinary"),
            ("Difficulty urinating","প্রস্রাব করতে কষ্ট",   "पेशाब करने में कठिनाई", "urinary"),
            # mental
            ("Anxiety",           "উদ্বেগ",                   "चिंता",                 "mental"),
            ("Low mood",          "মন খারাপ",                "मन उदास रहना",          "mental"),
            ("Sleep difficulty",  "ঘুমের সমস্যা",            "नींद न आना",            "mental"),
            ("Fatigue",           "অবসাদ",                   "थकान",                  "mental"),
            ("Poor concentration","মনোযোগের অভাব",           "ध्यान न लगना",          "mental"),
            ("Loss of appetite",  "খাওয়ার ইচ্ছা না থাকা",    "भूख न लगना",            "mental"),
            ("Irritability",      "খিটখিটে মেজাজ",           "चिड़चिड़ापन",            "mental"),
            ("Hopelessness",      "হতাশা",                   "निराशा",                "mental"),
            # women
            ("Irregular periods", "অনিয়মিত মাসিক",          "अनियमित मासिक धर्म",    "women"),
            ("Painful periods",   "মাসিকে ব্যথা",            "मासिक धर्म में दर्द",   "women"),
            ("Heavy bleeding",    "অতিরিক্ত রক্তস্রাব",     "अधिक रक्तस्राव",        "women"),
            ("Missed period",     "মাসিক বন্ধ",              "मासिक धर्म न आना",      "women"),
            ("Vaginal discharge", "যোনি স্রাব",              "योनि स्राव",            "women"),
            ("Pregnancy nausea",  "গর্ভাবস্থায় বমি বমি ভাব","गर्भावस्था में मतली",   "women"),
            ("Breast pain",       "স্তনে ব্যথা",             "स्तन में दर्द",         "women"),
            # skin extras
            ("Blisters",          "ফোসকা",                   "फफोले",                 "skin"),
            ("Crusty skin patches","খসখসে চামড়া",           "पपड़ीदार त्वचा",         "skin"),
            ("Intense skin itching","তীব্র চুলকানি",         "तीव्र खुजली",           "skin"),
            ("Skin sores",        "চামড়ায় ঘা",              "त्वचा पर घाव",          "skin"),
            # general extras
            ("Pallor / pale skin","ফ্যাকাশে চেহারা",         "पीली त्वचा",            "general"),
            ("Rapid heartbeat",   "দ্রুত হৃদস্পন্দন",        "तेज़ दिल की धड़कन",      "general"),
            ("Excessive thirst",  "অতিরিক্ত তৃষ্ণা",        "अत्यधिक प्यास",         "general"),
            ("Unexplained weight loss","অকারণে ওজন কমা",    "बिना कारण वजन कम होना", "general"),
        ]
        for s in new_symptoms:
            cursor.execute(
                "INSERT INTO symptoms (name_en, name_bn, name_hi, body_area) VALUES (?, ?, ?, ?)", s
            )

        new_conditions = [
            ("Conjunctivitis (Pink Eye)", "কনজাঙ্কটিভাইটিস (চোখ ওঠা)", "कंजंक्टिवाइटिस", "low",
             "Clean eye with clean water\nAvoid touching\nNo shared towels\nUse sunglasses outdoors\nSee doctor if worsening after 2 days",
             "পরিষ্কার জল দিয়ে চোখ ধোবেন\nচোখে হাত দেবেন না\nতোয়ালে ভাগ করবেন না\nবাইরে সানগ্লাস পরুন\n২ দিন পর খারাপ হলে ডাক্তার দেখান",
             "साफ पानी से आंख साफ करें\nछूने से बचें\nतौलिए साझा न करें\nबाहर धूप का चश्मा पहनें\n2 दिन बाद बिगड़ने पर डॉक्टर को दिखाएं",
             1, None),
            ("Ear Infection", "কানের সংক্রমণ", "कान का संक्रमण", "medium",
             "Do not insert anything in ear\nTake paracetamol for pain\nKeep ear dry\nSee doctor for antibiotic prescription\nNo swimming",
             "কানে কিছু ঢোকাবেন না\nব্যথার জন্য প্যারাসিটামল খান\nকান শুকনো রাখুন\nঅ্যান্টিবায়োটিকের জন্য ডাক্তার দেখান\nসাঁতার কাটবেন না",
             "कान में कुछ न डालें\nदर्द के लिए पैरासिटामोल लें\nकान को सूखा रखें\nएंटीबायोटिक के लिए डॉक्टर को दिखाएं\nतैरना मना है",
             1, None),
            ("UTI (Urinary Tract Infection)", "ইউটিআই (মূত্রনালীর সংক্রমণ)", "यूटीआई (मूत्र पथ संक्रमण)", "medium",
             "Drink plenty of water\nDo not hold urine\nSee doctor for antibiotics\nAvoid spicy food\nComplete full antibiotic course if prescribed",
             "প্রচুর জল পান করুন\nপ্রস্রাব আটকে রাখবেন না\nঅ্যান্টিবায়োটিকের জন্য ডাক্তার দেখান\nঝাল খাবার এড়িয়ে চলুন\nপরামর্শমতো অ্যান্টিবায়োটিক কোর্স শেষ করুন",
             "खूब पानी पिएं\nपेशाब न रोकें\nएंटीबायोटिक के लिए डॉक्टर को दिखाएं\nमसालेदार भोजन से बचें\nएंटीबायोटिक का कोर्स पूरा करें",
             1, None),
            ("Chickenpox", "জলবসন্ত", "चेचक (चिकनपॉक्स)", "medium",
             "Do not scratch blisters\nTrim nails short\nApply calamine lotion\nIsolate from others especially pregnant women and children\nSee doctor immediately",
             "ফোসকা চুলকাবেন না\nনখ ছোট রাখুন\nক্যালামাইন লোশন লাগান\nঅন্যদের থেকে আলাদা থাকুন, বিশেষ করে গর্ভবতী নারী ও শিশুদের থেকে\nঅবিলম্বে ডাক্তার দেখান",
             "फफोले न खुजलाएं\nनाखून छोटे रखें\nकैलामाइन लोशन लगाएं\nदूसरों से अलग रहें खासकर गर्भवती महिलाओं और बच्चों से\nतुरंत डॉक्टर को दिखाएं",
             1, None),
            ("Scabies", "স্ক্যাবিস (খোশপঁচড়া)", "खाज (खुजली)", "low",
             "See doctor for prescription cream\nWash all clothes and bedding in hot water\nAvoid skin contact with others\nAll household members should be treated simultaneously",
             "ক্রিমের জন্য ডাক্তার দেখান\nসমস্ত জামাকাপড় এবং বিছানার চাদর গরম জলে ধুয়ে নিন\nঅন্যদের সাথে ত্বকের যোগাযোগ এড়ান\nবাড়ির সকল সদস্যের একসাথে চিকিৎসা করা উচিত",
             "क्रीम के लिए डॉक्टर को दिखाएं\nसभी कपड़े और बिस्तर गर्म पानी में धोएं\nदूसरों के साथ त्वचा के संपर्क से बचें\nघर के सभी सदस्यों का एक साथ इलाज होना चाहिए",
             1, None),
            ("Anaemia Risk", "রক্তাল্পতার ঝুঁকি", "एनीमिया का जोखिम", "medium",
             "Eat iron-rich foods (spinach, lentils, jaggery)\nTake iron supplements only if prescribed\nAvoid tea/coffee with meals\nSee doctor for blood test confirmation\nWomen should check for heavy periods",
             "আয়রন সমৃদ্ধ খাবার খান (পালং শাক, ডাল, গুড়)\nপরামর্শ দেওয়া হলে তবেই আয়রন সাপ্লিমেন্ট খান\nখাবারের সাথে চা/কফি এড়িয়ে চলুন\nরক্ত ​​পরীক্ষার জন্য ডাক্তার দেখান\nমহিলাদের অতিরিক্ত মাসিকের সমস্যা আছে কিনা তা পরীক্ষা করা উচিত",
             "आयरन युक्त भोजन करें (पालक, दाल, गुड़)\nसलाह दी गई हो तो ही आयरन सप्लीमेंट लें\nभोजन के साथ चाय/कॉफी से बचें\nरक्त परीक्षण के लिए डॉक्टर को दिखाएं\nमहिलाओं को अधिक मासिक धर्म की जांच करनी चाहिए",
             1, None),
            ("Hypertension Risk", "উচ্চ রক্তচাপের ঝুঁকি", "उच्च रक्तचाप का जोखिम", "high",
             "Sit and rest immediately\nMeasure BP if possible\nAvoid salt and heavy exertion\nTake prescribed BP medicine if already on it\nSee doctor today do not wait",
             "অবিলম্বে বসুন এবং বিশ্রাম নিন\nসম্ভব হলে বিপি মাপুন\nলবণ এবং ভারী পরিশ্রম এড়িয়ে চলুন\nওষুধ চললে বিপি-র ওষুধ খান\nআজই ডাক্তার দেখান, অপেক্ষা করবেন না",
             "तुरंत बैठें और आराम करें\nसंभव हो तो बीपी मापें\nनमक और भारी मेहनत से बचें\nपहले से चल रही बीपी की दवा लें\nआज ही डॉक्टर को दिखाएं, प्रतीक्षा न करें",
             1, None),
            ("General Illness", "সাধারণ অসুস্থতা", "सामान्य बीमारी", "medium",
             "Rest and drink plenty of fluids\nMonitor temperature\nConsult a doctor if symptoms persist or worsen",
             "বিশ্রাম নিন এবং প্রচুর তরল পান করুন\nশরীরের তাপমাত্রা লক্ষ্য রাখুন\nলক্ষণগুলি ৪-৫ দিনের বেশি থাকলে ডাক্তার দেখান",
             "आराम करें और खूब तरल पदार्थ पिएं\nतापमान पर नज़र रखें\nयदि लक्षण बने रहते हैं या बिगड़ते हैं तो डॉक्टर से परामर्श करें",
             1, None),
        ]

        cond_ids = {}
        for c in new_conditions:
            cursor.execute("""
                INSERT INTO conditions (
                    name_en, name_bn, name_hi, severity,
                    first_aid_en, first_aid_bn, first_aid_hi,
                    see_doctor, emergency_note
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, c)
            cond_ids[c[0]] = cursor.lastrowid

        cursor.execute("SELECT symptom_id, name_en FROM symptoms")
        symp_map = {row['name_en']: row['symptom_id'] for row in cursor.fetchall()}

        mappings = [
            ("Conjunctivitis (Pink Eye)",
             ["Eye redness", "Eye discharge"],
             [("Eye itching", 2), ("Watery eyes", 1), ("Eye pain", 1)]),
            ("Ear Infection",
             ["Ear pain", "Ear discharge"],
             [("Hearing loss", 2), ("Ear fullness", 2), ("Fever", 1)]),
            ("UTI (Urinary Tract Infection)",
             ["Burning urination", "Frequent urination"],
             [("Lower abdominal pain", 2), ("Cloudy urine", 2), ("Blood in urine", 3)]),
            ("Chickenpox",
             ["Blisters", "Fever"],
             [("Intense skin itching", 3), ("Skin sores", 2), ("Fatigue", 1)]),
            ("Scabies",
             ["Intense skin itching", "Skin sores"],
             [("Crusty skin patches", 2)]),
            ("Anaemia Risk",
             ["Pallor / pale skin", "Fatigue"],
             [("Rapid heartbeat", 2), ("Loss of appetite", 2), ("Unexplained weight loss", 1), ("Dizziness", 1)]),
            ("Hypertension Risk",
             ["Rapid heartbeat", "Headache"],
             [("Dizziness", 2), ("Blurred vision", 2), ("Fatigue", 1)]),
        ]

        for c_name, reqs, opts in mappings:
            c_id = cond_ids[c_name]
            for r_name in reqs:
                s_id = symp_map.get(r_name)
                if s_id:
                    cursor.execute(
                        "INSERT INTO condition_symptoms (condition_id, symptom_id, is_required, weight) VALUES (?, ?, 1, 3)",
                        (c_id, s_id)
                    )
                else:
                    print(f"[WARNING] Required symptom '{r_name}' not found for {c_name}")
            for o_name, w in opts:
                s_id = symp_map.get(o_name)
                if s_id:
                    cursor.execute(
                        "INSERT INTO condition_symptoms (condition_id, symptom_id, is_required, weight) VALUES (?, ?, 0, ?)",
                        (c_id, s_id, w)
                    )
                else:
                    print(f"[WARNING] Optional symptom '{o_name}' not found for {c_name}")
    else:
        # Symptoms already seeded — fetch existing condition IDs for medicine linking
        cond_ids = {}
        target_conditions = [
            'Conjunctivitis (Pink Eye)', 'Ear Infection', 'UTI (Urinary Tract Infection)',
            'Chickenpox', 'Scabies', 'Anaemia Risk', 'Hypertension Risk', 'General Illness'
        ]
        for c_name in target_conditions:
            cursor.execute("SELECT condition_id FROM conditions WHERE name_en = ?", (c_name,))
            row = cursor.fetchone()
            if row:
                cond_ids[c_name] = row["condition_id"]
            elif c_name == "General Illness":
                cursor.execute("""
                    INSERT INTO conditions (name_en, name_bn, name_hi, severity, first_aid_en, first_aid_bn, first_aid_hi, see_doctor)
                    VALUES ("General Illness", "সাধারণ অসুস্থতা", "सामान्य बीमारी", "medium", 
                            "Rest and drink plenty of fluids", "বিশ্রাম নিন এবং প্রচুর তরল পান করুন", "आराम करें और खूब तरल पदार्थ पिएं", 1)
                """)
                cond_ids[c_name] = cursor.lastrowid

    print("Expanded seed data loaded successfully")


def reseed_medicines(cursor):
    """Strictly enforce OTC medicine mappings by wiping and reseeding."""
    # Wipe existing mappings safely
    cursor.execute("DELETE FROM facility_medicines")
    cursor.execute("DELETE FROM medicines")
    
    # Define strict mapping
    MEDICINE_MAP = {
        'Common Cold': ['Cetirizine 10mg', 'Guaifenesin syrup', 'Vitamin C 500mg'],
        'Dengue Risk': ['Paracetamol 500mg', 'ORS Sachets'],
        'Malaria Risk': ['Paracetamol 500mg', 'ORS Sachets'],
        'Typhoid Risk': ['Paracetamol 500mg', 'ORS Sachets'],
        'Food Poisoning': ['ORS Sachets', 'Activated Charcoal', 'Domperidone 10mg'],
        'Dehydration': ['ORS Sachets', 'Electrolyte Powder'],
        'Gastritis': ['Antacid (Gelusil)', 'Domperidone 10mg'],
        'Diarrhea': ['ORS Sachets', 'Loperamide 2mg', 'Zinc Sulfate 20mg'],
        'Skin Allergy': ['Cetirizine 10mg', 'Calamine Lotion', 'Hydrocortisone 1% Cream'],
        'Conjunctivitis (Pink Eye)': ['Sodium Chloride Eye Drops', 'Chloramphenicol Eye Drops'],
        'Ear Infection': ['Otocain Ear Drops', 'Paracetamol 500mg'],
        'Asthma Attack': ['Salbutamol Inhaler'],
        'Heat Stroke': ['ORS Sachets', 'Electrolyte Powder'],
        'Migraine': ['Paracetamol 500mg', 'Ibuprofen 400mg'],
        'Jaundice Risk': ['Vitamin C 500mg', 'ORS Sachets'],
        'UTI': ['Potassium Citrate Sachets', 'Cranberry Extract Tablet'],
        'Chest Infection': ['Guaifenesin Syrup', 'Paracetamol 500mg'],
        'Fungal Infection': ['Clotrimazole Cream'],
        'Wound/Skin Infection': ['Betadine Ointment', 'Paracetamol 500mg'],
        'Sore Throat': ['Povidone Iodine Gargle', 'Strepsils'],
        'General Illness': ['Paracetamol 500mg', 'Vitamin C 500mg'],
    }
    
    MEDICINE_TRANSLATIONS = {
        'Cetirizine 10mg': ('সেটিরিজিন ১০মিগ্রা', 'सेटीरिज़ीन 10mg'),
        'Guaifenesin syrup': ('গুফেনেসিন সিরাপ', 'गुइफ़ेनेसिन सिरप'),
        'Guaifenesin Syrup': ('গুফেনেসিন সিরাপ', 'गुइफ़ेनेसिन सिरप'),
        'Vitamin C 500mg': ('ভিটামিন সি ৫০০মিগ্রা', 'विटामिन सी 500mg'),
        'Paracetamol 500mg': ('প্যারাসিটামল ৫০০মিগ্রা', 'पैरासिटामोल 500mg'),
        'ORS Sachets': ('ওআরএস স্যাসে', 'ओआरएस पाउच'),
        'Activated Charcoal': ('অ্যাক্টিভেটেড চারকোল', 'एक्टिवेटेड चारकोल'),
        'Domperidone 10mg': ('ডমপেরিডন ১০মিগ্রা', 'डोम्पेरिडोन 10mg'),
        'Electrolyte Powder': ('ইলেক্ট্রোলাইট পাউডার', 'इलेक्ट्रोलाइट पाउडर'),
        'Antacid (Gelusil)': ('অ্যান্টাসিড (জেলুসিল)', 'एंटासिड (जेलुसिल)'),
        'Loperamide 2mg': ('লোপেরামাইড ২মিগ্রা', 'लोपरामाइड 2mg'),
        'Zinc Sulfate 20mg': ('জিঙ্ক সালফেট ২০মিগ্রা', 'जिंक सल्फेट 20mg'),
        'Calamine Lotion': ('ক্যালামাইন লোশন', 'कैलामाइन लोशन'),
        'Hydrocortisone 1% Cream': ('হাইড্রোকর্টিসোন ১% ক্রিম', 'हाइड्रोकार्टिसोन 1% क्रीम'),
        'Sodium Chloride Eye Drops': ('স্যালাইন আই ড্রপ', 'सेलाइन आई ड्रॉप'),
        'Chloramphenicol Eye Drops': ('ক্লোরামফেনিকল আই ড্রপ', 'क्लोरैम्फेनिकॉल आई ड्रॉप'),
        'Otocain Ear Drops': ('অটোকেন ইয়ার ড্রপ', 'ओटोकेन ईयर ड्रॉप'),
        'Salbutamol Inhaler': ('সালবিউটামল ইনহেলার', 'सालबुटामोल इन्हेलर'),
        'Ibuprofen 400mg': ('আইবুপ্রোফেন ৪০০মিগ্রা', 'इबुप्रोफेन 400mg'),
        'Potassium Citrate Sachets': ('পটাসিয়াম সিট্রেট স্যাসে', 'पोटेशियम साइट्रेट पाउच'),
        'Cranberry Extract Tablet': ('ক্র্যানবেরি সারাংশের ট্যাবলেট', 'क्रैनबेरी अर्क टैबलेट'),
        'Clotrimazole Cream': ('ক্লোট্রাইমাজোল ক্রিম', 'क्लोट्रिमेज़ोल क्रीम'),
        'Betadine Ointment': ('বিটাদিন মলম', 'बीटाडीन मलहम'),
        'Povidone Iodine Gargle': ('পোভিডোন আয়োডিন গার্গল', 'पोविडोन आयोडीन गरारे'),
        'Strepsils': ('স্ট্রেপসিলস', 'स्ट्रेप्सिल्स'),
    }
    
    # 1. Map conditions
    cursor.execute("SELECT condition_id, name_en FROM conditions")
    cond_rows = cursor.fetchall()
    
    new_med_ids = []
    
    for row in cond_rows:
        c_id = row['condition_id']
        c_name = row['name_en']
        
        # Match using exact or contains
        matched_key = None
        for key in MEDICINE_MAP.keys():
            k_clean = key.lower().replace('risk', '').strip()
            # specifically map gastroenteritis to food poisoning or diarrhea if we want
            c_clean = c_name.lower().replace('risk', '').strip()
            
            if k_clean in c_clean or c_clean in k_clean:
                matched_key = key
                break
                
            # Extra mapping for Gastroenteritis since Diarrhea/Gastritis isn't exactly matching
            if 'gastroenteritis' in c_clean and key == 'Diarrhea':
                matched_key = key
                break
                
        if matched_key:
            meds = MEDICINE_MAP[matched_key]
            for m_name in meds:
                bn, hi = MEDICINE_TRANSLATIONS.get(m_name, (m_name, m_name))
                cursor.execute('''
                    INSERT INTO medicines (condition_id, name_en, name_bn, name_hi, otc_available)
                    VALUES (?, ?, ?, ?, 1)
                ''', (c_id, m_name, bn, hi))
                new_med_ids.append(cursor.lastrowid)

    # 2. Link to facilities
    cursor.execute("SELECT facility_id FROM facilities WHERE type IN ('Jan Aushadhi', 'Pharmacy')")
    pharma_facs = [r['facility_id'] for r in cursor.fetchall()]
    
    for fac_id in pharma_facs:
        for m_id in new_med_ids:
            cursor.execute(
                "INSERT OR IGNORE INTO facility_medicines (facility_id, medicine_id) VALUES (?, ?)",
                (fac_id, m_id)
            )


def reseed_medicines(cursor):
    """Strictly enforce OTC medicine mappings by wiping and reseeding."""
    cursor.execute("DELETE FROM facility_medicines")
    cursor.execute("DELETE FROM medicines")

    def normalize_condition_name(name):
        cleaned = ''.join(ch.lower() if ch.isalnum() else ' ' for ch in (name or ''))
        return ' '.join(cleaned.split())

    medicine_map = {
        'common cold': ['Cetirizine 10mg', 'Guaifenesin Syrup', 'Vitamin C 500mg', 'Povidone Iodine Gargle', 'Strepsils'],
        'influenza': ['Paracetamol 500mg', 'Cetirizine 10mg', 'Guaifenesin Syrup', 'Vitamin C 500mg'],
        'dengue risk': ['Paracetamol 500mg', 'ORS Sachets'],
        'malaria risk': ['Paracetamol 500mg', 'ORS Sachets'],
        'typhoid risk': ['Paracetamol 500mg', 'ORS Sachets'],
        'food poisoning': ['ORS Sachets', 'Activated Charcoal', 'Domperidone 10mg'],
        'gastroenteritis': ['ORS Sachets', 'Loperamide 2mg', 'Zinc Sulfate 20mg'],
        'dehydration': ['ORS Sachets', 'Electrolyte Powder'],
        'gastritis': ['Antacid (Gelusil)', 'Domperidone 10mg'],
        'diarrhea': ['ORS Sachets', 'Loperamide 2mg', 'Zinc Sulfate 20mg'],
        'skin allergy': ['Cetirizine 10mg', 'Calamine Lotion', 'Hydrocortisone 1% Cream'],
        'fungal infection': ['Clotrimazole Cream'],
        'scabies': ['Clotrimazole Cream', 'Calamine Lotion', 'Hydrocortisone 1% Cream'],
        'conjunctivitis': ['Sodium Chloride Eye Drops', 'Chloramphenicol Eye Drops'],
        'ear infection': ['Otocain Ear Drops', 'Paracetamol 500mg'],
        'asthma attack': ['Salbutamol Inhaler'],
        'heat stroke': ['ORS Sachets', 'Electrolyte Powder'],
        'migraine': ['Paracetamol 500mg', 'Ibuprofen 400mg'],
        'tension headache': ['Paracetamol 500mg', 'Ibuprofen 400mg'],
        'jaundice risk': ['Vitamin C 500mg', 'ORS Sachets'],
        'uti': ['Potassium Citrate Sachets', 'Cranberry Extract Tablet'],
        'urinary tract infection': ['Potassium Citrate Sachets', 'Cranberry Extract Tablet'],
        'chest infection': ['Guaifenesin Syrup', 'Paracetamol 500mg'],
        'wound skin infection': ['Betadine Ointment', 'Paracetamol 500mg'],
        'sore throat': ['Povidone Iodine Gargle', 'Strepsils'],
        'general illness': ['Paracetamol 500mg', 'Vitamin C 500mg'],
        'anaemia': ['Iron + Folic Acid Tablets', 'Vitamin C 500mg'],
        'anaemia risk': ['Iron + Folic Acid Tablets', 'Vitamin C 500mg'],
        'anemia': ['Iron + Folic Acid Tablets', 'Vitamin C 500mg'],
        'anemia risk': ['Iron + Folic Acid Tablets', 'Vitamin C 500mg'],
        'hypertension risk': ['Vitamin C 500mg'],
        'chickenpox': ['Calamine Lotion', 'Paracetamol 500mg', 'Vitamin C 500mg'],
        'chickenpox risk': ['Calamine Lotion', 'Paracetamol 500mg', 'Vitamin C 500mg'],
    }

    medicine_aliases = {
        'pink eye': 'conjunctivitis',
        'conjunctivitis pink eye': 'conjunctivitis',
        'urinary infection': 'urinary tract infection',
    }

    medicine_translations = {
        'Cetirizine 10mg': ('à¦¸à§‡à¦Ÿà¦¿à¦°à¦¿à¦œà¦¿à¦¨ à§§à§¦à¦®à¦¿à¦—à§à¦°à¦¾', 'à¤¸à¥‡à¤Ÿà¥€à¤°à¤¿à¤œà¤¼à¥€à¤¨ 10mg'),
        'Guaifenesin syrup': ('à¦—à§à¦«à§‡à¦¨à§‡à¦¸à¦¿à¦¨ à¦¸à¦¿à¦°à¦¾à¦ª', 'à¤—à¥à¤‡à¤«à¤¼à¥‡à¤¨à¥‡à¤¸à¤¿à¤¨ à¤¸à¤¿à¤°à¤ª'),
        'Guaifenesin Syrup': ('à¦—à§à¦«à§‡à¦¨à§‡à¦¸à¦¿à¦¨ à¦¸à¦¿à¦°à¦¾à¦ª', 'à¤—à¥à¤‡à¤«à¤¼à¥‡à¤¨à¥‡à¤¸à¤¿à¤¨ à¤¸à¤¿à¤°à¤ª'),
        'Vitamin C 500mg': ('à¦­à¦¿à¦Ÿà¦¾à¦®à¦¿à¦¨ à¦¸à¦¿ à§«à§¦à§¦à¦®à¦¿à¦—à§à¦°à¦¾', 'à¤µà¤¿à¤Ÿà¤¾à¤®à¤¿à¤¨ à¤¸à¥€ 500mg'),
        'Paracetamol 500mg': ('à¦ªà§à¦¯à¦¾à¦°à¦¾à¦¸à¦¿à¦Ÿà¦¾à¦®à¦² à§«à§¦à§¦à¦®à¦¿à¦—à§à¦°à¦¾', 'à¤ªà¥ˆà¤°à¤¾à¤¸à¤¿à¤Ÿà¤¾à¤®à¥‹à¤² 500mg'),
        'ORS Sachets': ('à¦“à¦†à¦°à¦à¦¸ à¦¸à§à¦¯à¦¾à¦¸à§‡', 'à¤“à¤†à¤°à¤à¤¸ à¤ªà¤¾à¤‰à¤š'),
        'Activated Charcoal': ('à¦…à§à¦¯à¦¾à¦•à§à¦Ÿà¦¿à¦­à§‡à¦Ÿà§‡à¦¡ à¦šà¦¾à¦°à¦•à§‹à¦²', 'à¤à¤•à¥à¤Ÿà¤¿à¤µà¥‡à¤Ÿà¥‡à¤¡ à¤šà¤¾à¤°à¤•à¥‹à¤²'),
        'Domperidone 10mg': ('à¦¡à¦®à¦ªà§‡à¦°à¦¿à¦¡à¦¨ à§§à§¦à¦®à¦¿à¦—à§à¦°à¦¾', 'à¤¡à¥‹à¤®à¥à¤ªà¥‡à¤°à¤¿à¤¡à¥‹à¤¨ 10mg'),
        'Electrolyte Powder': ('à¦‡à¦²à§‡à¦•à§à¦Ÿà§à¦°à§‹à¦²à¦¾à¦‡à¦Ÿ à¦ªà¦¾à¦‰à¦¡à¦¾à¦°', 'à¤‡à¤²à¥‡à¤•à¥à¤Ÿà¥à¤°à¥‹à¤²à¤¾à¤‡à¤Ÿ à¤ªà¤¾à¤‰à¤¡à¤°'),
        'Antacid (Gelusil)': ('à¦…à§à¦¯à¦¾à¦¨à§à¦Ÿà¦¾à¦¸à¦¿à¦¡ (à¦œà§‡à¦²à§à¦¸à¦¿à¦²)', 'à¤à¤‚à¤Ÿà¤¾à¤¸à¤¿à¤¡ (à¤œà¥‡à¤²à¥à¤¸à¤¿à¤²)'),
        'Loperamide 2mg': ('à¦²à§‹à¦ªà§‡à¦°à¦¾à¦®à¦¾à¦‡à¦¡ à§¨à¦®à¦¿à¦—à§à¦°à¦¾', 'à¤²à¥‹à¤ªà¤°à¤¾à¤®à¤¾à¤‡à¤¡ 2mg'),
        'Zinc Sulfate 20mg': ('à¦œà¦¿à¦™à§à¦• à¦¸à¦¾à¦²à¦«à§‡à¦Ÿ à§¨à§¦à¦®à¦¿à¦—à§à¦°à¦¾', 'à¤œà¤¿à¤‚à¤• à¤¸à¤²à¥à¤«à¥‡à¤Ÿ 20mg'),
        'Calamine Lotion': ('à¦•à§à¦¯à¦¾à¦²à¦¾à¦®à¦¾à¦‡à¦¨ à¦²à§‹à¦¶à¦¨', 'à¤•à¥ˆà¤²à¤¾à¤®à¤¾à¤‡à¤¨ à¤²à¥‹à¤¶à¤¨'),
        'Hydrocortisone 1% Cream': ('à¦¹à¦¾à¦‡à¦¡à§à¦°à§‹à¦•à¦°à§à¦Ÿà¦¿à¦¸à§‹à¦¨ à§§% à¦•à§à¦°à¦¿à¦®', 'à¤¹à¤¾à¤‡à¤¡à¥à¤°à¥‹à¤•à¤¾à¤°à¥à¤Ÿà¤¿à¤¸à¥‹à¤¨ 1% à¤•à¥à¤°à¥€à¤®'),
        'Sodium Chloride Eye Drops': ('à¦¸à§à¦¯à¦¾à¦²à¦¾à¦‡à¦¨ à¦†à¦‡ à¦¡à§à¦°à¦ª', 'à¤¸à¥‡à¤²à¤¾à¤‡à¤¨ à¤†à¤ˆ à¤¡à¥à¤°à¥‰à¤ª'),
        'Chloramphenicol Eye Drops': ('à¦•à§à¦²à§‹à¦°à¦¾à¦®à¦«à§‡à¦¨à¦¿à¦•à¦² à¦†à¦‡ à¦¡à§à¦°à¦ª', 'à¤•à¥à¤²à¥‹à¤°à¥ˆà¤®à¥à¤«à¥‡à¤¨à¤¿à¤•à¥‰à¤² à¤†à¤ˆ à¤¡à¥à¤°à¥‰à¤ª'),
        'Otocain Ear Drops': ('à¦…à¦Ÿà§‹à¦•à§‡à¦¨ à¦‡à¦¯à¦¼à¦¾à¦° à¦¡à§à¦°à¦ª', 'à¤“à¤Ÿà¥‹à¤•à¥‡à¤¨ à¤ˆà¤¯à¤° à¤¡à¥à¤°à¥‰à¤ª'),
        'Salbutamol Inhaler': ('à¦¸à¦¾à¦²à¦¬à¦¿à¦‰à¦Ÿà¦¾à¦®à¦² à¦‡à¦¨à¦¹à§‡à¦²à¦¾à¦°', 'à¤¸à¤¾à¤²à¤¬à¥à¤Ÿà¤¾à¤®à¥‹à¤² à¤‡à¤¨à¥à¤¹à¥‡à¤²à¤°'),
        'Ibuprofen 400mg': ('à¦†à¦‡à¦¬à§à¦ªà§à¦°à§‹à¦«à§‡à¦¨ à§ªà§¦à§¦à¦®à¦¿à¦—à§à¦°à¦¾', 'à¤‡à¤¬à¥à¤ªà¥à¤°à¥‹à¤«à¥‡à¤¨ 400mg'),
        'Potassium Citrate Sachets': ('à¦ªà¦Ÿà¦¾à¦¸à¦¿à¦¯à¦¼à¦¾à¦® à¦¸à¦¿à¦Ÿà§à¦°à§‡à¦Ÿ à¦¸à§à¦¯à¦¾à¦¸à§‡', 'à¤ªà¥‹à¤Ÿà¥‡à¤¶à¤¿à¤¯à¤® à¤¸à¤¾à¤‡à¤Ÿà¥à¤°à¥‡à¤Ÿ à¤ªà¤¾à¤‰à¤š'),
        'Cranberry Extract Tablet': ('à¦•à§à¦°à§à¦¯à¦¾à¦¨à¦¬à§‡à¦°à¦¿ à¦¸à¦¾à¦°à¦¾à¦‚à¦¶à§‡à¦° à¦Ÿà§à¦¯à¦¾à¦¬à¦²à§‡à¦Ÿ', 'à¤•à¥à¤°à¥ˆà¤¨à¤¬à¥‡à¤°à¥€ à¤…à¤°à¥à¤• à¤Ÿà¥ˆà¤¬à¤²à¥‡à¤Ÿ'),
        'Clotrimazole Cream': ('à¦•à§à¦²à§‹à¦Ÿà§à¦°à¦¾à¦‡à¦®à¦¾à¦œà§‹à¦² à¦•à§à¦°à¦¿à¦®', 'à¤•à¥à¤²à¥‹à¤Ÿà¥à¤°à¤¿à¤®à¥‡à¤œà¤¼à¥‹à¤² à¤•à¥à¤°à¥€à¤®'),
        'Betadine Ointment': ('à¦¬à¦¿à¦Ÿà¦¾à¦¦à¦¿à¦¨ à¦®à¦²à¦®', 'à¤¬à¥€à¤Ÿà¤¾à¤¡à¥€à¤¨ à¤®à¤²à¤¹à¤®'),
        'Povidone Iodine Gargle': ('à¦ªà§‹à¦­à¦¿à¦¡à§‹à¦¨ à¦†à¦¯à¦¼à§‹à¦¡à¦¿à¦¨ à¦—à¦¾à¦°à§à¦—à¦²', 'à¤ªà¥‹à¤µà¤¿à¤¡à¥‹à¤¨ à¤†à¤¯à¥‹à¤¡à¥€à¤¨ à¤—à¤°à¤¾à¤°à¥‡'),
        'Strepsils': ('à¦¸à§à¦Ÿà§à¦°à§‡à¦ªà¦¸à¦¿à¦²à¦¸', 'à¤¸à¥à¤Ÿà¥à¤°à¥‡à¤ªà¥à¤¸à¤¿à¤²à¥à¤¸'),
        'Iron + Folic Acid Tablets': ('à¦†à¦¯à¦¼à¦°à¦¨ + à¦«à¦²à¦¿à¦• à¦…à§à¦¯à¦¾à¦¸à¦¿à¦¡ à¦Ÿà§à¦¯à¦¾à¦¬à¦²à§‡à¦Ÿ', 'à¤†à¤¯à¤°à¤¨ + à¤«à¥‹à¤²à¤¿à¤• à¤à¤¸à¤¿à¤¡ à¤Ÿà¥ˆà¤¬à¤²à¥‡à¤Ÿ'),
    }

    cursor.execute("SELECT condition_id, name_en FROM conditions")
    cond_rows = cursor.fetchall()
    new_med_ids = []

    for row in cond_rows:
        normalized_name = normalize_condition_name(row['name_en'])
        matched_key = medicine_aliases.get(normalized_name, normalized_name)

        if matched_key not in medicine_map:
            for key in medicine_map.keys():
                if key in normalized_name or normalized_name in key:
                    matched_key = key
                    break

        meds = medicine_map.get(matched_key)
        if not meds:
            continue

        for medicine_name in meds:
            name_bn, name_hi = medicine_translations.get(medicine_name, (medicine_name, medicine_name))
            cursor.execute(
                """
                    INSERT INTO medicines (condition_id, name_en, name_bn, name_hi, otc_available)
                    VALUES (?, ?, ?, ?, 1)
                """,
                (row['condition_id'], medicine_name, name_bn, name_hi),
            )
            new_med_ids.append(cursor.lastrowid)

    cursor.execute("SELECT facility_id FROM facilities WHERE type IN ('Jan Aushadhi', 'Pharmacy')")
    pharma_facs = [r['facility_id'] for r in cursor.fetchall()]

    for fac_id in pharma_facs:
        for med_id in new_med_ids:
            cursor.execute(
                "INSERT OR IGNORE INTO facility_medicines (facility_id, medicine_id) VALUES (?, ?)",
                (fac_id, med_id),
            )

