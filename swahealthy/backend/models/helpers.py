"""
Database helper utilities.
"""

import math
import sqlite3

from config import Config


def get_db_connection():
    """Open a connection to the SQLite database."""
    conn = sqlite3.connect(Config.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def haversine(lat1, lon1, lat2, lon2):
    """Calculate the great-circle distance (km) between two coordinates."""
    R = 6371.0  # Earth radius in kilometres
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def upsert_user(user_info):
    """Insert or update a Google-authenticated user and return their data."""
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
        age = user['age']
        gender = user['gender']
    else:
        cursor.execute('''
            INSERT INTO users (google_id, name, email, profile_pic)
            VALUES (?, ?, ?, ?)
        ''', (google_id, name, email, profile_pic))
        user_id = cursor.lastrowid
        age = None
        gender = None

    conn.commit()
    conn.close()

    return {
        'user_id': user_id,
        'google_id': google_id,
        'name': name,
        'email': email,
        'profile_pic': profile_pic,
        'age': age,
        'gender': gender,
    }


def get_log_by_id(log_id):
    """Fetch a single session log by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM session_log WHERE log_id = ?", (log_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_symptoms_by_ids(symptom_ids, lang='en'):
    """Fetch symptom names by a list of IDs for a specific language."""
    if not symptom_ids:
        return []
    
    name_col = f'name_{lang}' if lang in ('en', 'bn', 'hi') else 'name_en'
    placeholders = ','.join('?' * len(symptom_ids))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT {name_col} as name FROM symptoms WHERE symptom_id IN ({placeholders})", symptom_ids)
    rows = cursor.fetchall()
    conn.close()
    
    return [row['name'] for row in rows]


def get_condition_by_name(name_en, lang='en'):
    """Fetch condition details by any localized condition name."""
    if not name_en:
        return None

    name_col = f'name_{lang}' if lang in ('en', 'bn', 'hi') else 'name_en'
    first_aid_col = f'first_aid_{lang}' if lang in ('en', 'bn', 'hi') else 'first_aid_en'
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT 
            condition_id, 
            {name_col} as translated_name, 
            severity, 
            {first_aid_col} as first_aid_text, 
            see_doctor, 
            emergency_note 
        FROM conditions 
        WHERE name_en = ? OR name_bn = ? OR name_hi = ?
        LIMIT 1
    """, (name_en, name_en, name_en))
    row = cursor.fetchone()
    conn.close()
    
    return dict(row) if row else None
