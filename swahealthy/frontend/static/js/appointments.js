/**
 * SwaHealthy Appointments Logic
 * Handles trilingual localization, tab switching, and API interactions.
 */

let currentDoctorId = null;
let selectedDate = null;
let selectedSlot = null;

document.addEventListener('DOMContentLoaded', () => {
    initApptLanguage();
    initTabs();
    initGlobalListeners();
});

function initGlobalListeners() {
    // Escape key to close success modal
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeSuccessModal();
        }
    });

    // Click outside modal card to close
    const modal = document.getElementById('success-modal');
    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeSuccessModal();
            }
        });
    }
}

function initApptLanguage() {
    // Rely on global applyTranslations() from app.js for data-i18n items
    // But handle manual field placeholders and dynamic strings here
    
    const phoneEl = document.getElementById('patient-phone');
    if (phoneEl) {
        phoneEl.placeholder = t('phone_number_placeholder');
    }

    // Pre-fill booking form phone from localStorage
    const savedPhone = localStorage.getItem('swahealthy_patient_phone');
    if (savedPhone && phoneEl) {
        phoneEl.value = savedPhone;
    }
}

function initTabs() {
    const tabBtns = document.querySelectorAll('.appt-tab-btn');
    const tabPanes = document.querySelectorAll('.appt-tab-pane');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tab = btn.getAttribute('data-tab');
            tabBtns.forEach(b => b.classList.remove('active'));
            tabPanes.forEach(p => p.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById(tab + '-tab').classList.add('active');

            // Auto-load all appointments when switching to 'my' tab
            if (tab === 'my') {
                loadAllAppointments();
            }
        });
    });
}

function selectDoctor(card) {
    document.querySelectorAll('.doctor-card').forEach(c => c.classList.remove('selected'));
    card.classList.add('selected');
    currentDoctorId = card.getAttribute('data-id');
    document.getElementById('booking-step-2').classList.remove('step-hidden');
    document.getElementById('booking-step-3').classList.add('step-hidden');
    
    // Clear previous selection
    selectedSlot = null;
}

async function fetchSlots() {
    const dateInput = document.getElementById('appointment-date');
    selectedDate = dateInput.value;
    if (!selectedDate || !currentDoctorId) return;

    const slotsList = document.getElementById('slots-list');
    slotsList.innerHTML = '<div class="loader-mini"></div>';

    try {
        const res = await fetch(`/appointments/slots?doctor_id=${currentDoctorId}&date=${selectedDate}`);
        const data = await res.json();
        
        const lang = localStorage.getItem('swahealthy_lang') || 'en';
        
        if (data.slots && data.slots.length > 0) {
            slotsList.innerHTML = '';
            data.slots.forEach(slot => {
                const btn = document.createElement('button');
                btn.className = 'appt-slot-btn';
                btn.textContent = slot;
                btn.onclick = () => selectSlot(btn, slot);
                slotsList.appendChild(btn);
            });
        } else {
            slotsList.innerHTML = `<p class="no-data">${APPT_LOCALE[lang]['no_slots_found']}</p>`;
        }
    } catch (e) {
        slotsList.innerHTML = '<p class="error">Failed to load slots.</p>';
    }
}

function selectSlot(btn, slot) {
    document.querySelectorAll('.appt-slot-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    selectedSlot = slot;
    document.getElementById('booking-step-3').classList.remove('step-hidden');
}

async function submitBooking(event) {
    event.preventDefault();
    if (!navigator.onLine) {
        const lang = localStorage.getItem('swahealthy_lang') || 'en';
        alert(APPT_LOCALE[lang]['offline']);
        return;
    }

    const patientName = document.getElementById('patient-name').value;
    const patientPhone = document.getElementById('patient-phone').value;
    const patientReason = document.getElementById('patient-reason').value;

    const bookingData = {
        doctor_id: currentDoctorId,
        date: selectedDate,
        time: selectedSlot,
        patient_name: patientName,
        patient_phone: patientPhone,
        reason: patientReason,
        language: localStorage.getItem('swahealthy_lang') || 'en'
    };

    try {
        const res = await fetch('/appointments', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(bookingData)
        });

        if (res.ok) {
            // Save phone to localStorage
            localStorage.setItem('swahealthy_patient_phone', patientPhone);
            
            showSuccessModal();
            // Reset form
            document.getElementById('booking-form').reset();
            document.getElementById('booking-step-2').classList.add('step-hidden');
            document.getElementById('booking-step-3').classList.add('step-hidden');
            document.querySelectorAll('.appt-doc-card').forEach(c => c.classList.remove('selected'));
            currentDoctorId = null;
            selectedDate = null;
            selectedSlot = null;
        }
    } catch (e) {
        alert('Failed to book appointment.');
    }
}

function showSuccessModal() {
    document.getElementById('appt-modal-bg').style.display = 'flex';
    document.getElementById('btn-close-modal').focus();
    document.body.style.overflow = 'hidden';
}

function closeSuccessModal() {
    document.getElementById('appt-modal-bg').style.display = 'none';
    document.body.style.overflow = '';
}

function handleModalBgClick(e) {
    // Close if clicking the dark background, not the card itself
    if (e.target.id === 'appt-modal-bg') {
        closeSuccessModal();
    }
}

async function loadAllAppointments() {
    const list = document.getElementById('my-apps-list');
    const loader = document.getElementById('my-apps-loader');
    if (loader) loader.style.display = 'block';
    if (list) list.innerHTML = '';

    try {
        const res = await fetch('/appointments/my');
        const data = await res.json();
        if (loader) loader.style.display = 'none';
        
        const lang = localStorage.getItem('swahealthy_lang') || 'en';
        const strings = APPT_LOCALE[lang];

        if (data && data.length > 0) {
            list.innerHTML = '';
            data.forEach(app => {
                const card = document.createElement('div');
                card.className = 'appt-my-card';
                card.id = `appt-card-${app.appointment_id}`;
                card.innerHTML = `
                    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:10px;">
                        <div style="flex:1;">
                            <span class="status-badge ${app.status}">${strings['status_' + app.status] || app.status}</span>
                            <h4>${app.doctor_name}</h4>
                            <p class="special">${app.specialisation}</p>
                            <p class="datetime">👤 ${app.patient_name} &nbsp;📞 ${app.patient_phone}</p>
                            <p class="datetime">📅 ${app.appointment_date} &nbsp;🕐 ${app.appointment_time}</p>
                        </div>
                        ${app.status === 'pending' ? `
                        <div>
                            <button class="btn-cancel" onclick="cancelAppt(${app.appointment_id}, this)">Cancel</button>
                        </div>` : ''}
                    </div>
                `;
                list.appendChild(card);
            });
        } else {
            list.innerHTML = '<p class="appt-hint" style="padding:20px 0; text-align:center;">No appointments booked yet.</p>';
        }
    } catch (e) {
        if (loader) loader.style.display = 'none';
        list.innerHTML = '<p class="appt-hint" style="color:#c62828;">Failed to load appointments. Please try again.</p>';
    }
}

async function cancelAppt(id, btn) {
    if (!confirm('Cancel this appointment?')) return;
    
    // Visual feedback
    if (btn) { btn.disabled = true; btn.textContent = 'Cancelling…'; }

    try {
        const res = await fetch(`/appointments/${id}`, { method: 'DELETE' });
        if (res.ok) {
            loadAllAppointments(); // Refresh the entire list
        } else {
            alert('Could not cancel appointment.');
            if (btn) { btn.disabled = false; btn.textContent = 'Cancel'; }
        }
    } catch (e) {
        alert('Failed to cancel appointment.');
        if (btn) { btn.disabled = false; btn.textContent = 'Cancel'; }
    }
}
