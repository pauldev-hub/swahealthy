let currentLang = localStorage.getItem('swahealthy_lang') || 'en';

document.addEventListener("DOMContentLoaded", () => {
    // Check url lang and localStorage sync
    if(window.location.pathname === '/') {
        const urlParams = new URLSearchParams(window.location.search);
        const urlLang = urlParams.get('lang');
        if(!urlLang || urlLang !== currentLang) {
            window.location.search = `?lang=${currentLang}`;
        }
    }
    
    // Register Service Worker
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/static/service-worker.js')
        .then(() => console.log('SW Registered'))
        .catch(err => console.log('SW Reg Failed:', err));
    }
});

function setLang(lang) {
    localStorage.setItem('swahealthy_lang', lang);
    currentLang = lang;
    if(window.location.pathname === '/') {
        window.location.search = `?lang=${lang}`;
    } else {
        window.location.reload();
    }
}

function toggleGroup(areaId) {
    const content = document.getElementById(`group-${areaId}`);
    const parent = content.parentElement.querySelector('.group-header');
    
    if (content.classList.contains('expanded')) {
        content.classList.remove('expanded');
        parent.setAttribute('aria-expanded', 'false');
    } else {
        content.classList.add('expanded');
        parent.setAttribute('aria-expanded', 'true');
    }
}

document.addEventListener("DOMContentLoaded", () => {
    if(window.location.pathname === '/') {
        toggleGroup('head');
        toggleGroup('chest');
    }
});

function submitSymptoms(e) {
    e.preventDefault();
    const checked = document.querySelectorAll('input[name="symptoms"]:checked');
    if(checked.length === 0) {
        alert("Please select at least one symptom.");
        return;
    }
    
    const symptomIds = Array.from(checked).map(cb => parseInt(cb.value));
    
    localStorage.setItem('pending_symptoms', JSON.stringify(symptomIds));
    window.location.href = '/results';
}

if(window.location.pathname === '/results') {
    document.addEventListener("DOMContentLoaded", () => {
        const storedStr = localStorage.getItem('pending_symptoms');
        if(!storedStr) {
            window.location.href = '/';
            return;
        }
        
        const symptomIds = JSON.parse(storedStr);
        analyzeSymptoms(symptomIds, currentLang);
    });
}

let _diagnosedConditionId = null;

function analyzeSymptoms(symptomIds, lang) {
    fetch('/diagnose', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symptom_ids: symptomIds, language: lang })
    })
    .then(res => res.json())
    .then(data => {
        _diagnosedConditionId = data.condition_id || null;
        renderResult(data);
        getLocationAndFacilities();
    })
    .catch(err => {
        console.error(err);
        alert("Error analyzing symptoms. Are you offline?");
    });
}

function loadHistoryResult(symptomIds, lang) {
    localStorage.setItem('pending_symptoms', JSON.stringify(symptomIds));
    localStorage.setItem('swahealthy_lang', lang);
    window.location.href = '/results';
}

function renderResult(data) {
    document.getElementById('loading-state').style.display = 'none';
    document.getElementById('results-container').style.display = 'block';
    
    document.getElementById('res-condition').textContent = data.condition;
    
    const sevBadge = document.getElementById('res-severity');
    const severityStr = data.severity.toLowerCase();
    sevBadge.className = `severity-badge ${severityStr}`;
    sevBadge.textContent = `${data.severity.toUpperCase()} SEVERITY`;
    
    // Set severity on root for SOS widget logic
    const resultRoot = document.getElementById('result-root');
    if(resultRoot) {
        resultRoot.setAttribute('data-severity', severityStr);
        initSOS();
    }
    
    if(data.see_doctor) {
        document.getElementById('res-see-doctor').style.display = 'flex';
    }
    if(data.emergency_note) {
        document.getElementById('res-emergency').style.display = 'flex';
        document.getElementById('emergency-text').textContent = data.emergency_note;
    }
    
    const faList = document.getElementById('res-first-aid');
    faList.innerHTML = '';
    data.first_aid.forEach(step => {
        const li = document.createElement('li');
        li.textContent = step;
        faList.appendChild(li);
    });
    
    if(data.alternates && data.alternates.length > 0) {
        document.getElementById('alternates-section').style.display = 'block';
        const altContainer = document.getElementById('res-alternates');
        altContainer.innerHTML = '';
        data.alternates.forEach(alt => {
            const div = document.createElement('div');
            div.className = 'alternate-item';
            div.innerHTML = `
                <span style="font-weight: 500">${alt.condition}</span>
                <span class="severity-badge ${alt.severity.toLowerCase()} mini">${alt.severity.toUpperCase()}</span>
            `;
            altContainer.appendChild(div);
        });
    }
    
    // Appointment CTA Logic
    if(data.see_doctor || severityStr === 'medium' || severityStr === 'high') {
        const cta = document.getElementById('doctor-booking-cta');
        if(cta) {
            cta.style.display = 'block';
            updateCTALocalization();
        }
    }
}

const NAV_LOCALE = {
    'en': { 'history': 'History', 'appointments': 'Appointments', 'cta_title': 'Need a Consultation?', 'cta_msg': 'Book an appointment with a specialist now.' },
    'bn': { 'history': 'ইতিহাস', 'appointments': 'অ্যাপয়েন্টমেন্ট', 'cta_title': 'পরামর্শ প্রয়োজন?', 'cta_msg': 'এখন একজন বিশেষজ্ঞের সাথে অ্যাপয়েন্টমেন্ট বুক করুন।' },
    'hi': { 'history': 'इतिहास', 'appointments': 'अपॉइंटमेंट', 'cta_title': 'परामर्श की आवश्यकता है?', 'cta_msg': 'अभी विशेषज्ञ के साथ अपॉइंटमेंट बुक करें।' }
};

function updateNavLocalization() {
    const lang = localStorage.getItem('swahealthy_lang') || 'en';
    const strings = NAV_LOCALE[lang];
    if(document.getElementById('nav-history-text')) document.getElementById('nav-history-text').textContent = strings.history;
    if(document.getElementById('nav-appointments-text')) document.getElementById('nav-appointments-text').textContent = strings.appointments;
}

function updateCTALocalization() {
    const lang = localStorage.getItem('swahealthy_lang') || 'en';
    const strings = NAV_LOCALE[lang];
    if(document.getElementById('cta-title')) document.getElementById('cta-title').textContent = strings.cta_title;
    if(document.getElementById('cta-msg')) document.getElementById('cta-msg').textContent = strings.cta_msg;
}

document.addEventListener('DOMContentLoaded', updateNavLocalization);

let map;
function getLocationAndFacilities() {
    const locStatus = document.getElementById('loc-status');
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                locStatus.textContent = "Location detected ✓";
                fetchFacilities(position.coords.latitude, position.coords.longitude);
            },
            (error) => {
                locStatus.textContent = "Location denied. Using Kolkata center.";
                fetchFacilities(22.5726, 88.3639);
            }
        );
    } else {
        locStatus.textContent = "Location unsupported. Using Kolkata center.";
        fetchFacilities(22.5726, 88.3639);
    }
}

function fetchFacilities(lat, lng) {
    fetch(`/facilities?lat=${lat}&lng=${lng}`)
    .then(res => res.json())
    .then(data => {
        initMap(lat, lng, data);
        renderFacilitiesList(data);
    })
    .catch(err => {
        console.error("Failed fetching facilities", err);
    });

    // Also fetch nearby medicines if a condition was diagnosed
    if (_diagnosedConditionId) {
        const lang = localStorage.getItem('swahealthy_lang') || 'en';
        fetch(`/medicines?condition_id=${_diagnosedConditionId}&lat=${lat}&lng=${lng}&lang=${lang}`)
        .then(res => res.json())
        .then(medData => {
            renderMedicines(medData);
        })
        .catch(err => {
            console.error("Failed fetching medicines", err);
        });
    }
}

function renderMedicines(facilities) {
    const section = document.getElementById('medicines-section');
    const list = document.getElementById('medicines-list');
    if (!facilities || facilities.length === 0) {
        section.style.display = 'none';
        return;
    }
    section.style.display = 'block';
    list.innerHTML = '';

    facilities.forEach(f => {
        const card = document.createElement('div');
        card.className = 'medicine-facility-card';

        const medPills = f.medicines.map(m =>
            `<span class="med-pill">${m}</span>`
        ).join('');

        card.innerHTML = `
            <div class="med-card-header">
                <div class="med-card-info">
                    <div class="med-fac-name">${f.name}</div>
                    <div class="med-fac-meta">${f.type} • ${f.district}</div>
                </div>
                <div class="med-fac-dist">${f.distance} km</div>
            </div>
            <div class="med-pills-wrap">${medPills}</div>
        `;
        list.appendChild(card);
    });
}

function initMap(lat, lng, facilities) {
    if(map) map.remove();
    
    map = L.map('map', {
        attributionControl: false
    }).setView([lat, lng], 12);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19
    }).addTo(map);
    
    L.control.attribution({position: 'bottomright'}).addAttribution('&copy; OpenStreetMap').addTo(map);
    
    L.marker([lat, lng]).addTo(map).bindPopup("<b>You are here</b>");
    
    facilities.forEach(f => {
        L.marker([f.latitude, f.longitude])
        .addTo(map)
        .bindPopup(`<b>${f.name}</b><br>${f.type}<br>${f.contact}`);
    });
}

function renderFacilitiesList(facilities) {
    const list = document.getElementById('facilities-list');
    list.innerHTML = '';
    facilities.forEach(f => {
        const li = document.createElement('li');
        li.className = 'facility-item';
        li.innerHTML = `
            <div>
                <div class="fac-name">${f.name}</div>
                <div class="fac-meta">${f.type} • Contact: ${f.contact}</div>
            </div>
            <div class="fac-dist">${f.distance} km</div>
        `;
        list.appendChild(li);
    });
}

function clearHistory() {
    if(confirm("Are you sure you want to delete all history?")) {
        fetch('/history', { method: 'DELETE' })
        .then(() => window.location.reload());
    }
}

// === SOS Emergency Widget ===
const SOS_LOCALE = {
    'en': {
        'title': 'Emergency Contacts',
        'ambulance': 'Ambulance / MSVS',
        'police': 'Police',
        'emergency': 'National Emergency',
        'women': 'Women Helpline',
        'close': 'Close',
        'alert': '⚠ High severity detected. Please call emergency services if needed.'
    },
    'bn': {
        'title': 'জরুরি যোগাযোগ',
        'ambulance': 'অ্যাম্বুলেন্স / MSVS',
        'police': 'পুলিশ',
        'emergency': 'জাতীয় জরুরি অবস্থা',
        'women': 'মহিলা হেল্পলাইন',
        'close': 'বন্ধ করুন',
        'alert': '⚠ উচ্চ তীব্রতা সনাক্ত করা হয়েছে। প্রয়োজন হলে জরুরি পরিষেবা কল করুন।'
    },
    'hi': {
        'title': 'आपातकालीन संपर्क',
        'ambulance': 'एम्बुलेंस / MSVS',
        'police': 'पुलिस',
        'emergency': 'राष्ट्रीय आपातकाल',
        'women': 'महिला हेल्पलाइन',
        'close': 'बंद करें',
        'alert': '⚠ उच्च गंभीरता का पता चला। यदि आवश्यक हो तो कृपया आपातकालीन सेवाओं को कॉल करें।'
    }
};

/**
 * Opens the SOS Emergency Modal
 * @param {boolean} isAutoPrompt - Whether this was triggered automatically
 */
function openSOSModal(isAutoPrompt = false) {
    const overlay = document.getElementById('sos-overlay');
    const alertBanner = document.getElementById('sos-high-alert');
    const lang = localStorage.getItem('swahealthy_lang') || 'en';
    const strings = SOS_LOCALE[lang] || SOS_LOCALE['en'];

    // Update translations
    document.getElementById('sos-title').textContent = strings.title;
    document.getElementById('sos-alert-text').textContent = strings.alert;
    document.querySelector('.sos-close-btn').textContent = strings.close;
    
    document.querySelectorAll('[data-key]').forEach(el => {
        const key = el.getAttribute('data-key');
        if(strings[key]) el.textContent = strings[key];
    });

    if(isAutoPrompt) {
        alertBanner.style.display = 'block';
    } else {
        alertBanner.style.display = 'none';
    }

    overlay.classList.add('active');
    overlay.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden'; // Prevent scrolling
}

/**
 * Closes the SOS Emergency Modal and restores focus
 */
function closeSOSModal() {
    const overlay = document.getElementById('sos-overlay');
    overlay.classList.remove('active');
    overlay.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    document.getElementById('sos-fab').focus();
}

/**
 * Handles clicks on the overlay background to close the modal
 */
function handleOverlayClick(e) {
    if(e.target.id === 'sos-overlay') {
        closeSOSModal();
    }
}

/**
 * Initializes SOS auto-prompt logic based on severity
 */
function initSOS() {
    const resultRoot = document.getElementById('result-root');
    if(!resultRoot) return;

    const severity = resultRoot.getAttribute('data-severity');
    if(severity === 'high' && !window.sosPrompted) {
        window.sosPrompted = true; // Only trigger once
        setTimeout(() => {
            openSOSModal(true);
        }, 1500);
    }
}

// Ensure initSOS runs on page load and after results render
document.addEventListener("DOMContentLoaded", initSOS);
