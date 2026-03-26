let currentLang = localStorage.getItem('swahealthy_lang') || 'en';
let _splashReleaseRequested = false;

function looksMojibake(value) {
    return typeof value === 'string' && /Ã|Â|â|à¦|à¤|ðŸ/.test(value);
}

function decodeMojibake(value) {
    if (!looksMojibake(value)) return value;

    let current = value;
    for (let i = 0; i < 3; i += 1) {
        try {
            const bytes = Uint8Array.from(Array.from(current), ch => ch.charCodeAt(0) & 0xff);
            const decoded = new TextDecoder('utf-8').decode(bytes);
            if (!decoded || decoded === current) break;
            current = decoded;
            if (!looksMojibake(current)) break;
        } catch (err) {
            break;
        }
    }

    return current;
}

function sanitizeLocaleObject(localeObject) {
    if (!localeObject || typeof localeObject !== 'object') return localeObject;

    Object.keys(localeObject).forEach(key => {
        const value = localeObject[key];
        if (typeof value === 'string') {
            localeObject[key] = decodeMojibake(value);
        } else if (value && typeof value === 'object') {
            sanitizeLocaleObject(value);
        }
    });

    return localeObject;
}

function sanitizeLocaleMaps() {
    if (window.translations) {
        sanitizeLocaleObject(window.translations);
    }
    if (window.APPT_LOCALE) {
        sanitizeLocaleObject(window.APPT_LOCALE);
    }
}

window.decodeMojibake = decodeMojibake;

function humanizeTranslationKey(key) {
    if (!key) return '';
    if (!key.includes('_')) return key.charAt(0).toUpperCase() + key.slice(1);
    return key
        .split('_')
        .filter(Boolean)
        .map(part => part.charAt(0).toUpperCase() + part.slice(1))
        .join(' ');
}

/**
 * Translation helper
 * @param {string} key 
 * @returns {string} translated text
 */
function t(key) {
    if (window.translations && window.translations[currentLang] && window.translations[currentLang][key]) {
        return decodeMojibake(window.translations[currentLang][key]);
    }
    // Fallback to English if missing
    if (window.translations && window.translations['en'] && window.translations['en'][key]) {
        return decodeMojibake(window.translations['en'][key]);
    }
    return humanizeTranslationKey(key);
}

function applyTranslations() {
    // 1. Update HTML lang for screen readers
    document.documentElement.lang = currentLang;

    // 2. Handle Bengali Font switching
    document.body.classList.toggle('font-bn', currentLang === 'bn');
    document.body.classList.toggle('font-hi', currentLang === 'hi');

    // 3. Update all static elements with data-i18n
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        const translated = t(key);

        if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
            el.placeholder = translated;
        } else {
            // Preserve child elements (icons/svgs) if they exist
            const svgGroup = el.querySelector('svg, .logo-icon, .history-icon, .sos-icon, .btn-icon, .group-icon, .loc-icon, .med-icon, .rec-icon');
            if (svgGroup) {
                // If it has an icon, we need to be careful not to overwrite it
                // We'll look for a text node or a specific span to update
                // For simplicity, if it's a "button-icon" style, we assume we might need to update just the text
                // But often these labels are just text nodes next to the icon.
                // A better way is to wrap the text in a span if not already.
                // For the purpose of this fix, many elements already have dedicated spans.
                // If not, we'll try to update just the text part.

                // If the element has children, find the text node
                let foundText = false;
                for (let node of el.childNodes) {
                    if (node.nodeType === Node.TEXT_NODE && node.textContent.trim().length > 0) {
                        node.textContent = translated;
                        foundText = true;
                        break;
                    }
                }
                // If no text node found but it's empty otherwise, just set it
                if (!foundText && el.children.length === 0) {
                    el.textContent = translated;
                }
            } else {
                el.textContent = translated;
            }
        }
    });

    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        el.placeholder = t(el.getAttribute('data-i18n-placeholder'));
    });

    document.querySelectorAll('[data-i18n-title]').forEach(el => {
        el.setAttribute('title', t(el.getAttribute('data-i18n-title')));
    });

    document.querySelectorAll('[data-i18n-aria-label]').forEach(el => {
        el.setAttribute('aria-label', t(el.getAttribute('data-i18n-aria-label')));
    });

    document.querySelectorAll('[data-i18n-alt]').forEach(el => {
        el.setAttribute('alt', t(el.getAttribute('data-i18n-alt')));
    });

    // 4. Sync with cookie for backend
    document.cookie = `swahealthy_lang=${currentLang}; path=/; max-age=${30 * 24 * 60 * 60}`;
}

function syncServerRenderedLanguage() {
    const url = new URL(window.location.href);
    const serverRenderedPaths = new Set(['/', '/history', '/profile', '/appointments', '/summary', '/wellness']);
    const needsServerLang = window.location.pathname === '/' ||
        window.location.pathname === '/history' ||
        window.location.pathname === '/profile' ||
        window.location.pathname === '/appointments' ||
        window.location.pathname === '/wellness' ||
        window.location.pathname.startsWith('/summary/');

    document.querySelectorAll('a[href]').forEach(link => {
        const rawHref = link.getAttribute('href');
        if (!rawHref || rawHref.startsWith('#') || rawHref.startsWith('javascript:')) return;
        try {
            const nextUrl = new URL(rawHref, window.location.origin);
            const nextPath = nextUrl.pathname;
            if (
                serverRenderedPaths.has(nextPath) ||
                nextPath.startsWith('/summary/')
            ) {
                nextUrl.searchParams.set('lang', currentLang);
                link.setAttribute('href', `${nextUrl.pathname}${nextUrl.search}${nextUrl.hash}`);
            }
        } catch (err) {
            // Ignore malformed or special links.
        }
    });

    if (!needsServerLang) return;

    if (url.searchParams.get('lang') !== currentLang) {
        url.searchParams.set('lang', currentLang);
        window.location.replace(url.toString());
    }
}

function syncHistoryLocalizedFields() {
    document.querySelectorAll('.history-condition[data-condition-en]').forEach(el => {
        const nextValue =
            el.getAttribute(`data-condition-${currentLang}`) ||
            el.getAttribute('data-condition-en') ||
            el.textContent;
        el.textContent = decodeMojibake(nextValue);
    });

    document.querySelectorAll('.history-sym-names[data-symptoms-en]').forEach(el => {
        const nextValue =
            el.getAttribute(`data-symptoms-${currentLang}`) ||
            el.getAttribute('data-symptoms-en') ||
            el.textContent;
        el.textContent = decodeMojibake(nextValue);
    });
}

function releaseAppSplash() {
    if (_splashReleaseRequested) return;

    const splash = document.getElementById('app-splash');
    if (!splash) return;

    _splashReleaseRequested = true;
    document.body.classList.remove('splash-active');
    splash.classList.add('is-exiting');

    window.setTimeout(() => {
        splash.hidden = true;
        splash.remove();
    }, 560);
}

function initAppSplash() {
    const splash = document.getElementById('app-splash');
    if (!splash) return;

    document.body.classList.add('splash-active');

    let minimumElapsed = false;
    let shellReady = false;
    let workerReady = !('serviceWorker' in navigator);

    const attemptRelease = () => {
        if (minimumElapsed && (shellReady || workerReady)) {
            releaseAppSplash();
        }
    };

    window.setTimeout(() => {
        minimumElapsed = true;
        attemptRelease();
    }, 1400);

    window.requestAnimationFrame(() => {
        window.requestAnimationFrame(() => {
            shellReady = true;
            attemptRelease();
        });
    });

    window.addEventListener('load', () => {
        shellReady = true;
        attemptRelease();
    }, { once: true });

    window.setTimeout(() => {
        workerReady = true;
        attemptRelease();
    }, 3200);

    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.addEventListener('message', (event) => {
            if (event.data && event.data.type === 'SWAHEALTHY_APP_READY') {
                workerReady = true;
                attemptRelease();
            }
        });

        navigator.serviceWorker.ready
            .then(() => {
                workerReady = true;
                attemptRelease();
            })
            .catch(() => {
                workerReady = true;
                attemptRelease();
            });
    }
}

document.addEventListener("DOMContentLoaded", () => {
    sanitizeLocaleMaps();
    applyTranslations();
    syncHistoryLocalizedFields();
    syncServerRenderedLanguage();
    initAppSplash();

    // Register Service Worker
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/static/pwa/service-worker.js')
            .then(() => console.log('SW Registered'))
            .catch(err => console.log('SW Reg Failed:', err));
    }
});

function setLang(lang) {
    localStorage.setItem('swahealthy_lang', lang);
    currentLang = lang;

    // Update active state of buttons
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('onclick').includes(`'${lang}'`));
    });

    applyTranslations();

    document.querySelectorAll('.symptom-name[data-name-en]').forEach(el => {
        const nextValue =
            el.getAttribute(`data-name-${lang}`) ||
            el.getAttribute('data-name-en') ||
            el.textContent;
        el.textContent = decodeMojibake(nextValue);
    });

    syncHistoryLocalizedFields();

    const url = new URL(window.location);
    url.searchParams.set('lang', lang);
    window.location.href = url.toString();
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



// --- Standalone AI Photo Analysis Logic ---
let _standalonePhotoBase64 = null;
let _standalonePhotoType = null;

function handleStandalonePhotoSelect(e) {
    const file = e.target.files[0];
    if (!file) return;

    // Validate type
    if (!['image/jpeg', 'image/png'].includes(file.type)) {
        alert(t('upload_jpg_png'));
        e.target.value = "";
        return;
    }

    // Validate size (max 2MB)
    if (file.size > 2 * 1024 * 1024) {
        alert(t('image_under_2mb'));
        e.target.value = "";
        return;
    }

    const reader = new FileReader();
    reader.onload = function (evt) {
        const result = evt.target.result;
        const parts = result.split(',');
        
        if (parts.length < 2) {
            console.error("Invalid image data format");
            alert(t('failed_process_image'));
            return;
        }

        _standalonePhotoBase64 = parts[1];
        _standalonePhotoType = file.type;

        // Show preview
        document.getElementById('ai-upload-prompt').style.display = 'none';
        document.getElementById('ai-photo-preview-container').style.display = 'block';
        document.getElementById('ai-photo-preview').src = result;
        document.getElementById('ai-action-buttons').style.display = 'flex';
    };
    reader.readAsDataURL(file);
}

function removeStandalonePhoto(e) {
    if (e) e.stopPropagation();
    _standalonePhotoBase64 = null;
    _standalonePhotoType = null;

    const input = document.getElementById('ai-photo-input');
    if (input) input.value = "";
    document.getElementById('ai-upload-prompt').style.display = 'block';
    document.getElementById('ai-photo-preview-container').style.display = 'none';
    document.getElementById('ai-photo-preview').src = "";
    document.getElementById('ai-action-buttons').style.display = 'none';
}

function submitSymptoms(e) {
    e.preventDefault();
    const checked = document.querySelectorAll('input[name="symptoms"]:checked');
    if (checked.length === 0) {
        alert(t('select_at_least_one_symptom'));
        return;
    }

    const symptomIds = Array.from(checked).map(cb => parseInt(cb.value));
    localStorage.setItem('pending_symptoms', JSON.stringify(symptomIds));

    window.location.href = '/duration';
}

function submitDuration(e) {
    e.preventDefault();
    const checkedDuration = document.querySelector('input[name="duration"]:checked');
    const duration = checkedDuration ? checkedDuration.value : '< 1 day';
    localStorage.setItem('pending_duration', duration);
    window.location.href = '/results';
}

if (window.location.pathname === '/results') {
    document.addEventListener("DOMContentLoaded", () => {
        promoteMedicinesDrawerToBody();
        const storedStr = localStorage.getItem('pending_symptoms');
        const duration = localStorage.getItem('pending_duration') || '< 1 day';
        if (!storedStr) {
            window.location.href = '/';
            return;
        }

        const symptomIds = JSON.parse(storedStr);
        analyzeSymptoms(symptomIds, currentLang, duration);
    });
}

if (window.location.pathname === '/') {
    document.addEventListener("DOMContentLoaded", () => {
        loadHomeNearbyHospitals();
    });
}

function analyzeStandalonePhoto() {
    if (!_standalonePhotoBase64 || !_standalonePhotoType) {
        alert(t('select_photo_first'));
        return;
    }

    document.getElementById('ai-action-buttons').style.display = 'none';
    document.getElementById('ai-loading-state').style.display = 'flex';
    document.getElementById('ai-assessment-card').style.display = 'none';

    const payload = {
        image: _standalonePhotoBase64,
        media_type: _standalonePhotoType,
        language: currentLang
    };

    fetch('/analyze-photo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
        .then(res => res.json())
        .then(data => {
            document.getElementById('ai-loading-state').style.display = 'none';
            renderStandaloneAssessment(data);
        })
        .catch(err => {
            console.error("Photo analysis failed:", err);
            document.getElementById('ai-loading-state').style.display = 'none';
            alert(t('failed_analyze_photo'));
            document.getElementById('ai-action-buttons').style.display = 'flex';
        });
}

function renderStandaloneAssessment(data) {
    document.getElementById('ai-action-buttons').style.display = 'flex';
    document.getElementById('ai-assessment-card').style.display = 'block';

    if (data.error) {
        document.getElementById('ai-photo-observed').textContent = "Error: " + data.error;
        document.getElementById('ai-photo-urgency').textContent = t('error_label');
        document.getElementById('ai-photo-urgency').className = "severity-badge high mini";
        document.getElementById('ai-photo-recommendation').textContent = t('check_logs_details');
        document.getElementById('ai-photo-conditions').innerHTML = "";
        return;
    }

    document.getElementById('ai-photo-observed').textContent = data.observed || t('not_available');

    const badge = document.getElementById('ai-photo-urgency');
    const urgency = (data.urgency || "low").toLowerCase();
    badge.className = `severity-badge ${urgency} mini`;
    badge.textContent = t(`${urgency}_urgency`);

    const condList = document.getElementById('ai-photo-conditions');
    condList.innerHTML = '';
    if (data.possible_conditions && data.possible_conditions.length > 0) {
        data.possible_conditions.forEach(c => {
            const span = document.createElement('span');
            span.className = 'med-pill';
            span.textContent = c;
            condList.appendChild(span);
        });
    } else {
        const span = document.createElement('span');
        span.className = 'med-pill';
        span.textContent = t('none_identified');
        condList.appendChild(span);
    }

    document.getElementById('ai-photo-recommendation').textContent = data.recommendation || "";
}

function resetStandaloneAnalysis() {
    removeStandalonePhoto();
    document.getElementById('ai-assessment-card').style.display = 'none';
}

let _diagnosedConditionId = null;
/** Snapshot for re-rendering the medicines drawer (fixed inside transformed main would clip; see promoteMedicinesDrawerToBody). */
let _cachedDrawerMedicines = [];
let _homeNearbyLoaded = false;
let _homeNearbyRequestInFlight = false;

function promoteMedicinesDrawerToBody() {
    const overlay = document.getElementById('medicines-overlay');
    const drawer = document.getElementById('medicines-drawer');
    if (!overlay || !drawer) return;
    if (overlay.parentElement !== document.body) {
        document.body.appendChild(overlay);
    }
    if (drawer.parentElement !== document.body) {
        document.body.appendChild(drawer);
    }
}

function medicineDisplayLabel(med) {
    if (med == null) return '';
    if (typeof med === 'string') return med;
    if (typeof med === 'object') {
        return med.name || med.medicine_name || med.label || '';
    }
    return String(med);
}

function fillMedicinesDrawerList(medicines) {
    const container = document.querySelector('#medicines-drawer #drawer-medicines-list');
    if (!container) return;
    const raw = Array.isArray(medicines) ? medicines : [];
    const labels = raw.map(medicineDisplayLabel).map(s => String(s).trim()).filter(Boolean);
    container.innerHTML = '';
    if (labels.length === 0) {
        const p = document.createElement('p');
        p.className = 'drawer-medicines-empty';
        p.textContent = t('consult_pharmacist_otc');
        container.appendChild(p);
        return;
    }
    labels.forEach((text) => {
        const span = document.createElement('span');
        span.className = 'med-chip';
        span.textContent = text;
        container.appendChild(span);
    });
}

function analyzeSymptoms(symptomIds, lang, duration = '< 1 day') {
    const age = localStorage.getItem('swahealthy_age');
    const gender = localStorage.getItem('swahealthy_gender');

    fetch('/diagnose', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            symptom_ids: symptomIds,
            language: lang,
            duration: duration,
            age: age,
            gender: gender
        })
    })
        .then(res => {
            if (!res.ok) {
                return res.json().then(err => Promise.reject(err));
            }
            return res.json();
        })
        .then(data => {
            if (data.error) {
                console.error("API Error:", data);
                alert(`${t('error_analyzing_symptoms')}: ${data.error}`);
                return;
            }

            _diagnosedConditionId = data.condition_id || null;

            // For guest users, save to local history so profile dashboard shows check count
            if (!document.body.classList.contains('user-logged-in')) {
                try {
                    const history = JSON.parse(localStorage.getItem('swahealthy_history') || '[]');
                    history.push({
                        condition: data.condition,
                        severity: data.severity,
                        date: new Date().toISOString()
                    });
                    localStorage.setItem('swahealthy_history', JSON.stringify(history));
                } catch (e) {
                    console.error("Failed to save guest history:", e);
                }
            }

            // Render the result and show facilities
            console.log('[analyzeSymptoms] Rendering result on /results page...');
            renderResult(data);
            getLocationAndFacilities();
            
            // Clear pending data from localStorage
            localStorage.removeItem('pending_symptoms');
            localStorage.removeItem('pending_duration');
        })
        .catch(err => {
            console.error("Fetch error:", err);
            const errMsg = err.error || err.message || "Unknown error";
            alert(`${t('error_analyzing_symptoms')}: ${errMsg}`);
        });
}

function loadHistoryResult(symptomIds, lang) {
    localStorage.setItem('pending_symptoms', JSON.stringify(symptomIds));
    // Do not set photo for history view (or it will re-analyze)
    localStorage.removeItem('pending_photo_b64');
    localStorage.removeItem('pending_photo_type');

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
    sevBadge.textContent = t(`${severityStr}_severity`);

    // Set severity on root for SOS widget logic
    const resultRoot = document.getElementById('result-root');
    if (resultRoot) {
        resultRoot.setAttribute('data-severity', severityStr);
        initSOS();
    }

    if (data.see_doctor) {
        document.getElementById('res-see-doctor').style.display = 'flex';
    }
    if (data.emergency_note) {
        document.getElementById('res-emergency').style.display = 'flex';
        document.getElementById('emergency-text').textContent = data.emergency_note;
    }

    const durationContainer = document.getElementById('res-duration-container');
    const durationText = document.getElementById('res-duration-text');
    if (durationContainer && durationText) {
        if (data.duration_note) {
            durationContainer.style.display = 'flex';
            durationText.textContent = data.duration_note;
        } else {
            durationContainer.style.display = 'none';
        }
    }

    const faList = document.getElementById('res-first-aid');
    faList.innerHTML = '';
    data.first_aid.forEach(step => {
        const li = document.createElement('li');
        li.textContent = step;
        faList.appendChild(li);
    });

    promoteMedicinesDrawerToBody();
    const medicinesBtn = document.getElementById('medicines-btn');
    const meds = data.recommended_medicines && data.recommended_medicines.length > 0
        ? data.recommended_medicines
        : [];
    _cachedDrawerMedicines = meds;
    const labels = meds.map(medicineDisplayLabel).map(s => String(s).trim()).filter(Boolean);
    if (medicinesBtn) {
        if (labels.length > 0) {
            medicinesBtn.innerHTML = `💊 <span>Medicines (${labels.length})</span>`;
        } else if (meds.length > 0) {
            medicinesBtn.innerHTML = `💊 <span>Medicines (${meds.length})</span>`;
        } else {
            medicinesBtn.innerHTML = '💊 <span>Medicines</span>';
        }
    }
    fillMedicinesDrawerList(meds);

    const inlineMedsWidget = document.getElementById('recommended-meds-widget');
    const inlineMedsList = document.getElementById('recommended-meds-inline');
    if (inlineMedsWidget && inlineMedsList) {
        if (labels.length > 0) {
            inlineMedsWidget.style.display = 'block';
            inlineMedsList.innerHTML = '';
            labels.forEach(text => {
                const span = document.createElement('span');
                span.className = 'med-pill';
                span.textContent = text;
                inlineMedsList.appendChild(span);
            });
        } else {
            inlineMedsWidget.style.display = 'none';
        }
    }

    if (data.alternates && data.alternates.length > 0) {
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

    if (data.log_id) {
        const btn = document.getElementById('save-summary-widget');
        if (btn) {
            btn.href = `/summary/${data.log_id}?lang=${localStorage.getItem('swahealthy_lang') || 'en'}`;
            btn.style.display = 'inline-flex';
        }
    }
}

// Helper for dynamic condition names - we'll keep the server-provided translated name 
// as it comes from the DB, but for static strings we use t()

let _lastFacilityMapState = null;

function formatDistance(distance) {
    const numeric = Number(distance);
    if (!Number.isFinite(numeric)) return '';
    return `${numeric.toFixed(numeric >= 10 ? 0 : 1)} km`;
}

function getFallbackCoordinates() {
    return { lat: 22.5726, lng: 88.3639, label: t('default_service_area') };
}

function loadHomeNearbyHospitals(force = false) {
    const list = document.getElementById('home-nearby-list');
    const status = document.getElementById('home-nearby-status');
    const loading = document.getElementById('home-nearby-loading');

    if (!list || !status || !loading) return;
    if (_homeNearbyLoaded && !force) return;
    if (_homeNearbyRequestInFlight) return;

    _homeNearbyRequestInFlight = true;
    loading.style.display = 'block';
    status.textContent = t('detecting');

    const loadHospitals = (lat, lng, locationLabel, statusMessage) => {
        status.textContent = statusMessage || t('location_detected');

        fetch(`/nearby-hospitals?lat=${lat}&lng=${lng}&limit=10`)
            .then(res => res.json())
            .then(data => {
                renderHomeNearbyHospitals(Array.isArray(data) ? data : []);
                _homeNearbyLoaded = true;
            })
            .catch(err => {
                console.error('Failed fetching nearby hospitals', err);
                renderHomeNearbyHospitals([]);
                status.textContent = t('nearby_hospitals_unavailable');
            })
            .finally(() => {
                loading.style.display = 'none';
                _homeNearbyRequestInFlight = false;
            });
    };

    if ('geolocation' in navigator) {
        navigator.geolocation.getCurrentPosition(
            (position) => loadHospitals(position.coords.latitude, position.coords.longitude, '', t('location_detected')),
            () => {
                const fallback = getFallbackCoordinates();
                loadHospitals(fallback.lat, fallback.lng, fallback.label, `${t('location_denied')} ${fallback.label}`);
            },
            { enableHighAccuracy: true, timeout: 8000, maximumAge: 300000 }
        );
        return;
    }

    const fallback = getFallbackCoordinates();
    loadHospitals(fallback.lat, fallback.lng, fallback.label, `${t('location_unsupported')} ${fallback.label}`);
}

function renderHomeNearbyHospitals(hospitals) {
    const list = document.getElementById('home-nearby-list');
    if (!list) return;

    list.innerHTML = '';

    if (!hospitals.length) {
        list.innerHTML = `<li class="facility-item">${t('no_hospitals_found')}</li>`;
        return;
    }

    hospitals.forEach((hospital) => {
        const item = document.createElement('li');
        item.className = 'facility-item';
        item.innerHTML = `
            <div>
                <div class="fac-name">${hospital.name}</div>
                <div class="fac-meta">${hospital.ownership} • ${hospital.type} • ${hospital.district}</div>
                <div class="fac-meta">${t('contact_label')}: ${hospital.contact || 'N/A'}</div>
            </div>
            <div class="fac-dist">${formatDistance(hospital.distance)}</div>
        `;
        list.appendChild(item);
    });
}

function createMapMarkerIcon(kind) {
    const icons = {
        user: `
            <div class="map-marker map-marker-user">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <path d="M12 21s6-5.2 6-11a6 6 0 1 0-12 0c0 5.8 6 11 6 11Z"></path>
                    <circle cx="12" cy="10" r="2.5"></circle>
                </svg>
            </div>
        `,
        aushadhi: `
            <div class="map-marker map-marker-aushadhi">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <path d="M9 7h6"></path>
                    <path d="M10 4h4"></path>
                    <path d="M8 10h8l-1 8H9l-1-8Z"></path>
                    <path d="M10 14h4"></path>
                </svg>
            </div>
        `,
        facility: `
            <div class="map-marker map-marker-facility">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <path d="M6 21V7a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v14"></path>
                    <path d="M4 21h16"></path>
                    <path d="M9 10h.01"></path>
                    <path d="M15 10h.01"></path>
                    <path d="M9 14h.01"></path>
                    <path d="M15 14h.01"></path>
                </svg>
            </div>
        `
    };

    return L.divIcon({
        html: icons[kind] || icons.facility,
        className: kind === 'user' ? 'user-location-icon' : 'facility-icon',
        iconSize: [34, 42],
        iconAnchor: [17, 38],
        popupAnchor: [0, -34]
    });
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
                const fallback = getFallbackCoordinates();
                locStatus.textContent = `${t('location_denied')} ${fallback.label}`;
                fetchFacilities(fallback.lat, fallback.lng);
            }
        );
    } else {
        const fallback = getFallbackCoordinates();
        locStatus.textContent = `${t('location_unsupported')} ${fallback.label}`;
        fetchFacilities(fallback.lat, fallback.lng);
    }
    setUpTabs();
}

function setUpTabs() {
    const tabAushadhi = document.getElementById('tab-aushadhi');
    const tabFacilities = document.getElementById('tab-facilities');
    const tabMap = document.getElementById('tab-map');
    const contentAushadhi = document.getElementById('tab-content-aushadhi');
    const contentFacilities = document.getElementById('tab-content-facilities');
    const contentMap = document.getElementById('tab-content-map');

    if (!tabAushadhi || !tabFacilities || !tabMap || !contentAushadhi || !contentFacilities || !contentMap) return;
    if (tabAushadhi.dataset.tabsBound === 'true') return;

    const activateTab = (selected) => {
        tabAushadhi.classList.add('active');
        contentAushadhi.classList.add('active');
        tabFacilities.classList.remove('active');
        contentFacilities.classList.remove('active');
        tabMap.classList.remove('active');
        contentMap.classList.remove('active');

        if (selected === 'facilities') {
            tabAushadhi.classList.remove('active');
            tabFacilities.classList.add('active');
            contentAushadhi.classList.remove('active');
            contentFacilities.classList.add('active');
        } else if (selected === 'map') {
            tabAushadhi.classList.remove('active');
            tabMap.classList.add('active');
            contentAushadhi.classList.remove('active');
            contentMap.classList.add('active');
            if (_lastFacilityMapState) {
                setTimeout(() => {
                    renderMap(_lastFacilityMapState.lat, _lastFacilityMapState.lng, _lastFacilityMapState.facilities);
                }, 60);
            }
        }
    };

    tabAushadhi.addEventListener('click', () => activateTab('aushadhi'));
    tabFacilities.addEventListener('click', () => activateTab('facilities'));
    tabMap.addEventListener('click', () => activateTab('map'));

    tabAushadhi.dataset.tabsBound = 'true';
}

function fetchFacilities(lat, lng) {
    fetch(`/facilities?lat=${lat}&lng=${lng}&limit=10`)
        .then(res => res.json())
        .then(data => {
            _lastFacilityMapState = { lat, lng, facilities: data };
            renderFacilitiesList(data);
            if (typeof renderMap === 'function' && isMapTabActive()) {
                renderMap(lat, lng, data);
            }
        })
        .catch(err => {
            console.error("Failed fetching facilities", err);
        });

    if (_diagnosedConditionId) {
        const lang = localStorage.getItem('swahealthy_lang') || 'en';
        fetch(`/medicines?condition_id=${_diagnosedConditionId}&lat=${lat}&lng=${lng}&lang=${lang}`)
            .then(res => res.json())
            .then(medData => {
                if (Array.isArray(medData)) {
                    renderMedicines(medData);
                } else if (medData && medData.error) {
                    console.error('Medicines API error', medData.error);
                    renderMedicines([]);
                } else {
                    renderMedicines([]);
                }
            })
            .catch(err => {
                console.error("Failed fetching medicines", err);
                renderMedicines([]);
            });
    } else {
        renderMedicines([]);
    }
}

function renderMedicines(facilities) {
    console.log('renderMedicines called with', facilities);
    const section = document.getElementById('medicines-section');
    const list = document.getElementById('medicines-list');
    const empty = document.getElementById('medicines-empty');
    const count = document.getElementById('medicines-count');

    if (!facilities || facilities.length === 0) {
        section.style.display = 'block';
        count.textContent = t('aushadhi_centers_found_zero');
        list.innerHTML = '';
        empty.style.display = 'block';
        return;
    }
    section.style.display = 'block';
    empty.style.display = 'none';
    list.innerHTML = '';
    count.textContent = t('aushadhi_centers_found').replace('{count}', facilities.length);

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


function renderMap(lat, lng, facilities) {
    const mapContainer = document.getElementById('fac-map');
    if (!mapContainer) return;

    // Remove existing map instance if any
    if (map) {
        map.remove();
        map = null;
    }

    try {
        map = L.map('fac-map').setView([lat, lng], 13);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributing'
        }).addTo(map);

        const bounds = L.latLngBounds([[lat, lng]]);

        // User marker
        const userIcon = L.divIcon({
            html: '📍',
            className: 'user-location-icon',
            iconSize: [24, 24],
            iconAnchor: [12, 12]
        });
        L.marker([lat, lng], { icon: userIcon }).addTo(map)
            .bindPopup('You are here')
            .openPopup();

        // Facility markers
        facilities.forEach(fac => {
            if (fac.latitude && fac.longitude) {
                const isAushadhi = fac.type === 'Jan Aushadhi';
                const emoji = isAushadhi ? '💊' : '🏥';

                const facIcon = L.divIcon({
                    html: `<div style="font-size: 24px;">${emoji}</div>`,
                    className: 'facility-icon',
                    iconSize: [30, 30],
                    iconAnchor: [15, 15]
                });

                L.marker([fac.latitude, fac.longitude], { icon: facIcon }).addTo(map)
                    .bindPopup(`<b>${fac.name}</b><br>${fac.type}`);

                bounds.extend([fac.latitude, fac.longitude]);
            }
        });

        if (facilities.length > 0) {
            map.fitBounds(bounds, { padding: [40, 40], maxZoom: 14 });
        }

        // Fix map gray box issue
        setTimeout(() => {
            map.invalidateSize();
            if (facilities.length > 0) {
                map.fitBounds(bounds, { padding: [40, 40], maxZoom: 14 });
            }
        }, 100);
    } catch (e) {
        console.error("Map initialization failed", e);
    }
}

function renderFacilitiesList(facilities) {
    const list = document.getElementById('facilities-list');
    list.innerHTML = '';
    const hospitals = facilities.filter(f => f.type !== 'Jan Aushadhi');
    hospitals.forEach(f => {
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
    if (hospitals.length === 0) {
        list.innerHTML = '<li class="facility-item">No non-Jan Aushadhi facilities found nearby.</li>';
    }
}

function clearHistory() {
    if (confirm("Are you sure you want to delete all history?")) {
        fetch('/history', { method: 'DELETE' })
            .then(() => window.location.reload());
    }
}

function getLocationAndFacilities() {
    const locStatus = document.getElementById('loc-status');
    setUpTabs();
    if (!locStatus) return;

    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                locStatus.textContent = t('location_detected');
                fetchFacilities(position.coords.latitude, position.coords.longitude);
            },
            () => {
                const fallback = getFallbackCoordinates();
                locStatus.textContent = `${t('location_denied')} ${fallback.label}`;
                fetchFacilities(fallback.lat, fallback.lng);
            }
        );
    } else {
        const fallback = getFallbackCoordinates();
        locStatus.textContent = `${t('location_unsupported')} ${fallback.label}`;
        fetchFacilities(fallback.lat, fallback.lng);
    }
}

function isMapTabActive() {
    const tabMap = document.getElementById('tab-map');
    const mapContent = document.getElementById('tab-content-map');
    const hasTab = tabMap && tabMap.classList.contains('active');
    const hasContent = mapContent && mapContent.classList.contains('active');
    return Boolean(hasTab && hasContent);
}

function renderMedicines(facilities) {
    console.log('renderMedicines called with', facilities);
    const section = document.getElementById('medicines-section');
    const list = document.getElementById('medicines-list');
    const empty = document.getElementById('medicines-empty');
    const count = document.getElementById('medicines-count');

    if (!section || !list || !empty || !count) return;

    if (!facilities || facilities.length === 0) {
        section.style.display = 'block';
        count.textContent = t('aushadhi_centers_found_zero');
        list.innerHTML = '';
        empty.style.display = 'block';
        return;
    }

    section.style.display = 'block';
    empty.style.display = 'none';
    list.innerHTML = '';
    count.textContent = t('aushadhi_centers_found').replace('{count}', facilities.length);

    facilities.forEach((f) => {
        const card = document.createElement('div');
        card.className = 'medicine-facility-card';

        const medPills = (f.medicines || []).map((m) =>
            `<span class="med-pill">${m}</span>`
        ).join('');

        card.innerHTML = `
            <div class="med-card-header">
                <div class="med-card-info">
                    <div class="med-fac-name">${f.name}</div>
                    <div class="med-fac-meta">${f.type} • ${f.district}</div>
                </div>
                <div class="med-fac-dist">${formatDistance(f.distance)}</div>
            </div>
            <div class="med-pills-wrap">${medPills}</div>
        `;
        list.appendChild(card);
    });
}

function renderMap(lat, lng, facilities) {
    const mapContainer = document.getElementById('fac-map');
    if (!mapContainer || !isMapTabActive()) return;

    if (map) {
        map.remove();
        map = null;
    }

    try {
        map = L.map('fac-map').setView([lat, lng], 13);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors'
        }).addTo(map);

        const bounds = L.latLngBounds([[lat, lng]]);
        L.marker([lat, lng], { icon: createMapMarkerIcon('user') }).addTo(map)
            .bindPopup(t('you_are_here'));

        (facilities || []).forEach((fac) => {
            if (fac.latitude && fac.longitude) {
                const iconKind = fac.type === 'Jan Aushadhi' ? 'aushadhi' : 'facility';
                L.marker([fac.latitude, fac.longitude], { icon: createMapMarkerIcon(iconKind) }).addTo(map)
                    .bindPopup(`<b>${fac.name}</b><br>${fac.type}${fac.district ? `<br>${fac.district}` : ''}`);
                bounds.extend([fac.latitude, fac.longitude]);
            }
        });

        if ((facilities || []).length > 0) {
            map.fitBounds(bounds, { padding: [40, 40], maxZoom: 14 });
        }

        setTimeout(() => {
            if (!map) return;
            map.invalidateSize();
            if ((facilities || []).length > 0) {
                map.fitBounds(bounds, { padding: [40, 40], maxZoom: 14 });
            }
        }, 100);
    } catch (e) {
        console.error("Map initialization failed", e);
    }
}

function renderFacilitiesList(facilities) {
    const list = document.getElementById('facilities-list');
    if (!list) return;

    list.innerHTML = '';
    const hospitals = (facilities || []).filter((f) => f.type !== 'Jan Aushadhi');

    hospitals.forEach((f) => {
        const li = document.createElement('li');
        li.className = 'facility-item';
        li.innerHTML = `
            <div>
                <div class="fac-name">${f.name}</div>
                <div class="fac-meta">${f.type} • ${f.district || getFallbackCoordinates().label}</div>
                <div class="fac-meta">${t('contact_label')}: ${f.contact || 'N/A'}</div>
            </div>
            <div class="fac-dist">${formatDistance(f.distance)}</div>
        `;
        list.appendChild(li);
    });

    if (hospitals.length === 0) {
        list.innerHTML = `<li class="facility-item">${t('no_hospitals_found')}</li>`;
    }
}

function clearHistory() {
    if (confirm(t('confirm_clear_history'))) {
        fetch('/history', { method: 'DELETE' })
            .then(() => window.location.reload());
    }
}

// Emergency SOS handling
function openSosDrawer() {
    document.getElementById('sos-overlay').classList.add('open');
    document.getElementById('sos-drawer').classList.add('open');
}

function closeSosDrawer() {
    document.getElementById('sos-overlay').classList.remove('open');
    document.getElementById('sos-drawer').classList.remove('open');
}

document.querySelectorAll('.sos-chip').forEach(chip => {
    chip.addEventListener('click', () => {
        window.location.href = `tel:${chip.dataset.phone}`;
    });
});

// Medicines Drawer handling
function openMedicinesDrawer() {
    promoteMedicinesDrawerToBody();
    fillMedicinesDrawerList(_cachedDrawerMedicines);
    const drawer = document.getElementById('medicines-drawer');
    const overlay = document.getElementById('medicines-overlay');
    if (!drawer) return;
    drawer.style.transform = 'translateY(0)';
    drawer.style.transition = 'transform 0.3s ease';
    if (overlay) overlay.style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function closeMedicinesDrawer() {
    const drawer = document.getElementById('medicines-drawer');
    const overlay = document.getElementById('medicines-overlay');
    if (!drawer) return;
    drawer.style.transform = 'translateY(100%)';
    if (overlay) overlay.style.display = 'none';
    document.body.style.overflow = '';
}

// === SOS Emergency Widget ===
function openSOSModal(isAutoPrompt = false) {
    const overlay = document.getElementById('sos-overlay');
    const alertBanner = document.getElementById('sos-high-alert');

    // Update translations
    document.getElementById('sos-title').textContent = t('emergency_contacts');
    document.getElementById('sos-alert-text').textContent = t('high_severity_alert');
    document.querySelector('.sos-close-btn').textContent = t('close');

    if (isAutoPrompt) {
        alertBanner.style.display = 'block';
    } else {
        alertBanner.style.display = 'none';
    }

    overlay.classList.add('open');
    overlay.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
}

/**
 * Closes the SOS Emergency Modal and restores focus
 */
function closeSOSModal() {
    const overlay = document.getElementById('sos-overlay');
    overlay.classList.remove('open');
    overlay.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    document.getElementById('sos-fab').focus();
}

/**
 * Handles clicks on the overlay background to close the modal
 */
function handleOverlayClick(e) {
    if (e.target.id === 'sos-overlay') {
        closeSOSModal();
    }
}

/**
 * Initializes SOS auto-prompt logic based on severity
 */
function initSOS() {
    const resultRoot = document.getElementById('result-root');
    if (!resultRoot) return;

    const severity = resultRoot.getAttribute('data-severity');
    if (severity === 'high' && !window.sosPrompted) {
        window.sosPrompted = true; // Only trigger once
        setTimeout(() => {
            openSOSModal(true);
        }, 1500);
    }
}

document.addEventListener('click', function (e) {
    const btn = e.target.closest('#medicines-btn');
    if (btn) {
        openMedicinesDrawer();
        return;
    }
    const closeBtn = e.target.closest('#medicines-overlay, .btn-block.btn-light');
    if (closeBtn && document.getElementById('medicines-drawer')) {
        const drawer = document.getElementById('medicines-drawer');
        if (drawer.style.transform === 'translateY(0px)' ||
            drawer.style.transform === 'translateY(0)') {
            closeMedicinesDrawer();
        }
    }
});

document.addEventListener("DOMContentLoaded", () => {
    initSOS();
});

// === Upload Photo Modal ===
function openUploadModal() {
    const overlay = document.getElementById('upload-overlay');
    if (overlay) {
        overlay.classList.add('active');
        overlay.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';
    }
}

function closeUploadModal() {
    const overlay = document.getElementById('upload-overlay');
    if (overlay) {
        overlay.classList.remove('active');
        overlay.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
    }
}

function handleUploadOverlayClick(e) {
    if (e.target.id === 'upload-overlay') {
        closeUploadModal();
    }
}
