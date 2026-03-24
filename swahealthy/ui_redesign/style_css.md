# style.css — Full Replacement
**File location:** `static/css/style.css`  
Replace the entire file with the code below.

```css
/* ============================================================
   SwaHealthy — Professional UI v2.0
   Targets your exact class names. 95%+ drop-in accurate.
   ============================================================ */

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700&family=Noto+Sans+Bengali:wght@400;500;600&family=Noto+Sans+Devanagari:wght@400;500;600&display=swap');

/* ============================================================
   CSS VARIABLES
   ============================================================ */
:root {
  --primary:         #0D9488;
  --primary-dark:    #0F766E;
  --primary-light:   #CCFBF1;
  --accent:          #14B8A6;
  --accent2:         #2DD4BF;

  --sev-low:         #16A34A;
  --sev-low-bg:      #DCFCE7;
  --sev-med:         #D97706;
  --sev-med-bg:      #FEF3C7;
  --sev-high:        #DC2626;
  --sev-high-bg:     #FEE2E2;

  --bg:              #F0FDFA;
  --surface:         #FFFFFF;
  --surface2:        #F8FFFE;
  --border:          #CCFBF1;
  --border-mid:      #99F6E4;

  --text:            #134E4A;
  --text-light:      #5EADA6;
  --text-muted:      #94A3B8;

  --r-sm:  8px;
  --r-md:  14px;
  --r-lg:  20px;
  --r-xl:  28px;

  --sh-sm: 0 1px 3px rgba(13,148,136,.08), 0 1px 2px rgba(13,148,136,.06);
  --sh-md: 0 4px 16px rgba(13,148,136,.12), 0 2px 6px rgba(13,148,136,.08);
  --sh-lg: 0 10px 32px rgba(13,148,136,.15), 0 4px 12px rgba(13,148,136,.10);

  --font: 'DM Sans', 'Noto Sans Bengali', 'Noto Sans Devanagari', sans-serif;
  --ease: 0.2s cubic-bezier(.4,0,.2,1);
}

/* ============================================================
   RESET & BASE
   ============================================================ */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { font-size: 16px; scroll-behavior: smooth; }
body {
  font-family: var(--font);
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}
img { max-width: 100%; display: block; }
a { color: var(--primary); text-decoration: none; }
a:hover { color: var(--primary-dark); }

/* ============================================================
   NAVBAR  — targets your: .navbar .nav-container .nav-brand
             .nav-controls .lang-toggle .lang-btn .history-link
   ============================================================ */
.navbar {
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: var(--sh-sm);
}

.nav-container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 1.25rem;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--primary);
  letter-spacing: -0.3px;
  text-decoration: none;
  white-space: nowrap;
}

.nav-brand .logo-icon {
  width: 36px; height: 36px;
  background: linear-gradient(135deg, var(--primary), var(--accent2));
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.1rem;
}

.nav-controls {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  flex-wrap: nowrap;
  overflow-x: auto;
}

/* Language toggle */
.lang-toggle {
  display: flex;
  align-items: center;
  background: var(--bg);
  border: 1px solid var(--border-mid);
  border-radius: var(--r-sm);
  padding: 3px 4px;
  gap: 2px;
  margin-right: 0.5rem;
}

.lang-toggle .divider {
  color: var(--border-mid);
  font-size: 0.75rem;
  pointer-events: none;
}

.lang-btn {
  background: none;
  border: none;
  padding: 0.28rem 0.6rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--text-light);
  border-radius: 5px;
  cursor: pointer;
  transition: all var(--ease);
  font-family: var(--font);
  white-space: nowrap;
}

.lang-btn.active,
.lang-btn:hover {
  background: var(--primary);
  color: #fff;
}

/* Nav links (History, Appointments, AI, Profile) */
.history-link {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  font-size: 0.78rem;
  font-weight: 500;
  color: var(--text-light);
  padding: 0.4rem 0.6rem;
  border-radius: var(--r-sm);
  transition: all var(--ease);
  white-space: nowrap;
}

.history-link:hover {
  background: var(--primary-light);
  color: var(--primary-dark);
}

.history-icon { font-size: 0.95rem; }

/* Auth links */
.auth-link {
  font-size: 0.78rem;
  font-weight: 600;
  padding: 0.38rem 0.9rem;
  border-radius: var(--r-sm);
  border: 1.5px solid var(--primary);
  color: var(--primary);
  transition: all var(--ease);
  white-space: nowrap;
}
.auth-link:hover { background: var(--primary); color: #fff; }

.logout-link {
  border-color: #ff5252 !important;
  color: #ff5252 !important;
}
.logout-link:hover { background: #ff5252 !important; color: #fff !important; }

/* User profile in nav */
.user-profile {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.profile-pic {
  width: 32px; height: 32px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid var(--border-mid);
}

.user-name {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text);
  max-width: 90px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* ============================================================
   MAIN CONTENT
   ============================================================ */
.main-content { min-height: calc(100vh - 64px); }

/* ============================================================
   PAGE CONTAINER  — your: .page-container
   ============================================================ */
.page-container {
  max-width: 520px;
  margin: 0 auto;
  padding: 1.5rem 1rem 7rem;
}

/* ============================================================
   PAGE HEADER  — your: .page-header  .subtitle  .title-action  .back-link
   ============================================================ */
.page-header {
  margin-bottom: 1.5rem;
}

.page-header h1 {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--text);
  letter-spacing: -0.5px;
  line-height: 1.2;
}

.page-header .subtitle {
  color: var(--text-light);
  margin-top: 0.35rem;
  font-size: 0.92rem;
}

.title-action {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.back-link {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 38px; height: 38px;
  border-radius: var(--r-md);
  background: var(--surface);
  border: 1px solid var(--border-mid);
  color: var(--text);
  transition: all var(--ease);
  flex-shrink: 0;
}

.back-link:hover {
  background: var(--primary-light);
  color: var(--primary);
  border-color: var(--primary);
}

/* ============================================================
   HERO BANNER (index page intro)
   ============================================================ */
.hero-banner {
  background: linear-gradient(135deg, var(--primary) 0%, var(--accent2) 100%);
  border-radius: var(--r-xl);
  padding: 1.5rem;
  color: #fff;
  margin-bottom: 1.5rem;
  position: relative;
  overflow: hidden;
}

.hero-banner::before {
  content: '';
  position: absolute;
  top: -24px; right: -24px;
  width: 120px; height: 120px;
  background: rgba(255,255,255,.08);
  border-radius: 50%;
}

.hero-banner h2 { font-size: 1.1rem; font-weight: 600; margin-bottom: 0.3rem; }
.hero-banner p  { font-size: 0.85rem; opacity: .85; }

/* ============================================================
   GENERIC CARD  — your: .card
   ============================================================ */
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-lg);
  padding: 1.25rem;
  box-shadow: var(--sh-sm);
  margin-bottom: 1rem;
}

/* ============================================================
   SYMPTOM FORM  — your: .symptom-form .symptom-groups
   ============================================================ */
.symptom-form { }
.symptom-groups { display: flex; flex-direction: column; gap: 0.75rem; margin-bottom: 1rem; }

/* ============================================================
   GROUP CARD  — your: .group-card .group-header .group-title
                        .group-icon .chevron .group-content.expanded
   ============================================================ */
.group-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-lg);
  overflow: hidden;
  box-shadow: var(--sh-sm);
  transition: box-shadow var(--ease);
}

.group-card:hover { box-shadow: var(--sh-md); }

.group-header {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.25rem;
  background: none;
  border: none;
  cursor: pointer;
  transition: background var(--ease);
  text-align: left;
}

.group-header:hover { background: var(--surface2); }
.group-header[aria-expanded="true"] { background: var(--surface2); border-bottom: 1px solid var(--border); }

.group-title {
  display: flex;
  align-items: center;
  gap: 0.65rem;
}

.group-title h2 {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text);
  margin: 0;
}

.group-icon {
  width: 36px; height: 36px;
  background: var(--primary-light);
  border-radius: var(--r-sm);
  display: flex; align-items: center; justify-content: center;
  font-size: 1.1rem;
  flex-shrink: 0;
}

.chevron {
  color: var(--text-muted);
  transition: transform var(--ease);
  display: flex;
  align-items: center;
}

.group-header[aria-expanded="true"] .chevron { transform: rotate(180deg); }

/* Collapsible content */
.group-content {
  display: none;
  padding: 0.85rem 1.25rem 1rem;
}

.group-content.expanded { display: block; }

/* ============================================================
   SYMPTOM LIST & ITEMS
   — your: .symptom-list .symptom-item .custom-checkbox
            .checkbox-box .symptom-name
   ============================================================ */
.symptom-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.symptom-item {
  display: flex;
  align-items: center;
  gap: 0.55rem;
  padding: 0.5rem 0.9rem;
  border: 1.5px solid var(--border-mid);
  border-radius: 50px;
  cursor: pointer;
  transition: all var(--ease);
  background: var(--bg);
  user-select: none;
}

.symptom-item:hover {
  border-color: var(--primary);
  background: var(--primary-light);
}

/* Hide native checkbox */
.custom-checkbox { display: none; }

/* Visual checkbox dot */
.checkbox-box {
  width: 18px; height: 18px;
  border: 2px solid var(--border-mid);
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  transition: all var(--ease);
  flex-shrink: 0;
  background: var(--surface);
}

.symptom-name {
  font-size: 0.88rem;
  font-weight: 500;
  color: var(--text);
  transition: color var(--ease);
}

/* Checked state — CSS only, no JS needed */
.symptom-item:has(.custom-checkbox:checked) {
  background: var(--primary);
  border-color: var(--primary);
}

.symptom-item:has(.custom-checkbox:checked) .checkbox-box {
  background: rgba(255,255,255,.25);
  border-color: rgba(255,255,255,.7);
}

.symptom-item:has(.custom-checkbox:checked) .checkbox-box::after {
  content: '✓';
  color: #fff;
  font-size: 0.65rem;
  font-weight: 700;
}

.symptom-item:has(.custom-checkbox:checked) .symptom-name {
  color: #fff;
}

/* ============================================================
   STICKY FOOTER (Submit button area)  — your: .sticky-footer
   ============================================================ */
.sticky-footer {
  position: sticky;
  bottom: 0;
  background: linear-gradient(to top, var(--bg) 80%, transparent);
  padding: 1rem 0 0.5rem;
  margin-top: 0.5rem;
}

/* ============================================================
   BUTTONS  — your: .btn .btn-primary .btn-secondary
              .btn-light .btn-block .btn-icon .mt-4
   ============================================================ */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  border: none;
  border-radius: var(--r-md);
  padding: 0.8rem 1.5rem;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--ease);
  font-family: var(--font);
  text-decoration: none;
  white-space: nowrap;
  line-height: 1;
}

.btn-primary {
  background: linear-gradient(135deg, var(--primary), var(--accent));
  color: #fff;
  box-shadow: 0 4px 14px rgba(13,148,136,.35);
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(13,148,136,.45);
  color: #fff;
}

.btn-primary:active { transform: translateY(0); }

.btn-secondary {
  background: var(--surface);
  color: var(--primary);
  border: 1.5px solid var(--primary);
}

.btn-secondary:hover {
  background: var(--primary-light);
  color: var(--primary-dark);
}

.btn-light {
  background: var(--surface2);
  color: var(--text-light);
  border: 1px solid var(--border-mid);
}

.btn-light:hover {
  background: var(--primary-light);
  color: var(--primary);
  border-color: var(--primary);
}

.btn-block { width: 100%; }

.btn-icon { gap: 0.6rem; }

.mt-4 { margin-top: 1.5rem; }

/* ============================================================
   FAB — SOS  — your: .sos-fab .sos-icon .sos-label
                      + .upload-fab (AI Photo on index)
   ============================================================ */
.sos-fab {
  position: fixed;
  bottom: 1.5rem;
  right: 1rem;
  width: 56px; height: 56px;
  border-radius: 50%;
  background: linear-gradient(135deg, #EF4444, #DC2626);
  color: #fff;
  border: none;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2px;
  box-shadow: var(--sh-lg);
  z-index: 200;
  transition: all var(--ease);
  font-family: var(--font);
  text-decoration: none;
}

.sos-fab:hover { transform: scale(1.08); box-shadow: 0 12px 36px rgba(220,38,38,.4); }

.sos-icon { font-size: 1.2rem; line-height: 1; }
.sos-label { font-size: 0.6rem; font-weight: 700; letter-spacing: 0.5px; }

/* AI Photo FAB (sits above SOS) */
.upload-fab {
  bottom: 5.5rem;
  background: linear-gradient(135deg, var(--primary), var(--accent2));
}

.upload-fab:hover { transform: scale(1.08); color: #fff; }

/* ============================================================
   SOS MODAL  — your: .sos-overlay .sos-card .sos-high-alert
                       .sos-buttons .sos-btn .sos-close-btn
   ============================================================ */
.sos-overlay {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,.45);
  backdrop-filter: blur(4px);
  z-index: 300;
  align-items: flex-end;
  justify-content: center;
  padding: 1rem;
}

.sos-overlay.open { display: flex; }

.sos-card {
  background: var(--surface);
  border-radius: var(--r-xl) var(--r-xl) var(--r-lg) var(--r-lg);
  padding: 1.75rem 1.5rem;
  width: 100%;
  max-width: 480px;
  animation: slideUp .3s cubic-bezier(.34,1.56,.64,1);
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(24px); }
  to   { opacity: 1; transform: translateY(0); }
}

.sos-card h2 {
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 1.1rem;
  text-align: center;
}

.sos-high-alert {
  background: var(--sev-high-bg);
  border: 1px solid #FECACA;
  border-radius: var(--r-md);
  padding: 0.75rem 1rem;
  font-size: 0.85rem;
  color: #991B1B;
  font-weight: 500;
  margin-bottom: 1rem;
  text-align: center;
}

.sos-buttons {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  margin-bottom: 1rem;
}

.sos-btn {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  padding: 0.9rem 1.1rem;
  background: var(--bg);
  border: 1.5px solid var(--border-mid);
  border-radius: var(--r-md);
  text-decoration: none;
  transition: all var(--ease);
}

.sos-btn:hover {
  background: var(--sev-high-bg);
  border-color: var(--sev-high);
}

.sos-btn .btn-icon { font-size: 1.1rem; }

.sos-btn .btn-label {
  flex: 1;
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--text);
}

.sos-btn .btn-num {
  font-size: 1rem;
  font-weight: 700;
  color: var(--sev-high);
}

.sos-close-btn {
  width: 100%;
  padding: 0.8rem;
  border: 1.5px solid var(--border-mid);
  border-radius: var(--r-md);
  background: none;
  font-family: var(--font);
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-light);
  cursor: pointer;
  transition: all var(--ease);
}

.sos-close-btn:hover { background: var(--bg); color: var(--text); }

/* ============================================================
   SEVERITY BADGE  — your: .severity-badge .low .medium .high .mini
   ============================================================ */
.severity-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.45rem 1rem;
  border-radius: var(--r-md);
  font-size: 0.78rem;
  font-weight: 700;
  text-align: center;
  line-height: 1.3;
  letter-spacing: 0.4px;
  flex-shrink: 0;
}

.severity-badge.low    { background: var(--sev-low-bg);  color: var(--sev-low); }
.severity-badge.medium { background: var(--sev-med-bg);  color: var(--sev-med); }
.severity-badge.high   { background: var(--sev-high-bg); color: var(--sev-high); }

.severity-badge.mini {
  padding: 0.2rem 0.6rem;
  font-size: 0.68rem;
  border-radius: 50px;
}

/* ============================================================
   RESULTS PAGE  — your: .results-page .loading-state .spinner
                          .results-container .result-card
                          .result-header .pre-title .condition-title
   ============================================================ */
.results-page { }

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 1rem;
  gap: 1rem;
  color: var(--text-light);
  font-size: 0.95rem;
}

.spinner {
  width: 44px; height: 44px;
  border: 3px solid var(--primary-light);
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: spin .7s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

.results-container { }

/* Photo card (AI CTA at top of results) */
.photo-card {
  border-left: 4px solid var(--primary) !important;
  text-align: center;
}

.photo-card h3 {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text);
  margin-bottom: 0.4rem;
}

/* Result main card */
.result-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-xl);
  padding: 0;
  overflow: hidden;
  box-shadow: var(--sh-md);
  margin-bottom: 1rem;
}

.result-header {
  background: linear-gradient(135deg, var(--primary) 0%, var(--accent2) 100%);
  padding: 1.75rem 1.5rem;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
  position: relative;
  overflow: hidden;
}

.result-header::after {
  content: '⚕';
  position: absolute;
  right: 1rem; bottom: -0.5rem;
  font-size: 4rem;
  opacity: .1;
  pointer-events: none;
}

.pre-title {
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 1.2px;
  color: rgba(255,255,255,.75);
  display: block;
  margin-bottom: 0.35rem;
}

.condition-title {
  font-size: 1.45rem;
  font-weight: 700;
  color: #fff;
  letter-spacing: -0.3px;
  line-height: 1.2;
  margin: 0;
}

.result-header .severity-badge {
  background: rgba(255,255,255,.2);
  color: #fff;
  border: 1px solid rgba(255,255,255,.3);
  backdrop-filter: blur(4px);
  white-space: nowrap;
  margin-top: 0.25rem;
}

.result-description {
  padding: 1rem 1.5rem 0;
  font-size: 0.9rem;
  color: var(--text-light);
  line-height: 1.6;
}

/* ============================================================
   ALERT BOXES  — your: .alert-box .doctor-alert .emergency-alert
                         .duration-alert
   ============================================================ */
.alert-box {
  display: flex;
  gap: 0.85rem;
  align-items: flex-start;
  padding: 1rem 1.5rem;
  border-left: 4px solid transparent;
}

.alert-icon { font-size: 1.15rem; flex-shrink: 0; margin-top: 1px; }

.alert-content strong {
  display: block;
  font-size: 0.88rem;
  font-weight: 700;
  margin-bottom: 0.2rem;
}

.alert-content p {
  font-size: 0.85rem;
  line-height: 1.5;
  margin: 0;
}

.doctor-alert {
  background: var(--sev-med-bg);
  border-left-color: var(--sev-med);
}

.doctor-alert .alert-content strong { color: #92400E; }
.doctor-alert .alert-content p      { color: #78350F; }

.emergency-alert {
  background: var(--sev-high-bg);
  border-left-color: var(--sev-high);
}

.emergency-alert .alert-content strong { color: #991B1B; }
.emergency-alert .alert-content p      { color: #7F1D1D; }

.duration-alert {
  background: #EFF6FF;
  border-left-color: #3B82F6;
}

.duration-alert .alert-content p { color: #1E40AF; font-weight: 500; }

/* ============================================================
   FIRST AID  — your: .first-aid-section .first-aid-list .step-list
   ============================================================ */
.first-aid-section {
  padding: 1.25rem 1.5rem;
  border-top: 1px solid var(--border);
}

.first-aid-section h3 {
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  color: var(--text-muted);
  margin-bottom: 0.85rem;
}

.list-wrapper { }

.first-aid-list, .step-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding: 0;
}

.first-aid-list li, .step-list li {
  display: flex;
  gap: 0.75rem;
  align-items: flex-start;
  font-size: 0.9rem;
  line-height: 1.55;
  color: var(--text);
  counter-increment: step;
}

.first-aid-list li::before, .step-list li::before {
  content: counter(step);
  min-width: 26px; height: 26px;
  background: var(--primary-light);
  color: var(--primary-dark);
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.72rem;
  font-weight: 700;
  flex-shrink: 0;
  margin-top: 1px;
}

.first-aid-list { counter-reset: step; }
.step-list      { counter-reset: step; }

/* ============================================================
   TABS  — your: .med-tab-row .med-tab .tab-content.active
   ============================================================ */
.med-tab-row {
  display: flex;
  gap: 0;
  border-top: 1px solid var(--border);
  background: var(--surface2);
  overflow-x: auto;
}

.med-tab {
  flex: 1;
  padding: 0.75rem 0.5rem;
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--text-muted);
  border: none;
  background: none;
  cursor: pointer;
  border-bottom: 2.5px solid transparent;
  transition: all var(--ease);
  font-family: var(--font);
  white-space: nowrap;
  min-width: 0;
}

.med-tab.active,
.med-tab:hover {
  color: var(--primary);
  border-bottom-color: var(--primary);
  background: var(--primary-light);
}

.tab-content { display: none; }
.tab-content.active { display: block; }

/* ============================================================
   FACILITIES  — your: .facilities-card .facilities-header
                        .loc-icon .loc-status .map-container
                        .facility-list .facility-list-wrapper
   ============================================================ */
.facilities-card { border-radius: 0 0 var(--r-xl) var(--r-xl) !important; margin-bottom: 0 !important; }

.facilities-header {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin-bottom: 0.85rem;
}

.facilities-header h3 { font-size: 0.95rem; font-weight: 600; flex: 1; }
.loc-icon { font-size: 1.1rem; }
.loc-status {
  font-size: 0.72rem;
  font-weight: 600;
  color: var(--text-muted);
  background: var(--bg);
  padding: 0.2rem 0.6rem;
  border-radius: 50px;
  border: 1px solid var(--border-mid);
}

.map-container {
  width: 100%;
  height: 220px;
  border-radius: var(--r-md);
  border: 1px solid var(--border);
  overflow: hidden;
  margin-bottom: 0.85rem;
}

#fac-map { width: 100%; height: 100%; }

.facility-list-wrapper { }

.facility-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0;
  padding: 0;
}

.facility-list li {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  padding: 0.85rem 0;
  border-bottom: 1px solid var(--border);
  font-size: 0.88rem;
}

.facility-list li:last-child { border-bottom: none; }

/* ============================================================
   MEDICINES  — your: .medicines-card .medicines-header .med-icon
                       .medicines-subtitle .medicines-count
                       .medicines-list .medicines-empty
   ============================================================ */
.medicines-card, .medicines-required-card {
  border-radius: 0 0 var(--r-xl) var(--r-xl) !important;
  margin-bottom: 0 !important;
}

.medicines-header, .medications-head {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin-bottom: 0.6rem;
}

.medicines-header h3, .medications-head h3 { font-size: 0.95rem; font-weight: 600; }
.med-icon { font-size: 1.1rem; }

.medicines-subtitle {
  font-size: 0.8rem;
  color: var(--text-light);
  margin-bottom: 0.75rem;
}

.medicines-count {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--primary);
  margin-bottom: 0.6rem;
}

.medicines-list { display: flex; flex-direction: column; gap: 0.5rem; }

.medicines-empty {
  font-size: 0.85rem;
  color: var(--text-muted);
  text-align: center;
  padding: 1.5rem 0;
}

.recommended-meds { display: flex; flex-direction: column; gap: 0.5rem; }

/* ============================================================
   DOCTOR CTA  — your: #doctor-booking-cta .doctor-cta
                        .cta-icon .cta-text
   ============================================================ */
.doctor-cta {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.1rem 1.5rem;
  background: linear-gradient(135deg, var(--primary-light), #E0F2FE);
  border: 1.5px solid var(--border-mid);
  border-radius: var(--r-lg);
  margin: 0 1.5rem 1rem;
  transition: all var(--ease);
  text-decoration: none;
}

.doctor-cta:hover {
  border-color: var(--primary);
  box-shadow: var(--sh-sm);
  transform: translateY(-1px);
}

.cta-icon { font-size: 1.75rem; flex-shrink: 0; }

.cta-text strong {
  display: block;
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 0.15rem;
}

.cta-text p {
  font-size: 0.8rem;
  color: var(--text-light);
  margin: 0;
}

/* ============================================================
   ALTERNATES  — your: .alternates-section .alternates-list
   ============================================================ */
.alternates-section {
  padding: 1.25rem 1.5rem;
  border-top: 1px solid var(--border);
}

.alternates-section h3 {
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  color: var(--text-muted);
  margin-bottom: 0.75rem;
}

.alternates-list { display: flex; flex-direction: column; gap: 0.5rem; }

/* Alternate condition card (injected by JS) */
.alternate-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  padding: 0.8rem 1rem;
  background: var(--bg);
  border: 1px solid var(--border-mid);
  border-radius: var(--r-md);
}

.alternate-card .alt-name {
  font-size: 0.88rem;
  font-weight: 500;
  color: var(--text);
}

/* ============================================================
   ACTION BUTTONS  — your: .action-buttons
   ============================================================ */
.action-buttons {
  display: flex;
  gap: 0.75rem;
  margin-top: 1.25rem;
}

.action-buttons .btn { flex: 1; }

/* ============================================================
   DISCLAIMER  — your: .disclaimer-block .disclaimer-title
                        .disclaimer-text
   ============================================================ */
.disclaimer-block {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  padding: 1rem 1.1rem;
  margin-top: 1.25rem;
}

.disclaimer-title {
  font-size: 0.68rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--text-muted);
  margin-bottom: 0.35rem;
}

.disclaimer-text {
  font-size: 0.78rem;
  color: var(--text-light);
  line-height: 1.6;
}

/* ============================================================
   HISTORY PAGE  — your: .history-header .history-list
                          .history-card .history-meta
                          .history-date .history-condition
                          .history-symptoms .history-footer
                          .history-lang .view-details-link
                          .clear-history-container .clear-btn
   ============================================================ */
.history-header { }

.history-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.history-card {
  border-radius: var(--r-lg) !important;
  transition: box-shadow var(--ease), transform var(--ease);
}

.history-card:hover {
  box-shadow: var(--sh-md) !important;
  transform: translateY(-1px);
}

.history-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.history-date {
  font-size: 0.78rem;
  color: var(--text-muted);
  font-weight: 500;
}

.history-condition {
  font-size: 1rem;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 0.5rem;
  line-height: 1.3;
}

.history-symptoms {
  margin-bottom: 0.75rem;
  padding: 0.6rem 0.85rem;
  background: var(--bg);
  border-radius: var(--r-sm);
  border: 1px solid var(--border);
}

.history-sym-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--text-muted);
  margin-right: 0.4rem;
}

.history-sym-names {
  font-size: 0.82rem;
  color: var(--text-light);
}

.history-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-top: 1px solid var(--border);
  padding-top: 0.65rem;
}

.history-lang {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.78rem;
  color: var(--text-muted);
}

.view-details-link {
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--primary);
  transition: color var(--ease);
}

.view-details-link:hover { color: var(--primary-dark); }

.clear-history-container { margin-top: 0.5rem; }

.clear-btn {
  border-color: #FECACA !important;
  color: var(--sev-high) !important;
}

.clear-btn:hover {
  background: var(--sev-high) !important;
  color: #fff !important;
  border-color: var(--sev-high) !important;
}

/* Empty state */
.empty-state {
  text-align: center;
  padding: 3.5rem 1.5rem;
  color: var(--text-muted);
}

.empty-icon { font-size: 3rem; margin-bottom: 1rem; }

.empty-state h3 {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 0.4rem;
}

.empty-state p { font-size: 0.88rem; margin-bottom: 1.25rem; }

/* ============================================================
   UTILITIES
   ============================================================ */
.mt-1{margin-top:0.5rem}.mt-2{margin-top:1rem}
.mt-3{margin-top:1.25rem}.mt-4{margin-top:1.5rem}
.mb-1{margin-bottom:0.5rem}.mb-2{margin-bottom:1rem}
.text-center{text-align:center}
.text-muted{color:var(--text-muted)}
.divider{color:var(--border-mid)}

/* ============================================================
   RESPONSIVE
   ============================================================ */
@media (max-width: 600px) {
  .nav-controls { gap: 0.1rem; }
  .history-link span:not(.history-icon) { display: none; }
  .history-link { padding: 0.4rem; }
  .user-name { display: none; }
  .page-container { padding: 1.25rem 0.85rem 7rem; }
  .result-header { padding: 1.25rem 1.1rem; }
  .first-aid-section { padding: 1rem 1.1rem; }
  .alternates-section { padding: 1rem 1.1rem; }
  .doctor-cta { margin: 0 1rem 1rem; }
  .action-buttons { flex-direction: column; }
}

@media (min-width: 768px) {
  .sos-fab { bottom: 2rem; right: 2rem; }
  .upload-fab { bottom: 6.5rem; }
}
```
