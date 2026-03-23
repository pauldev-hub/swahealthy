"""
Diagnosis engine — rule-based symptom checker.
"""

from backend.models.helpers import get_db_connection


def diagnose(symptom_ids: list, language: str = 'en', duration: str = None, age: str = None, gender: str = None) -> dict:
    """
    Match user-selected symptoms against condition rules and return
    the best-matching condition with severity, first-aid steps, and alternates.
    """
    fallback = {
        "condition": "General illness",
        "severity": "medium",
        "first_aid": ["Rest and drink fluids.", "Consult a doctor if symptoms persist or worsen."],
        "see_doctor": True,
        "emergency_note": None,
        "alternates": [],
    }

    if not symptom_ids:
        return fallback

    conn = get_db_connection()
    cursor = conn.cursor()

    # Get all conditions and their symptom mappings
    cursor.execute('''
        SELECT c.*, cs.symptom_id, cs.is_required, cs.weight
        FROM conditions c
        JOIN condition_symptoms cs ON c.condition_id = cs.condition_id
    ''')

    rows = cursor.fetchall()

    # Score each condition
    cond_scores = {}
    cond_data = {}
    cond_required = {}

    for row in rows:
        c_id = row['condition_id']
        s_id = row['symptom_id']
        is_req = row['is_required']
        weight = row['weight']

        if c_id not in cond_data:
            cond_data[c_id] = dict(row)
            cond_scores[c_id] = 0
            cond_required[c_id] = False

        if s_id in symptom_ids:
            if is_req:
                cond_scores[c_id] += 3
                cond_required[c_id] = True
            else:
                cond_scores[c_id] += weight

    # Apply Gender-based score boost
    if gender == "Female":
        for c_id in cond_scores:
            c_name = cond_data[c_id]['name_en']
            if "Urinary" in c_name or "Anaemia" in c_name:
                cond_scores[c_id] += 2

    # Filter and sort
    results = []
    for c_id, score in cond_scores.items():
        if score > 0 and cond_required[c_id]:
            results.append((score, cond_data[c_id]))

    results.sort(key=lambda x: x[0], reverse=True)
    conn.close()

    if not results:
        # Relax: drop required-match constraint
        for c_id, score in cond_scores.items():
            if score > 0:
                results.append((score, cond_data[c_id]))
        results.sort(key=lambda x: x[0], reverse=True)
        if not results:
            # Final fallback: Fetch "General Illness" from DB to ensure it has a condition_id
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM conditions WHERE name_en = 'General Illness' LIMIT 1")
                gi_row = cursor.fetchone()
                conn.close()
                if gi_row:
                    gi_row = dict(gi_row)
                    name_key = f"name_{language}"
                    fa_key = f"first_aid_{language}"
                    response = {
                        "condition_id": gi_row['condition_id'],
                        "condition": gi_row.get(name_key) or gi_row['name_en'],
                        "severity": gi_row['severity'],
                        "first_aid": [s.strip() for s in (gi_row.get(fa_key) or gi_row['first_aid_en']).split('\n') if s.strip()],
                        "see_doctor": bool(gi_row['see_doctor']),
                        "emergency_note": gi_row['emergency_note'],
                        "alternates": [],
                    }
                    return response
            except:
                pass
            return fallback

    # Format response
    top_cond = results[0][1]

    name_key = f"name_{language}"
    fac_key = f"first_aid_{language}"

    cond_name = (
        top_cond[name_key]
        if name_key in top_cond and top_cond[name_key]
        else top_cond['name_en']
    )
    first_aid_text = (
        top_cond[fac_key]
        if fac_key in top_cond and top_cond[fac_key]
        else top_cond['first_aid_en']
    )

    first_aid_steps = [step.strip() for step in first_aid_text.split('\n') if step.strip()]

    response = {
        "condition_id": top_cond['condition_id'],
        "condition": cond_name,
        "severity": top_cond['severity'],
        "first_aid": first_aid_steps,
        "see_doctor": bool(top_cond['see_doctor']),
        "emergency_note": top_cond['emergency_note'],
        "alternates": [],
    }

    # Duration Logic adjustments
    if duration == "7+ days":
        if response['severity'] == 'low':
            response['severity'] = 'medium'
        elif response['severity'] == 'medium':
            response['severity'] = 'high'
    elif duration == "4-7 days":
        if response['severity'] == 'low' and not response['see_doctor']:
            response['see_doctor'] = True

    # Age Logic adjustments
    try:
        age_val = int(age) if age else None
    except:
        age_val = None

    if age_val:
        if age_val >= 60 and response['severity'] == 'low':
            response['see_doctor'] = True
        if age_val <= 12 and response['severity'] == 'medium':
            response['severity'] = 'high'

    response['duration_note'] = None
    if duration:
        response['duration_note'] = f"Duration: {duration} — consider seeing a doctor if symptoms persist."

    for score, alt_cond in results[1:3]:
        alt_name = (
            alt_cond[name_key]
            if name_key in alt_cond and alt_cond[name_key]
            else alt_cond['name_en']
        )
        response['alternates'].append({
            "condition": alt_name,
            "severity": alt_cond['severity'],
        })

    return response
