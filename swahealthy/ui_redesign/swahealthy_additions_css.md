# style_additions.css — Paste at the BOTTOM of your existing style.css
**File location:** `static/css/style.css`  
**Action:** Scroll to the very end of your existing style.css and paste everything below.

```css
/* ============================================================
   ADDITIONS v2.1 — Profile, AI Analysis, Appointments
   Paste at the bottom of static/css/style.css
   ============================================================ */

/* ============================================================
   PROFILE PAGE
   Targets: .profile-page-container .profile-card
            .profile-icon-wrapper .gender-options-grid
            .gender-option .option-content .form-control #save-msg
   ============================================================ */
.profile-page-container {
  background: linear-gradient(135deg, var(--bg) 0%, var(--primary-light) 100%) !important;
  margin: 0 !important;
  max-width: 100% !important;
  min-height: calc(100vh - 64px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
}

.profile-card {
  max-width: 460px !important;
  width: 100% !important;
  padding: 2.25rem !important;
  border-radius: var(--r-xl) !important;
  box-shadow: var(--sh-lg) !important;
  border: none !important;
  border-top: 4px solid var(--primary) !important;
  background: var(--surface) !important;
}

.profile-icon-wrapper {
  width: 80px !important;
  height: 80px !important;
  background: var(--primary-light) !important;
  border-radius: 50% !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  margin: 0 auto 1.25rem !important;
}

.profile-card h2 {
  font-size: 1.4rem !important;
  font-weight: 700 !important;
  color: var(--text) !important;
  letter-spacing: -0.3px !important;
}

.profile-card p {
  color: var(--text-light) !important;
  font-size: 0.88rem !important;
  margin-top: 0.4rem !important;
}

/* Form labels inside profile */
.profile-card label[data-i18n="age_label"],
.profile-card label[data-i18n="gender_label"] {
  display: block !important;
  margin-bottom: 0.5rem !important;
  font-weight: 600 !important;
  font-size: 0.88rem !important;
  color: var(--text) !important;
}

/* Text inputs */
.form-control {
  width: 100%;
  padding: 0.75rem 1rem;
  border-radius: var(--r-md);
  border: 1.5px solid var(--border-mid);
  font-size: 0.95rem;
  font-family: var(--font);
  color: var(--text);
  background: var(--surface);
  transition: all var(--ease);
  outline: none;
}

.form-control:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(13,148,136,.12);
}

/* Gender grid */
.gender-options-grid {
  display: grid !important;
  grid-template-columns: 1fr 1fr !important;
  gap: 0.75rem !important;
}

.gender-option { cursor: pointer; }

.option-content {
  background: var(--bg) !important;
  border: 1.5px solid var(--border-mid) !important;
  padding: 0.85rem !important;
  border-radius: var(--r-md) !important;
  text-align: center !important;
  transition: all var(--ease) !important;
  font-weight: 500 !important;
  color: var(--text) !important;
  font-size: 0.9rem !important;
}

.gender-option:hover .option-content {
  border-color: var(--primary) !important;
  background: var(--primary-light) !important;
}

.gender-option input:checked + .option-content {
  background: var(--primary) !important;
  border-color: var(--primary) !important;
  color: #fff !important;
  font-weight: 700 !important;
  box-shadow: 0 4px 12px rgba(13,148,136,.3) !important;
}

/* Profile save button override */
.profile-card .btn-primary {
  padding: 1rem !important;
  font-size: 1rem !important;
  border-radius: var(--r-lg) !important;
  margin-top: 0.5rem !important;
}

/* Save success message */
#save-msg {
  text-align: center !important;
  margin-top: 0.85rem !important;
  color: var(--sev-low) !important;
  font-weight: 600 !important;
  font-size: 0.9rem !important;
  background: var(--sev-low-bg) !important;
  border-radius: var(--r-md) !important;
  padding: 0.65rem !important;
}

/* ============================================================
   AI ANALYSIS PAGE
   Targets: .photo-card .upload-area #ai-drop-zone
            #ai-upload-prompt .upload-icon
            #ai-photo-preview-container
            .photo-header .photo-details .photo-rec-box
            .photo-conditions-list .photo-disclaimer
            .remove-photo-btn
   ============================================================ */

/* Upload card override for AI page */
#ai-upload-card {
  max-width: 600px !important;
  margin: 0 auto 1rem !important;
}

.upload-area {
  border: 2.5px dashed var(--border-mid);
  border-radius: var(--r-lg);
  cursor: pointer;
  transition: all var(--ease);
  overflow: hidden;
  background: var(--bg);
}

.upload-area:hover {
  border-color: var(--primary);
  background: var(--primary-light);
}

#ai-upload-prompt {
  text-align: center;
  padding: 2.5rem 1.5rem;
}

.upload-icon {
  font-size: 3rem !important;
  display: block !important;
  margin-bottom: 1rem !important;
}

#ai-upload-prompt p {
  font-size: 0.92rem;
  color: var(--text-light);
  line-height: 1.6;
}

#ai-upload-prompt small {
  font-size: 0.78rem;
  color: var(--text-muted);
}

#ai-photo-preview-container {
  text-align: center !important;
  padding: 1.25rem !important;
}

#ai-photo-preview {
  max-width: 100%;
  max-height: 280px;
  border-radius: var(--r-md);
  object-fit: contain;
  box-shadow: var(--sh-sm);
}

/* Action buttons under upload */
#ai-action-buttons {
  display: flex !important;
  gap: 0.75rem !important;
  justify-content: center !important;
  padding: 0 0 1rem !important;
  margin-top: 0 !important;
}

#ai-action-buttons .btn { flex: 1; }

.remove-photo-btn {
  background: var(--sev-high-bg) !important;
  color: var(--sev-high) !important;
  border: 1.5px solid #FECACA !important;
}

.remove-photo-btn:hover {
  background: var(--sev-high) !important;
  color: #fff !important;
}

/* AI loading state */
#ai-loading-state {
  margin: 2.5rem 0 !important;
}

/* AI results card */
#ai-assessment-card {
  max-width: 600px !important;
  margin: 0 auto !important;
  border-left: 4px solid var(--primary) !important;
}

.photo-header {
  display: flex !important;
  justify-content: space-between !important;
  align-items: center !important;
  border-bottom: 1px solid var(--border) !important;
  padding-bottom: 1rem !important;
  margin-bottom: 1rem !important;
}

.photo-header h3 {
  font-size: 1rem;
  font-weight: 700;
  color: var(--text);
  margin: 0;
}

.photo-icon { font-size: 1.2rem; }

.photo-details p {
  font-size: 0.9rem;
  color: var(--text);
  line-height: 1.6;
}

.photo-details strong {
  font-weight: 700;
  color: var(--text);
}

.photo-conditions-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin: 0.6rem 0 1rem;
}

/* Condition chips injected by JS */
.photo-conditions-list span,
.photo-conditions-list div {
  background: var(--primary-light);
  color: var(--primary-dark);
  border-radius: 50px;
  padding: 0.25rem 0.75rem;
  font-size: 0.82rem;
  font-weight: 600;
}

.photo-rec-box {
  background: var(--primary-light) !important;
  padding: 1rem !important;
  border-radius: var(--r-md) !important;
  border-left: 4px solid var(--primary) !important;
  font-size: 0.88rem !important;
  line-height: 1.6 !important;
  color: var(--primary-dark) !important;
  display: flex;
  gap: 0.6rem;
  align-items: flex-start;
}

.rec-icon { font-size: 1rem; flex-shrink: 0; margin-top: 1px; }

.photo-disclaimer {
  margin-top: 1rem !important;
  text-align: center !important;
}

.photo-disclaimer small {
  font-size: 0.75rem;
  color: var(--text-muted);
  font-style: italic;
}

/* ============================================================
   APPOINTMENTS PAGE
   Targets: .appt-page .appt-hero .appt-hero-icon
            .appt-hero-title .appt-hero-sub
            .appt-tabs .appt-tab-btn .appt-tab-pane
            .appt-section .appt-section-title
            .appt-doctor-grid .appt-doc-card .appt-doc-avatar
            .appt-doc-info .appt-doc-name .appt-doc-spec
            .appt-date-input .appt-slots-grid .appt-hint
            .appt-form .appt-form-group .appt-input .appt-textarea
            .appt-my-card .status-badge .btn-cancel
   ============================================================ */
.appt-page {
  max-width: 520px;
  margin: 0 auto;
  padding: 0 1rem 7rem;
}

/* Hero */
.appt-hero {
  background: linear-gradient(135deg, var(--primary) 0%, var(--accent2) 100%);
  border-radius: var(--r-xl);
  padding: 1.5rem;
  margin: 1.25rem 0 1rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  color: #fff;
  position: relative;
  overflow: hidden;
}

.appt-hero::before {
  content: '';
  position: absolute;
  top: -20px; right: -20px;
  width: 100px; height: 100px;
  background: rgba(255,255,255,.08);
  border-radius: 50%;
}

.appt-hero-icon {
  font-size: 2rem;
  width: 52px; height: 52px;
  background: rgba(255,255,255,.2);
  border-radius: var(--r-md);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.appt-hero-title {
  font-size: 1.15rem;
  font-weight: 700;
  color: #fff;
  margin: 0 0 0.2rem;
  letter-spacing: -0.3px;
}

.appt-hero-sub {
  font-size: 0.82rem;
  color: rgba(255,255,255,.85);
  margin: 0;
  line-height: 1.4;
}

/* Tabs */
.appt-tabs {
  display: flex;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-lg);
  padding: 4px;
  gap: 4px;
  margin-bottom: 1.25rem;
  box-shadow: var(--sh-sm);
}

.appt-tab-btn {
  flex: 1;
  padding: 0.65rem 0.5rem;
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--text-muted);
  border: none;
  background: none;
  border-radius: var(--r-md);
  cursor: pointer;
  transition: all var(--ease);
  font-family: var(--font);
  white-space: nowrap;
}

.appt-tab-btn.active {
  background: var(--primary);
  color: #fff !important;
  border-bottom: none !important;
  box-shadow: 0 2px 8px rgba(13,148,136,.3);
}

.appt-tab-btn:not(.active):hover {
  background: var(--primary-light);
  color: var(--primary);
}

.appt-tab-pane { display: none; }
.appt-tab-pane.active { display: block; }

/* Section */
.appt-section {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-lg);
  padding: 1.25rem;
  margin-bottom: 1rem;
  box-shadow: var(--sh-sm);
}

.appt-section-title {
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  color: var(--text-muted);
  margin-bottom: 1rem;
}

/* Doctor grid */
.appt-doctor-grid {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.appt-doc-card {
  padding: 1rem;
  border: 1.5px solid var(--border-mid);
  border-radius: var(--r-md);
  cursor: pointer;
  transition: all var(--ease);
  background: var(--bg);
}

.appt-doc-card:hover {
  border-color: var(--primary);
  background: var(--primary-light);
  transform: translateY(-1px);
  box-shadow: var(--sh-sm);
}

.appt-doc-card.selected {
  border-color: var(--primary) !important;
  background: var(--primary-light) !important;
  box-shadow: 0 0 0 3px rgba(13,148,136,.15) !important;
}

.appt-doc-avatar {
  width: 44px; height: 44px;
  background: linear-gradient(135deg, var(--primary), var(--accent2));
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 1.1rem;
  font-weight: 700;
  flex-shrink: 0;
}

.appt-doc-info {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.appt-doc-name {
  font-size: 0.92rem;
  font-weight: 700;
  color: var(--text);
}

.appt-doc-spec {
  font-size: 0.78rem;
  color: var(--text-light);
  font-weight: 500;
}

/* Date input */
.appt-date-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1.5px solid var(--border-mid);
  border-radius: var(--r-md);
  font-size: 0.9rem;
  font-family: var(--font);
  color: var(--text);
  background: var(--surface);
  transition: all var(--ease);
  outline: none;
  margin-bottom: 1rem;
}

.appt-date-input:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(13,148,136,.12);
}

/* Slots */
.appt-slots-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.appt-slot-btn {
  padding: 0.5rem 1rem;
  border: 1.5px solid var(--border-mid);
  border-radius: 50px;
  background: var(--bg);
  cursor: pointer;
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--text);
  font-family: var(--font);
  transition: all var(--ease);
}

.appt-slot-btn:hover {
  border-color: var(--primary);
  background: var(--primary-light);
  color: var(--primary);
}

.appt-slot-btn.active {
  background: var(--primary) !important;
  color: #fff !important;
  border-color: var(--primary) !important;
  box-shadow: 0 2px 8px rgba(13,148,136,.3);
}

.appt-hint {
  font-size: 0.82rem;
  color: var(--text-muted);
  padding: 0.5rem 0;
  text-align: center;
  width: 100%;
}

/* Booking form */
.appt-form { }

.appt-form-group {
  margin-bottom: 1rem;
}

.appt-form-group label {
  display: block;
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--text);
  margin-bottom: 0.4rem;
}

.appt-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1.5px solid var(--border-mid);
  border-radius: var(--r-md);
  font-size: 0.9rem;
  font-family: var(--font);
  color: var(--text);
  background: var(--surface);
  transition: all var(--ease);
  outline: none;
}

.appt-input:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(13,148,136,.12);
}

.appt-textarea {
  resize: vertical;
  min-height: 90px;
}

/* My appointments cards */
.appt-my-card {
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--r-lg) !important;
  padding: 1rem 1.25rem !important;
  margin-bottom: 0.75rem !important;
  box-shadow: var(--sh-sm);
  transition: box-shadow var(--ease);
}

.appt-my-card:hover { box-shadow: var(--sh-md); }

/* Status badges */
.status-badge {
  font-size: 0.68rem;
  font-weight: 700;
  padding: 0.25rem 0.65rem;
  border-radius: 50px;
  text-transform: uppercase;
  letter-spacing: 0.4px;
}

.status-badge.pending   { background: var(--sev-med-bg); color: var(--sev-med); }
.status-badge.confirmed { background: var(--sev-low-bg); color: var(--sev-low); }
.status-badge.cancelled { background: var(--sev-high-bg); color: var(--sev-high); }

/* Cancel button */
.btn-cancel {
  background: none;
  border: 1.5px solid var(--sev-high);
  color: var(--sev-high);
  padding: 0.35rem 0.8rem;
  border-radius: var(--r-sm);
  cursor: pointer;
  font-size: 0.78rem;
  font-weight: 600;
  font-family: var(--font);
  transition: all var(--ease);
}

.btn-cancel:hover {
  background: var(--sev-high);
  color: #fff;
}

/* Step hidden */
.step-hidden { display: none !important; }

/* Success modal reuses .sos-overlay — already styled */
```
