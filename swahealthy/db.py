import sqlite3
import json
import math
import os

DB_PATH = 'swahealthy.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def upsert_user(user_info):
    conn = get_db_connection()
    cursor = conn.cursor()
    google_id = user_info.get('sub')
    name = user_info.get('name')
    email = user_info.get('email')
    profile_pic = user_info.get('picture')

    cursor.execute("SELECT * FROM users WHERE google_id = ?", (google_id,))
    user = cursor.fetchone()

    if user:
        cursor.execute('''
            UPDATE users
            SET name = ?, email = ?, profile_pic = ?
            WHERE google_id = ?
        ''', (name, email, profile_pic, google_id))
        user_id = user['user_id']
    else:
        cursor.execute('''
            INSERT INTO users (google_id, name, email, profile_pic)
            VALUES (?, ?, ?, ?)
        ''', (google_id, name, email, profile_pic))
        user_id = cursor.lastrowid
        
    conn.commit()
    conn.close()

    return {
        'user_id': user_id,
        'google_id': google_id,
        'name': name,
        'email': email,
        'profile_pic': profile_pic
    }

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0 # Earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Tables
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
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS session_log(
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
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

    # Medicines table: OTC medicines linked to conditions
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

    # Junction table: which facility stocks which medicine
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS facility_medicines(
            facility_id INTEGER NOT NULL,
            medicine_id INTEGER NOT NULL,
            FOREIGN KEY (facility_id) REFERENCES facilities(facility_id),
            FOREIGN KEY (medicine_id) REFERENCES medicines(medicine_id),
            PRIMARY KEY (facility_id, medicine_id)
        )
    ''')
    
    # Check if empty
    cursor.execute('SELECT COUNT(*) FROM symptoms')
    if cursor.fetchone()[0] == 0:
        seed_data(cursor)

    # Check if doctors are empty
    cursor.execute('SELECT COUNT(*) FROM doctors')
    if cursor.fetchone()[0] == 0:
        seed_doctors(cursor)

    # Check if medicines are empty
    cursor.execute('SELECT COUNT(*) FROM medicines')
    if cursor.fetchone()[0] == 0:
        seed_medicines(cursor)

    # === MIGRATIONS: safely add columns/tables added after initial DB creation ===
    # Add users table if it doesn't exist (migration for old DBs)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            google_id TEXT UNIQUE,
            name TEXT,
            email TEXT,
            profile_pic TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Add user_id column to session_log if missing (idempotent migration)
    cursor.execute("PRAGMA table_info(session_log)")
    columns = [row[1] for row in cursor.fetchall()]
    if 'user_id' not in columns:
        cursor.execute("ALTER TABLE session_log ADD COLUMN user_id INTEGER REFERENCES users(user_id)")
        print("[MIGRATION] Added user_id column to session_log")
        
    conn.commit()
    conn.close()

def seed_data(cursor):
    # 40 Symptoms
    symptoms = [
        # Head (8)
        ("Fever", "জ্বর", "बुखार", "head"),
        ("Headache", "মাথাব্যথা", "सिरदर्द", "head"),
        ("Dizziness", "মাথা ঘোরা", "चक्कर आना", "head"),
        ("Eye redness", "চোখ লাল হওয়া", "आँखें लाल होना", "head"),
        ("Blurred vision", "ঝাপসা দৃষ্টি", "धुंधली दृष्टि", "head"),
        ("Runny nose", "নাক দিয়ে জল পড়া", "बहती नाक", "head"),
        ("Sore throat", "গলা ব্যথা", "गले में खराश", "head"),
        ("Earache", "কান ব্যথা", "कान दर्द", "head"),
        # Chest (6)
        ("Cough", "কাশি", "खांसी", "chest"),
        ("Chest pain", "বুকের ব্যথা", "छाती में दर्द", "chest"),
        ("Shortness of breath", "শ্বাসকষ্ট", "सांस की तकलीफ", "chest"),
        ("Rapid heartbeat", "দ্রুত হৃদস্পন্দন", "तेज़ धड़कन", "chest"),
        ("Wheezing", "সাঁ সাঁ শব্দ", "घरघराहट", "chest"),
        ("Palpitations", "বুক ধড়ফড়", "घबराहट", "chest"),
        # Stomach (8)
        ("Nausea", "বমি ভাব", "मतली", "stomach"),
        ("Vomiting", "বমি", "उल्टी", "stomach"),
        ("Diarrhoea", "ডায়রিয়া", "दस्त", "stomach"),
        ("Stomach pain", "পেটের ব্যথা", "पेट दर्द", "stomach"),
        ("Bloating", "পেট ফাঁপা", "पेट फूलना", "stomach"),
        ("Loss of appetite", "ক্ষুধামন্দা", "भूख ना लगना", "stomach"),
        ("Constipation", "কোষ্ঠকাঠিন্য", "कब्ज", "stomach"),
        ("Blood in stool", "মলে রক্ত", "मल में रक्त", "stomach"),
        # General (9)
        ("Fatigue", "ক্লান্তি", "थकान", "general"),
        ("Body ache", "গায়ে ব্যথা", "बदन दर्द", "general"),
        ("Chills", "ঠাণ্ডা লাগা", "ठंड लगना", "general"),
        ("Sweating", "ঘাম", "पसीना आना", "general"),
        ("Weight loss", "ওজন কমা", "वजन कम होना", "general"),
        ("Swollen lymph nodes", "ফোলা লসিকা গ্রন্থি", "सूजी हुई लिम्फ नोड्स", "general"),
        ("High temperature", "উচ্চ তাপমাত্রা", "अधिक तापमान", "general"),
        ("Sneezing", "হাঁচি", "छींकना", "general"),
        ("Loss of smell", "গন্ধ না পাওয়া", "सूंघने की क्षमता में कमी", "general"),
        # Skin (9)
        ("Rash", "র‍্যাশ", "चकत्ते", "skin"),
        ("Itching", "চুলকানি", "खुजली", "skin"),
        ("Yellowing skin", "ত্বক হলুদ হওয়া", "त्वचा का पीला पड़ना", "skin"),
        ("Pale skin", "ফ্যাকাশে ত্বক", "पीली त्वचा", "skin"),
        ("Dry skin", "শুষ্ক ত্বক", "रूखी त्वचा", "skin"),
        ("Swelling", "ফোলা", "सूजन", "skin"),
        ("Bruising", "শিরা ফুলে যাওয়া", "चोट", "skin"),
        ("Skin peeling", "ত্বক ওঠা", "त्वचा छिलना", "skin"),
        ("Blisters", "ফোস্কা", "छाले", "skin")
    ]
    
    for s in symptoms:
        cursor.execute("INSERT INTO symptoms (name_en, name_bn, name_hi, body_area) VALUES (?, ?, ?, ?)", s)

    # 20 Conditions
    conditions = [
        ("Common Cold", "সাধারণ সর্দি", "सामान्य जुकाम", "low", 
         "Rest and drink plenty of fluids.\nTake over-the-counter cold medications.\nGargle with warm salt water for sore throat.",
         "বিশ্রাম নিন এবং প্রচুর তরল পান করুন।\nগরম জলে গার্গল করুন।",
         "आराम करें और बहुत सारा तरल पदार्थ पिएं।\nगर्म पानी से गरारे करें।",
         0, None),
        ("Influenza", "ফ্লু", "इन्फ्लूएंजा", "medium",
         "Drink clear fluids to prevent dehydration.\nRest in bed and take antipyretics for fever.\nMonitor breathing.",
         "বিশ্রাম নিন এবং জ্বর কমানোর ওষুধ খান।",
         "आराम करें और बुखार कम करने वाली दवाएं लें।",
         1, None),
        ("Dengue Risk", "ডেঙ্গুর ঝুঁকি", "डेंगू का जोखिम", "high",
         "Drink oral rehydration salts (ORS).\nAvoid NSAIDs like ibuprofen, use paracetamol instead.\nVisit a doctor immediately.",
         "প্যারাসিটামল ব্যবহার করুন এবং দ্রুত ডাক্তার দেখান।",
         "पैरासिटामोल का उपयोग करें और तुरंत डॉक्टर से मिलें।",
         1, "Seek immediate medical attention to check platelet count!"),
        ("Malaria Risk", "ম্যালেরিয়ার ঝুঁকি", "मलेरिया का जोखिम", "high",
         "Take prescribed antimalarial drugs.\nRest and manage fever.\nSeek medical diagnosis via blood test.",
         "রক্ত পরীক্ষা করে ডাক্তারের পরামর্শ নিন।",
         "रक्त परीक्षण कर डॉक्टर से सलाह लें।",
         1, "Malaria can be fatal without prompt treatment!"),
        ("Dehydration", "ডিহাইড্রেশন", "निर्जलीकरण", "medium",
         "Drink ORS or electrolyte solutions.\nAvoid caffeine and alcohol.\nRest in a cool place.",
         "ওআরএস বা স্যালাইন পান করুন।",
         "ओआरएस (ORS) या इलेक्ट्रोलाइट पिएं।",
         1, None),
        ("Food Poisoning", "খাদ্যে বিষক্রিয়া", "भोजन विषाक्तता", "medium",
         "Stay hydrated with small sips of water.\nAvoid solid food until vomiting stops.\nEat bland food initially.",
         "বমি বন্ধ না হওয়া পর্যন্ত কঠিন খাবার এড়িয়ে চলুন।",
         "उल्टी रुकने तक ठोस भोजन से बचें।",
         1, None),
        ("Typhoid Risk", "টাইফয়েডের ঝুঁকি", "टाइफाइड का जोखिम", "high",
         "Drink boiled or purified water.\nEat easily digestible food.\nUndergo a blood culture test.",
         "সেদ্ধ করা জল পান করুন এবং ডাক্তারের কাছে যান।",
         "उबला हुआ पानी पिएं और डॉक्टर से मिलें।",
         1, "Antibiotics are required; consult a doctor immediately!"),
        ("Migraine", "মাইগ্রেন", "माइग्रेन", "low",
         "Rest in a quiet, dark room.\nApply hot or cold compresses to your head.\nTake prescribed medication.",
         "অন্ধকার ঘরে বিশ্রাম নিন।",
         "एक शांत, अंधेरे कमरे में आराम करें।",
         0, None),
        ("Tension Headache", "টেনশন মাথাব্যথা", "तनाव सिरदर्द", "low",
         "Relax and rest.\nTake an OTC pain reliever.\nMassage your neck and shoulders.",
         "বিশ্রাম নিন এবং ঘাড় মাসাজ করুন।",
         "आराम करें और गर्दन की मालिश करें।",
         0, None),
        ("Conjunctivitis", "কনজাঙ্কটিভাইটিস (চোখ ওঠা)", "कंजंक्टिवाइटिस", "low",
         "Apply a cold compress to your eyes.\nWash your hands frequently.\nDo not rub your eyes.",
         "চোখে ঠান্ডা জল দিন এবং হাত ধোবেন ঘন ঘন।",
         "आंखों पर ठंडी सिकाई करें और बार-बार हाथ धोएं।",
         1, None),
        ("Chest Infection", "বুকের সংক্রমণ", "छाती में संक्रमण", "medium",
         "Use a humidifier.\nSit upright to breathe easily.\nTake prescribed antibiotics if bacterial.",
         "হিউমিডিফায়ার ব্যবহার করুন এবং সোজা হয়ে বসুন।",
         "ह्यूमिडिफायर का उपयोग करें और सीधे बैठें।",
         1, None),
        ("Asthma Attack", "হাঁপানি আক্রমণ", "अस्थमा का दौरा", "high",
         "Use a rescue inhaler immediately.\nSit upright and remain calm.\nIf breathing does not improve, seek help.",
         "অবিলম্বে ইনহেলার ব্যবহার করুন।",
         "तुरंत इन्हेलर का इस्तेमाल करें।",
         1, "Call emergency services if breathing does not normalize!"),
        ("Urinary Tract Infection", "ইউটিআই (মূত্রনালীর সংক্রমণ)", "मूत्र पथ संक्रमण", "medium",
         "Drink plenty of water to flush bacteria.\nDo not hold urine.\nConsult a doctor for antibiotics.",
         "প্রচুর জল পান করুন এবং ডাক্তার দেখান।",
         "खूब पानी पिएं और डॉक्टर से मिलें।",
         1, None),
        ("Jaundice Risk", "জন্ডিসের ঝুঁকি", "पीलिया का जोखिम", "high",
         "Eat a light and healthy diet.\nAvoid alcohol and oily food.\nSeek a liver function test.",
         "হালকা খাবার খান এবং লিভার পরীক্ষা করান।",
         "हल्का भोजन करें और लिवर फंक्शन टेस्ट कराएं।",
         1, "Potential liver inflammation; clinical diagnosis needed!"),
        ("Anaemia", "রক্তাল্পতা", "एनीमिया", "medium",
         "Eat iron-rich foods (spinach, red meat).\nTake iron supplements after consulting a doctor.\nInclude vitamin C in your diet.",
         "আয়রন যুক্ত খাবার খান।",
         "आयरन युक्त भोजन खाएं।",
         1, None),
        ("Skin Allergy", "ত্বকের অ্যালার্জি", "त्वचा की एलर्जी", "low",
         "Wash the area with cool water.\nApply an antihistamine cream.\nAvoid triggering allergens.",
         "অ্যালার্জির স্থানে ঠান্ডা জল লাগান।",
         "एलर्जी वाली जगह ठंडे पानी से धोएं।",
         0, None),
        ("Gastroenteritis", "গ্যাস্ট্রোএন্টেরাইটিস", "गैस्ट्रोएंटेराइटिस", "medium",
         "Drink plenty of liquids.\nSlowly introduce bland foods (BRAT diet).\nRest well.",
         "প্রচুর তরল পান করুন এবং বিশ্রাম নিন।",
         "हाइड्रेटेड रहें और आराम करें।",
         1, None),
        ("Hypertension Risk", "উচ্চ রক্তচাপ ঝুঁকি", "उच्च रक्तचाप जोखिम", "medium",
         "Reduce salt intake.\nAvoid stress and rest quietly.\nMonitor blood pressure regularly.",
         "লবণ খাওয়া কমান এবং মানসিক চাপ এড়ান।",
         "नमक कम खाएं और तनाव से बचें।",
         1, None),
        ("Heat Stroke", "হিট স্ট্রোক", "लू लगना (हीट स्ट्रोक)", "high",
         "Move to a cool area immediately.\nCool the body with cold water or ice packs.\nDrink fluids without ice.",
         "ঠান্ডা জায়গায় যান এবং শরীর ঠান্ডা করুন।",
         "ठंडी जगह पर जाएं और शरीर पर ठंडा पानी डालें।",
         1, "Medical emergency! Rapidly cool the body and go to a hospital!"),
        ("Chickenpox Risk", "জলবসন্ত ঝুঁকি", "चेचक (चिकनपॉक्स) जोखिम", "medium",
         "Isolate to prevent spreading.\nUse calamine lotion for itching.\nAvoid scratching blisters.",
         "সংক্রমণ এড়াতে আলাদা থাকুন।",
         "फैलने से रोकने के लिए अलग रहें।",
         1, None),
    ]
    
    for c in conditions:
        cursor.execute("""
            INSERT INTO conditions (
                name_en, name_bn, name_hi, severity, 
                first_aid_en, first_aid_bn, first_aid_hi, 
                see_doctor, emergency_note
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, c)

    # Simplified condition_symptoms: Randomised linkage for logic testing
    # First, get all symptoms and conditions by names
    cursor.execute("SELECT condition_id, name_en FROM conditions")
    cond_map = {row['name_en']: row['condition_id'] for row in cursor.fetchall()}
    
    cursor.execute("SELECT symptom_id, name_en FROM symptoms")
    symp_map = {row['name_en']: row['symptom_id'] for row in cursor.fetchall()}

    # Define standard linkage
    linkages = [
        ("Common Cold", ["Runny nose", "Sneezing", "Sore throat", "Cough", "Fever"]),
        ("Influenza", ["Fever", "Fatigue", "Body ache", "Cough", "Chills", "Headache"]),
        ("Dengue Risk", ["Fever", "Headache", "Body ache", "Fatigue", "Rash", "Eye redness"]),
        ("Malaria Risk", ["Fever", "Chills", "Sweating", "Fatigue", "Headache", "Body ache"]),
        ("Dehydration", ["Dizziness", "Fatigue", "Headache", "Dry skin"]),
        ("Food Poisoning", ["Nausea", "Vomiting", "Diarrhoea", "Stomach pain", "Fever"]),
        ("Typhoid Risk", ["Fever", "Fatigue", "Stomach pain", "Headache", "Loss of appetite"]),
        ("Migraine", ["Headache", "Nausea", "Blurred vision", "Dizziness"]),
        ("Tension Headache", ["Headache", "Fatigue"]),
        ("Conjunctivitis", ["Eye redness", "Itching", "Blurred vision"]),
        ("Chest Infection", ["Cough", "Chest pain", "Fever", "Shortness of breath", "Wheezing"]),
        ("Asthma Attack", ["Shortness of breath", "Wheezing", "Chest pain", "Rapid heartbeat"]),
        ("Urinary Tract Infection", ["Fever", "Frequent urination", "Painful urination", "Blood in urine"]), # Assuming closest symptoms mapped
        ("Jaundice Risk", ["Yellowing skin", "Fatigue", "Nausea", "Weight loss"]),
        ("Anaemia", ["Fatigue", "Pale skin", "Dizziness", "Shortness of breath"]),
        ("Skin Allergy", ["Rash", "Itching", "Swelling", "Dry skin"]),
        ("Gastroenteritis", ["Diarrhoea", "Vomiting", "Stomach pain", "Nausea"]),
        ("Hypertension Risk", ["Headache", "Dizziness", "Blurred vision", "Shortness of breath"]),
        ("Heat Stroke", ["High temperature", "Dizziness", "Headache", "Nausea", "Rapid heartbeat"]),
        ("Chickenpox Risk", ["Rash", "Fever", "Itching", "Blisters"])
    ]

    for c_name, s_names in linkages:
        c_id = cond_map.get(c_name)
        if not c_id: continue
        
        for idx, s_name in enumerate(s_names):
            s_id = symp_map.get(s_name)
            if s_id:
                is_req = 1 if idx == 0 else 0  # First mapped symptom is required
                weight = 3 if is_req else 1
                cursor.execute("""
                    INSERT INTO condition_symptoms (condition_id, symptom_id, is_required, weight)
                    VALUES (?, ?, ?, ?)
                """, (c_id, s_id, is_req, weight))

    # 10 Facilities
    facilities = [
        ("Kolkata Medical College", "Hospital", "Kolkata", 22.5735, 88.3629, "+91 33 2212 3000"),
        ("NRS Medical College", "Hospital", "Kolkata", 22.5645, 88.3683, "+91 33 2286 0033"),
        ("SSKM Hospital", "Hospital", "Kolkata", 22.5395, 88.3444, "+91 33 2204 1100"),
        ("Howrah District Hospital", "Hospital", "Howrah", 22.5800, 88.3299, "+91 33 2641 3400"),
        ("Salt Lake SD Hospital", "Hospital", "North 24 Parganas", 22.5866, 88.4116, "+91 33 2321 2323"),
        ("Barasat District Hospital", "Hospital", "North 24 Parganas", 22.7214, 88.4735, "+91 33 2552 2011"),
        ("Dum Dum Municipal Hospital", "Hospital", "North 24 Parganas", 22.6241, 88.4187, "+91 33 2551 3241"),
        ("Jan Aushadhi Kendra (Sealdah)", "Jan Aushadhi", "Kolkata", 22.5694, 88.3713, "N/A"),
        ("Bidhannagar State General Hospital", "PHC", "North 24 Parganas", 22.5937, 88.4206, "N/A"),
        ("Bardhaman Medical College", "Hospital", "Bardhaman", 23.2393, 87.8512, "N/A"),
    ]
    
    for f in facilities:
        cursor.execute("INSERT INTO facilities (name, type, district, latitude, longitude, contact) VALUES (?, ?, ?, ?, ?, ?)", f)

def seed_doctors(cursor):
    """Seed sample West Bengal doctors."""
    doctors = [
        ("Dr. Arindam Mukherjee", "Cardiologist", json.dumps(["Mon", "Wed", "Fri"]), json.dumps(["10:00", "11:00", "16:00", "17:00"]), "+91 98300 12345", "en"),
        ("Dr. Shampa Chatterjee", "General Physician", json.dumps(["Tue", "Thu", "Sat"]), json.dumps(["09:00", "10:30", "14:00", "15:30"]), "+91 98310 23456", "bn"),
        ("Dr. Rajesh Gupta", "Pediatrician", json.dumps(["Mon", "Tue", "Thu"]), json.dumps(["11:00", "12:00", "18:00", "19:00"]), "+91 98360 34567", "hi"),
        ("Dr. Ananya Das", "Dermatologist", json.dumps(["Wed", "Fri", "Sat"]), json.dumps(["10:00", "11:30", "16:30", "18:00"]), "+91 98320 45678", "en"),
        ("Dr. Somenath Banerjee", "Neurologist", json.dumps(["Mon", "Wed", "Sat"]), json.dumps(["12:00", "13:00", "17:00", "18:30"]), "+91 98330 56789", "bn")
    ]
    
    for d in doctors:
        cursor.execute("""
            INSERT INTO doctors (name, specialisation, available_days_json, slots_json, contact, language)
            VALUES (?, ?, ?, ?, ?, ?)
        """, d)

def seed_medicines(cursor):
    """Seed common OTC medicines for each condition and link to Jan Aushadhi facilities."""
    # Build condition lookup
    cursor.execute("SELECT condition_id, name_en FROM conditions")
    cond_map = {row['name_en']: row['condition_id'] for row in cursor.fetchall()}

    # (condition_name, name_en, name_bn, name_hi, otc_available)
    medicines = [
        # Common Cold
        ("Common Cold", "Cetirizine", "সেটিরিজিন", "सेटिरिज़ीन", 1),
        ("Common Cold", "Paracetamol", "প্যারাসিটামল", "पैरासिटामोल", 1),
        ("Common Cold", "Cough Syrup (Dextromethorphan)", "কাফ সিরাপ", "कफ सिरप", 1),
        # Influenza
        ("Influenza", "Paracetamol", "প্যারাসিটামল", "पैरासिटामोल", 1),
        ("Influenza", "Ibuprofen", "আইবুপ্রোফেন", "इबुप्रोफेन", 1),
        # Dengue Risk
        ("Dengue Risk", "Paracetamol", "প্যারাসিটামল", "पैरासिटामोल", 1),
        ("Dengue Risk", "ORS (Oral Rehydration Salts)", "ওআরএস", "ओआरएस", 1),
        # Malaria Risk
        ("Malaria Risk", "Paracetamol", "প্যারাসিটামল", "पैरासिटामोल", 1),
        # Dehydration
        ("Dehydration", "ORS (Oral Rehydration Salts)", "ওআরএস", "ओआरएस", 1),
        ("Dehydration", "Electrolyte Powder", "ইলেক্ট্রোলাইট পাউডার", "इलेक्ट्रोलाइट पाउडर", 1),
        # Food Poisoning
        ("Food Poisoning", "ORS (Oral Rehydration Salts)", "ওআরএস", "ओआरएस", 1),
        ("Food Poisoning", "Domperidone", "ডমপেরিডন", "डोम्पेरिडोन", 1),
        # Typhoid Risk
        ("Typhoid Risk", "Paracetamol", "প্যারাসিটামল", "पैरासिटामोल", 1),
        ("Typhoid Risk", "ORS (Oral Rehydration Salts)", "ওআরএস", "ओआरएस", 1),
        # Migraine
        ("Migraine", "Paracetamol", "প্যারাসিটামল", "पैरासिटामोल", 1),
        ("Migraine", "Ibuprofen", "আইবুপ্রোফেন", "इबुप्रोफेन", 1),
        # Tension Headache
        ("Tension Headache", "Paracetamol", "প্যারাসিটামল", "पैरासिटामोल", 1),
        ("Tension Headache", "Aspirin", "অ্যাসপিরিন", "एस्पिरिन", 1),
        # Conjunctivitis
        ("Conjunctivitis", "Antihistamine Eye Drops", "অ্যান্টিহিস্টামাইন আই ড্রপ", "एंटीहिस्टामाइन आई ड्रॉप", 1),
        # Chest Infection
        ("Chest Infection", "Paracetamol", "প্যারাসিটামল", "पैरासिटामोल", 1),
        ("Chest Infection", "Cough Syrup (Dextromethorphan)", "কাফ সিরাপ", "कफ सिरप", 1),
        # Asthma Attack
        ("Asthma Attack", "Salbutamol Inhaler", "সালবিউটামল ইনহেলার", "सालबुटामोल इन्हेलर", 1),
        # Urinary Tract Infection
        ("Urinary Tract Infection", "Cranberry Extract Tablets", "ক্র্যানবেরি ট্যাবলেট", "क्रैनबेरी टैबलेट", 1),
        # Jaundice Risk
        ("Jaundice Risk", "Multivitamin", "মাল্টিভিটামিন", "मल्टीविटामिन", 1),
        # Anaemia
        ("Anaemia", "Iron Tablets (Ferrous Sulphate)", "আয়রন ট্যাবলেট", "आयरन टैबलेट", 1),
        ("Anaemia", "Folic Acid", "ফলিক অ্যাসিড", "फोलिक एसिड", 1),
        # Skin Allergy
        ("Skin Allergy", "Cetirizine", "সেটিরিজিন", "सेटिरिज़ीन", 1),
        ("Skin Allergy", "Calamine Lotion", "ক্যালামাইন লোশন", "कैलामाइन लोशन", 1),
        # Gastroenteritis
        ("Gastroenteritis", "ORS (Oral Rehydration Salts)", "ওআরএস", "ओआरएस", 1),
        ("Gastroenteritis", "Zinc Tablets", "জিঙ্ক ট্যাবলেট", "ज़िंक टैबलेट", 1),
        # Hypertension Risk
        ("Hypertension Risk", "Low-dose Aspirin", "লো-ডোজ অ্যাসপিরিন", "लो-डोज़ एस्पिरिन", 1),
        # Heat Stroke
        ("Heat Stroke", "ORS (Oral Rehydration Salts)", "ওআরএস", "ओআरएस", 1),
        ("Heat Stroke", "Electrolyte Powder", "ইলেক্ট্রোলাইট পাউডার", "इलेक्ट्रोलाइट पाउडर", 1),
        # Chickenpox Risk
        ("Chickenpox Risk", "Calamine Lotion", "ক্যালামাইন লোশন", "कैलामाइन लोशन", 1),
        ("Chickenpox Risk", "Paracetamol", "প্যারাসিটামল", "पैरासिटामोल", 1),
    ]

    med_ids = []  # Track (condition_name, medicine_id) for facility linking
    for cond_name, name_en, name_bn, name_hi, otc in medicines:
        c_id = cond_map.get(cond_name)
        if not c_id:
            continue
        cursor.execute("""
            INSERT INTO medicines (condition_id, name_en, name_bn, name_hi, otc_available)
            VALUES (?, ?, ?, ?, ?)
        """, (c_id, name_en, name_bn, name_hi, otc))
        med_ids.append(cursor.lastrowid)

    # Get Jan Aushadhi / pharmacy facilities to link medicines
    cursor.execute("SELECT facility_id FROM facilities WHERE type IN ('Jan Aushadhi', 'Pharmacy')")
    pharma_facilities = [row['facility_id'] for row in cursor.fetchall()]

    # If no Jan Aushadhi facilities exist, add a few more for realistic data
    if len(pharma_facilities) < 2:
        extra_pharma = [
            ("Jan Aushadhi Kendra (Salt Lake)", "Jan Aushadhi", "North 24 Parganas", 22.5870, 88.4130, "N/A"),
            ("Jan Aushadhi Kendra (Howrah)", "Jan Aushadhi", "Howrah", 22.5810, 88.3280, "N/A"),
            ("Jan Aushadhi Kendra (Dum Dum)", "Jan Aushadhi", "North 24 Parganas", 22.6250, 88.4200, "N/A"),
        ]
        for f in extra_pharma:
            cursor.execute("INSERT INTO facilities (name, type, district, latitude, longitude, contact) VALUES (?, ?, ?, ?, ?, ?)", f)
            pharma_facilities.append(cursor.lastrowid)

    # Link all medicines to all Jan Aushadhi facilities
    for fac_id in pharma_facilities:
        for med_id in med_ids:
            cursor.execute("INSERT OR IGNORE INTO facility_medicines (facility_id, medicine_id) VALUES (?, ?)", (fac_id, med_id))
