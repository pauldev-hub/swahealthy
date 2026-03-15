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

function analyzeSymptoms(symptomIds, lang) {
    fetch('/diagnose', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symptom_ids: symptomIds, language: lang })
    })
    .then(res => res.json())
    .then(data => {
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
    sevBadge.className = `severity-badge ${data.severity.toLowerCase()}`;
    sevBadge.textContent = `${data.severity.toUpperCase()} SEVERITY`;
    
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
}

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
