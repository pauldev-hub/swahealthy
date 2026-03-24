# ui_fixes_v1.md
# File location: paste at the VERY BOTTOM of static/css/style.css
# This is a targeted patch — append only, never replace

```css
/* ============================================================
   UI FIXES v1 — Modern widgets, doctor avatars, profile hero,
   bottom nav labels, logout button
   ============================================================ */

/* ============================================================
   MODERN SYMPTOM PILLS — crisper, more tactile
   ============================================================ */
.symptom-item {
  padding: 0.45rem 1rem !important;
  border-radius: 999px !important;
  border: 1.5px solid var(--border-mid) !important;
  background: var(--surface) !important;
  box-shadow: 0 1px 3px rgba(13,148,136,.06) !important;
  gap: 0.5rem !important;
  transition: all 0.15s ease !important;
}

.symptom-item:hover {
  border-color: var(--primary) !important;
  background: var(--primary-light) !important;
  box-shadow: 0 2px 8px rgba(13,148,136,.15) !important;
  transform: translateY(-1px) !important;
}

.symptom-item:has(.custom-checkbox:checked) {
  background: linear-gradient(135deg, var(--primary), var(--accent)) !important;
  border-color: transparent !important;
  box-shadow: 0 3px 10px rgba(13,148,136,.35) !important;
  transform: translateY(-1px) !important;
}

.symptom-name {
  font-size: 0.85rem !important;
  font-weight: 500 !important;
}

/* ============================================================
   MODERN GROUP CARDS — left accent on expand
   ============================================================ */
.group-card {
  border-radius: var(--r-lg) !important;
  border: 1px solid var(--border) !important;
  transition: all 0.2s ease !important;
}

.group-header[aria-expanded="true"] {
  border-bottom: 1px solid var(--border) !important;
}

/* Teal left accent bar when expanded */
.group-card:has(.group-content.expanded) {
  border-left: 3px solid var(--primary) !important;
  box-shadow: var(--sh-md) !important;
}

.group-icon {
  background: linear-gradient(135deg, var(--primary-light), #E0FDF4) !important;
  border-radius: var(--r-sm) !important;
  font-size: 1.2rem !important;
}

/* ============================================================
   BOTTOM NAV — fix truncated labels
   ============================================================ */
.bottom-nav-label {
  font-size: 0.58rem !important;
  max-width: 60px !important;
  letter-spacing: 0 !important;
}

.bottom-nav-item {
  gap: 2px !important;
  padding: 0.3rem 0.2rem !important;
}

/* ============================================================
   DOCTOR AVATARS — male/female SVG icons
   Male avatar via .appt-doc-avatar.male
   Female avatar via .appt-doc-avatar.female
   JS assigns the class based on name detection
   ============================================================ */
.appt-doc-avatar {
  width: 52px !important;
  height: 52px !important;
  border-radius: 50% !important;
  background: linear-gradient(135deg, var(--primary), var(--accent2)) !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  flex-shrink: 0 !important;
  overflow: hidden !important;
  box-shadow: 0 2px 8px rgba(13,148,136,.25) !important;
}

.appt-doc-avatar svg {
  width: 32px;
  height: 32px;
  fill: rgba(255,255,255,0.95);
}

/* Each doctor card more modern */
.appt-doc-card {
  border-radius: var(--r-lg) !important;
  border: 1.5px solid var(--border) !important;
  padding: 1rem 1.1rem !important;
  background: var(--surface) !important;
  box-shadow: var(--sh-sm) !important;
  transition: all 0.2s ease !important;
  gap: 1rem !important;
}

.appt-doc-card:hover {
  border-color: var(--primary) !important;
  background: var(--primary-light) !important;
  transform: translateY(-2px) !important;
  box-shadow: var(--sh-md) !important;
}

.appt-doc-card.selected {
  border-color: var(--primary) !important;
  background: var(--primary-light) !important;
  box-shadow: 0 0 0 3px rgba(13,148,136,.15), var(--sh-sm) !important;
}

.appt-doc-name {
  font-size: 0.95rem !important;
  font-weight: 700 !important;
  color: var(--text) !important;
}

.appt-doc-spec {
  font-size: 0.78rem !important;
  color: var(--primary) !important;
  font-weight: 600 !important;
  margin-top: 0.15rem !important;
}

/* ============================================================
   PROFILE PAGE HERO — proper header with avatar + banner
   ============================================================ */
.profile-page-container {
  padding: 0 !important;
  align-items: flex-start !important;
  background: var(--bg) !important;
}

.profile-card {
  max-width: 100% !important;
  border-radius: 0 !important;
  border-top: none !important;
  box-shadow: none !important;
  padding: 0 !important;
  background: var(--bg) !important;
}

/* Hero banner at top of profile */
.profile-hero {
  background: linear-gradient(135deg, var(--primary) 0%, var(--accent2) 100%);
  padding: 2rem 1.5rem 3.5rem;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.profile-hero::before {
  content: '';
  position: absolute;
  top: -30px; right: -30px;
  width: 140px; height: 140px;
  background: rgba(255,255,255,.08);
  border-radius: 50%;
}

.profile-hero::after {
  content: '';
  position: absolute;
  bottom: -40px; left: -20px;
  width: 100px; height: 100px;
  background: rgba(255,255,255,.05);
  border-radius: 50%;
}

.profile-avatar-ring {
  width: 88px;
  height: 88px;
  border-radius: 50%;
  background: rgba(255,255,255,.2);
  border: 3px solid rgba(255,255,255,.5);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
  backdrop-filter: blur(4px);
}

.profile-avatar-ring svg {
  width: 52px;
  height: 52px;
  fill: rgba(255,255,255,.9);
}

.profile-hero-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #fff;
  margin: 0 0 0.3rem;
  letter-spacing: -0.3px;
}

.profile-hero-sub {
  font-size: 0.82rem;
  color: rgba(255,255,255,.8);
  margin: 0;
  line-height: 1.5;
}

/* Form section below hero */
.profile-form-section {
  background: var(--surface);
  border-radius: var(--r-xl) var(--r-xl) 0 0;
  margin-top: -1.5rem;
  padding: 1.75rem 1.5rem 2rem;
  position: relative;
  z-index: 1;
  box-shadow: 0 -4px 20px rgba(13,148,136,.08);
  min-height: calc(100vh - 200px);
}

/* ============================================================
   LOGOUT BUTTON — profile page only
   ============================================================ */
.profile-logout-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.6rem;
  width: 100%;
  padding: 0.9rem;
  margin-top: 1.5rem;
  background: none;
  border: 1.5px solid #FECACA;
  border-radius: var(--r-lg);
  color: var(--sev-high);
  font-size: 0.9rem;
  font-weight: 600;
  font-family: var(--font);
  cursor: pointer;
  transition: all var(--ease);
  text-decoration: none;
}

.profile-logout-btn:hover {
  background: var(--sev-high-bg);
  border-color: var(--sev-high);
  color: var(--sev-high);
  transform: translateY(-1px);
}

.profile-logout-btn svg {
  width: 16px;
  height: 16px;
  stroke: currentColor;
  fill: none;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
}

/* ============================================================
   MODERN CARDS — general refresh
   ============================================================ */
.card {
  border-radius: var(--r-lg) !important;
  border: 1px solid var(--border) !important;
  box-shadow: var(--sh-sm) !important;
}

/* Result card modern header */
.result-header {
  padding: 1.5rem !important;
}

.condition-title {
  font-size: 1.35rem !important;
}

/* Modern alert boxes */
.alert-box {
  border-radius: var(--r-md) !important;
  margin: 0.75rem 1.25rem !important;
}

/* ============================================================
   APPOINTMENTS HERO — modern gradient
   ============================================================ */
.appt-hero {
  background: linear-gradient(135deg, var(--primary) 0%, var(--accent2) 100%) !important;
  border-radius: var(--r-xl) !important;
  box-shadow: var(--sh-md) !important;
}

.appt-hero-title {
  font-size: 1.2rem !important;
  letter-spacing: -0.3px !important;
}

/* Modern tab buttons */
.appt-tabs {
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--r-lg) !important;
  padding: 4px !important;
}

.appt-tab-btn {
  border-radius: var(--r-md) !important;
  font-size: 0.82rem !important;
}

.appt-tab-btn.active {
  background: var(--primary) !important;
  color: #fff !important;
  box-shadow: 0 2px 8px rgba(13,148,136,.3) !important;
}

/* Modern slot buttons */
.appt-slot-btn {
  border-radius: var(--r-md) !important;
  font-size: 0.82rem !important;
  padding: 0.6rem 0.5rem !important;
  border: 1.5px solid var(--border-mid) !important;
  transition: all 0.15s ease !important;
}

.appt-slot-btn:hover {
  border-color: var(--primary) !important;
  background: var(--primary-light) !important;
  color: var(--primary) !important;
}

.appt-slot-btn.active {
  background: linear-gradient(135deg, var(--primary), var(--accent)) !important;
  border-color: transparent !important;
  color: #fff !important;
  box-shadow: 0 3px 10px rgba(13,148,136,.35) !important;
}
```