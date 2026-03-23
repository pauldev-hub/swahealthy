"""
Appointment routes — booking, slots, listing, cancellation.
"""

import json

from flask import Blueprint, render_template, request, jsonify, g

from backend.models.helpers import get_db_connection

appointments_bp = Blueprint('appointments', __name__)


@appointments_bp.route('/appointments', methods=['GET', 'POST'])
def appointments():
    """Handle appointment listing and booking."""
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute("SELECT * FROM doctors")
        doctors = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return render_template('appointments/appointments.html', doctors=doctors, lang=g.lang)

    if request.method == 'POST':
        data = request.get_json()
        required = ['doctor_id', 'patient_name', 'patient_phone', 'date', 'time']
        if not all(k in data for k in required):
            return jsonify({'error': 'Missing required fields'}), 400

        cursor.execute('''
            INSERT INTO appointments (doctor_id, patient_name, patient_phone, appointment_date, appointment_time, reason, language)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['doctor_id'], data['patient_name'], data['patient_phone'],
            data['date'], data['time'], data.get('reason', ''), data.get('language', 'en'),
        ))

        appointment_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return jsonify({'appointment_id': appointment_id, 'status': 'pending'})


@appointments_bp.route('/appointments/slots')
def get_slots():
    """Get available slots for a doctor on a specific date."""
    doctor_id = request.args.get('doctor_id')
    date = request.args.get('date')
    if not doctor_id or not date:
        return jsonify({'error': 'Missing parameters'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT slots_json FROM doctors WHERE doctor_id = ?", (doctor_id,))
    doctor = cursor.fetchone()
    if not doctor:
        return jsonify({'error': 'Doctor not found'}), 404

    all_slots = json.loads(doctor['slots_json'])

    cursor.execute('''
        SELECT appointment_time FROM appointments
        WHERE doctor_id = ? AND appointment_date = ? AND status != 'cancelled'
    ''', (doctor_id, date))
    booked_slots = [row['appointment_time'] for row in cursor.fetchall()]

    available_slots = [s for s in all_slots if s not in booked_slots]
    conn.close()
    return jsonify({'slots': available_slots})


@appointments_bp.route('/appointments/my')
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


@appointments_bp.route('/appointments/<int:app_id>', methods=['DELETE'])
def cancel_appointment(app_id):
    """Cancel an appointment."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE appointments SET status = 'cancelled' WHERE appointment_id = ?", (app_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})
