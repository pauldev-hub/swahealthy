# profile_consultation_css.md
# Append at the VERY BOTTOM of static/css/style.css

```css
/* ============================================================
   PROFILE DASHBOARD v2
   ============================================================ */

.profile-page-container {
  background: var(--bg) !important;
  padding: 0 !important;
  align-items: flex-start !important;
  min-height: calc(100vh - 64px);
}

.profile-card {
  max-width: 100% !important;
  border-radius: 0 !important;
  border: none !important;
  box-shadow: none !important;
  padding: 0 !important;
  background: var(--bg) !important;
  width: 100%;
}

/* Hero */
.profile-hero {
  background: linear-gradient(135deg, var(--primary) 0%, var(--accent2) 100%);
  padding: 2rem 1.5rem 4rem;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.profile-hero-deco1 {
  position: absolute;
  top: -30px; right: -30px;
  width: 140px; height: 140px;
  background: rgba(255,255,255,.08);
  border-radius: 50%;
  pointer-events: none;
}

.profile-hero-deco2 {
  position: absolute;
  bottom: -40px; left: -20px;
  width: 100px; height: 100px;
  background: rgba(255,255,255,.05);
  border-radius: 50%;
  pointer-events: none;
}

.profile-avatar-ring {
  width: 90px; height: 90px;
  border-radius: 50%;
  background: rgba(255,255,255,.2);
  border: 3px solid rgba(255,255,255,.5);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
  backdrop-filter: blur(4px);
  overflow: hidden;
}

.profile-avatar-ring svg {
  width: 54px; height: 54px;
}

.profile-hero-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #fff !important;
  margin: 0 0 0.25rem;
  letter-spacing: -0.3px;
}

.profile-hero-sub {
  font-size: 0.8rem;
  color: rgba(255,255,255,.75) !important;
  margin: 0 0 1.25rem;
}

/* Stats row */
.profile-stats-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0;
  background: rgba(255,255,255,.15);
  border-radius: var(--r-lg);
  padding: 0.75rem 1rem;
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255,255,255,.2);
  max-width: 280px;
  margin: 0 auto;
}

.profile-stat {
  flex: 1;
  text-align: center;
}

.profile-stat-value {
  display: block;
  font-size: 1.3rem;
  font-weight: 700;
  color: #fff;
  line-height: 1;
  margin-bottom: 0.2rem;
}

.profile-stat-label {
  font-size: 0.65rem;
  font-weight: 600;
  color: rgba(255,255,255,.75);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.profile-stat-divider {
  width: 1px;
  height: 32px;
  background: rgba(255,255,255,.25);
  flex-shrink: 0;
}

/* Form section */
.profile-form-section {
  background: var(--surface);
  border-radius: var(--r-xl) var(--r-xl) 0 0;
  margin-top: -1.75rem;
  padding: 1.75rem 1.25rem 6rem;
  position: relative;
  z-index: 1;
  box-shadow: 0 -4px 20px rgba(13,148,136,.08);
  min-height: 60vh;
}

.profile-section-label {
  font-size: 0.68rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--text-muted);
  margin-bottom: 1rem;
}

/* Field groups */
.profile-field-group {
  margin-bottom: 1.25rem;
}

.profile-field-label {
  display: block;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text);
  margin-bottom: 0.5rem;
}

.profile-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.profile-input-icon {
  position: absolute;
  left: 0.85rem;
  font-size: 1rem;
  pointer-events: none;
}

.profile-input {
  padding-left: 2.5rem !important;
  width: 100%;
  height: 48px;
  border: 1.5px solid var(--border-mid) !important;
  border-radius: var(--r-md) !important;
  font-size: 1rem !important;
  color: var(--text) !important;
  background: var(--bg) !important;
  transition: all var(--ease) !important;
}

.profile-input:focus {
  border-color: var(--primary) !important;
  box-shadow: 0 0 0 3px rgba(13,148,136,.12) !important;
  background: var(--surface) !important;
  outline: none !important;
}

/* Gender grid */
.gender-options-grid {
  display: grid !important;
  grid-template-columns: 1fr 1fr !important;
  gap: 0.65rem !important;
}

.gender-option { cursor: pointer; }

.option-content {
  background: var(--bg) !important;
  border: 1.5px solid var(--border-mid) !important;
  padding: 0.85rem 0.5rem !important;
  border-radius: var(--r-md) !important;
  text-align: center !important;
  transition: all var(--ease) !important;
  font-weight: 600 !important;
  font-size: 0.88rem !important;
  color: var(--text) !important;
  line-height: 1.3 !important;
}

.gender-option:hover .option-content {
  border-color: var(--primary) !important;
  background: var(--primary-light) !important;
}

.gender-option input:checked + .option-content {
  background: var(--primary) !important;
  border-color: var(--primary) !important;
  color: #fff !important;
  box-shadow: 0 4px 12px rgba(13,148,136,.3) !important;
}

/* Save button */
.profile-save-btn {
  padding: 1rem !important;
  font-size: 1rem !important;
  border-radius: var(--r-lg) !important;
  margin-top: 0.5rem !important;
  gap: 0.5rem !important;
}

/* Save message */
#save-msg {
  display: none;
  text-align: center;
  margin-top: 0.85rem;
  color: var(--sev-low);
  font-weight: 600;
  font-size: 0.88rem;
  background: var(--sev-low-bg);
  border-radius: var(--r-md);
  padding: 0.65rem;
}

/* Quick actions grid */
.profile-actions-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.65rem;
  margin-bottom: 1.25rem;
}

.profile-action-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  padding: 1rem 0.5rem;
  background: var(--bg);
  border: 1.5px solid var(--border);
  border-radius: var(--r-lg);
  text-decoration: none;
  transition: all var(--ease);
}

.profile-action-card:hover {
  border-color: var(--primary);
  background: var(--primary-light);
  transform: translateY(-2px);
  box-shadow: var(--sh-sm);
}

.profile-action-icon { font-size: 1.5rem; }

.profile-action-label {
  font-size: 0.72rem;
  font-weight: 600;
  color: var(--text);
  text-align: center;
}

/* App info section */
.profile-app-info {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--r-lg);
  overflow: hidden;
  margin-bottom: 1rem;
}

.profile-app-info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--border);
  font-size: 0.82rem;
}

.profile-app-info-row:last-child { border-bottom: none; }

.profile-app-info-row span:first-child {
  color: var(--text-light);
  font-weight: 500;
}

.profile-app-info-row span:last-child {
  color: var(--text);
  font-weight: 600;
}

/* Logout button */
.profile-logout-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.6rem;
  width: 100%;
  padding: 0.9rem;
  margin-top: 0.5rem;
  background: none;
  border: 1.5px solid #FECACA;
  border-radius: var(--r-lg);
  color: var(--sev-high) !important;
  font-size: 0.9rem;
  font-weight: 600;
  font-family: var(--font);
  cursor: pointer;
  transition: all var(--ease);
  text-decoration: none !important;
}

.profile-logout-btn:hover {
  background: var(--sev-high-bg);
  border-color: var(--sev-high);
  transform: translateY(-1px);
}

/* ============================================================
   CONSULTATION FLOATING WIDGET
   Sits above SOS, below AI Photo FAB
   ============================================================ */
.consult-fab {
  position: fixed;
  bottom: 9rem;
  right: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: linear-gradient(135deg, #7C3AED, #A855F7);
  color: #fff;
  border: none;
  border-radius: 999px;
  padding: 0.6rem 1rem 0.6rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 700;
  font-family: var(--font);
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(124,58,237,.4);
  z-index: 199;
  transition: all var(--ease);
  text-decoration: none;
  letter-spacing: 0.2px;
  animation: consultPulse 3s ease-in-out infinite;
}

.consult-fab:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 20px rgba(124,58,237,.5);
  color: #fff;
}

.consult-fab-icon { font-size: 1rem; flex-shrink: 0; }
.consult-fab-text { white-space: nowrap; }

@keyframes consultPulse {
  0%, 100% { box-shadow: 0 4px 16px rgba(124,58,237,.4); }
  50%       { box-shadow: 0 4px 24px rgba(124,58,237,.65); }
}

/* Stack order on mobile */
@media (max-width: 767px) {
  .consult-fab { bottom: 9rem; right: 1rem; }
  .upload-fab  { bottom: 12rem !important; }
}

@media (min-width: 768px) {
  .consult-fab { bottom: 10rem; right: 2rem; }
}
```