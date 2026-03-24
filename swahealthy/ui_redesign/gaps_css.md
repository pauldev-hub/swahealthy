# gaps_css.md
# File location: paste at the VERY BOTTOM of static/css/style.css
# Paste AFTER bottom_nav_css.md — this fills everything missing from the redesign
# 38 classes from original style.css that were not in style_css.md — all updated to teal system

```css
/* ============================================================
   GAPS v1.0 — Everything in original style.css not covered
   by style_css.md. All updated to teal design system.
   ============================================================ */

/* ============================================================
   FONT SWITCHING — body.font-bn / body.font-hi
   ============================================================ */
body.font-bn {
  font-family: 'Noto Sans Bengali', var(--font) !important;
}

body.font-hi {
  font-family: 'Noto Sans Devanagari', var(--font) !important;
}

/* ============================================================
   SOS PULSE ANIMATION
   ============================================================ */
@keyframes sos-pulse {
  0%   { box-shadow: 0 0 0 0 rgba(220, 38, 38, 0.7); }
  70%  { box-shadow: 0 0 0 14px rgba(220, 38, 38, 0); }
  100% { box-shadow: 0 0 0 0 rgba(220, 38, 38, 0); }
}

.sos-fab {
  animation: sos-pulse 2.2s ease-in-out infinite;
}

/* ============================================================
   FACILITY ITEMS — .facility-item .fac-name .fac-meta .fac-dist
   (used inside .facility-list on results page)
   ============================================================ */
.facility-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 0.85rem 0;
  border-bottom: 1px solid var(--border);
  gap: 0.75rem;
}

.facility-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.fac-name {
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--primary-dark);
  margin-bottom: 0.2rem;
}

.fac-meta {
  font-size: 0.78rem;
  color: var(--text-light);
  line-height: 1.4;
}

.fac-dist {
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--primary);
  background: var(--primary-light);
  padding: 0.25rem 0.65rem;
  border-radius: 50px;
  white-space: nowrap;
  flex-shrink: 0;
  border: 1px solid var(--border-mid);
}

/* ============================================================
   MEDICINE FACILITY CARDS
   .medicine-facility-card .med-card-header .med-card-info
   .med-fac-name .med-fac-meta .med-fac-dist
   .med-pills-wrap .med-pill .medicines-count
   ============================================================ */
.medicine-facility-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  padding: 0.85rem 1rem 0.75rem;
  margin-bottom: 0.75rem;
  box-shadow: var(--sh-sm);
  transition: box-shadow var(--ease);
}

.medicine-facility-card:hover {
  box-shadow: var(--sh-md);
}

.med-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 0.75rem;
  margin-bottom: 0.6rem;
}

.med-card-info {
  min-width: 0;
  flex: 1;
}

.med-fac-name {
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--primary-dark);
  margin-bottom: 0.15rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.med-fac-meta {
  font-size: 0.78rem;
  color: var(--text-light);
  line-height: 1.4;
}

.med-fac-dist {
  background: var(--primary-light);
  color: var(--primary-dark);
  font-size: 0.75rem;
  font-weight: 700;
  border-radius: 50px;
  padding: 0.2rem 0.65rem;
  white-space: nowrap;
  flex-shrink: 0;
  border: 1px solid var(--border-mid);
}

.med-pills-wrap {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
  margin-top: 0.5rem;
}

.med-pill {
  background: var(--primary-light);
  color: var(--primary-dark);
  border: 1px solid var(--border-mid);
  border-radius: 50px;
  font-size: 0.72rem;
  font-weight: 600;
  padding: 0.2rem 0.55rem;
}

/* ============================================================
   ALTERNATE ITEM — .alternate-item
   (old class name alias for .alternate-card)
   ============================================================ */
.alternate-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  padding: 0.8rem 1rem;
  background: var(--bg);
  border: 1px solid var(--border-mid);
  border-radius: var(--r-md);
  font-size: 0.88rem;
  font-weight: 500;
  color: var(--text);
}

/* ============================================================
   AI PHOTO UPLOAD — .photo-upload-card .upload-header
   .upload-desc .optional-tag #upload-prompt
   #photo-preview-container #photo-preview
   .photo-content-grid .photo-preview-thumbnail
   ============================================================ */
.photo-upload-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-lg);
  padding: 1.25rem;
  margin-bottom: 1rem;
  box-shadow: var(--sh-sm);
}

.upload-header {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  margin-bottom: 0.4rem;
}

.upload-header h3 {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text);
  margin: 0;
}

.optional-tag {
  font-size: 0.72rem;
  font-weight: 500;
  color: var(--text-muted);
  background: var(--bg);
  border: 1px solid var(--border-mid);
  padding: 0.1rem 0.5rem;
  border-radius: 50px;
  margin-left: 0.25rem;
}

.upload-desc {
  font-size: 0.82rem;
  color: var(--text-light);
  line-height: 1.5;
  margin-bottom: 0.85rem;
}

#upload-prompt {
  text-align: center;
  padding: 1.75rem 1rem;
}

#upload-prompt p {
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--text);
  margin: 0.5rem 0 0.25rem;
}

#upload-prompt small {
  font-size: 0.75rem;
  color: var(--text-muted);
}

#photo-preview-container {
  position: relative;
  display: inline-block;
  width: 100%;
  text-align: center;
}

#photo-preview {
  max-height: 220px;
  max-width: 100%;
  border-radius: var(--r-md);
  object-fit: contain;
  display: block;
  margin: 0 auto;
  box-shadow: var(--sh-sm);
  border: 1px solid var(--border);
}

.photo-content-grid {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1rem;
}

@media (min-width: 600px) {
  .photo-content-grid {
    flex-direction: row;
    align-items: flex-start;
  }
}

.photo-preview-thumbnail {
  flex-shrink: 0;
  width: 100%;
  max-width: 130px;
  margin: 0 auto;
}

.photo-preview-thumbnail img {
  width: 100%;
  height: 110px;
  object-fit: cover;
  border-radius: var(--r-md);
  border: 1px solid var(--border);
  box-shadow: var(--sh-sm);
}

/* ============================================================
   APPOINTMENTS EXTRAS
   .appt-days .appt-day-chip .appt-select-indicator
   .appt-lookup-row .appt-lookup-btn .appt-submit-btn
   ============================================================ */
.appt-days {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-top: 0.4rem;
}

.appt-day-chip {
  background: var(--primary-light);
  color: var(--primary-dark);
  font-size: 0.68rem;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 50px;
  border: 1px solid var(--border-mid);
}

.appt-select-indicator {
  font-size: 1.2rem;
  color: var(--border-mid);
  transition: color var(--ease);
  flex-shrink: 0;
}

.appt-doc-card.selected .appt-select-indicator {
  color: var(--primary);
}

.appt-lookup-row {
  display: flex;
  gap: 0.65rem;
  margin: 0.75rem 0 1.25rem;
}

.appt-lookup-row .appt-input {
  flex: 1;
}

.appt-lookup-btn {
  background: var(--primary);
  color: #fff;
  border: none;
  border-radius: var(--r-md);
  padding: 0.75rem 1.25rem;
  font-size: 0.9rem;
  font-weight: 700;
  cursor: pointer;
  font-family: var(--font);
  white-space: nowrap;
  transition: all var(--ease);
  flex-shrink: 0;
}

.appt-lookup-btn:hover {
  background: var(--primary-dark);
  transform: translateY(-1px);
}

/* Appointments submit — alias for btn btn-primary */
.appt-submit-btn {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  color: #fff;
  border: none;
  border-radius: var(--r-lg);
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  font-family: var(--font);
  transition: all var(--ease);
  box-shadow: 0 4px 14px rgba(13, 148, 136, 0.35);
  margin-top: 0.5rem;
}

.appt-submit-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(13, 148, 136, 0.45);
}

/* ============================================================
   APPOINTMENTS SUCCESS MODAL
   .appt-modal-bg .appt-modal-card .appt-modal-icon
   .appt-modal-title .appt-modal-msg .appt-modal-done-btn
   (separate from SOS overlay)
   ============================================================ */
.appt-modal-bg {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: none; /* toggled by JS */
  align-items: center;
  justify-content: center;
  z-index: 400;
  padding: 1.25rem;
  backdrop-filter: blur(4px);
}

/* JS sets display:flex to show */
.appt-modal-bg[style*="flex"] {
  animation: overlayFadeIn 0.2s ease;
}

@keyframes overlayFadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}

.appt-modal-card {
  background: var(--surface);
  border-radius: var(--r-xl);
  padding: 2.25rem 1.75rem;
  max-width: 360px;
  width: 100%;
  text-align: center;
  box-shadow: var(--sh-lg);
  border-top: 4px solid var(--primary);
  animation: slideUp 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.appt-modal-icon {
  font-size: 3.5rem;
  display: block;
  margin-bottom: 0.75rem;
}

.appt-modal-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--text);
  margin: 0 0 0.5rem;
  letter-spacing: -0.3px;
}

.appt-modal-msg {
  font-size: 0.88rem;
  color: var(--text-light);
  line-height: 1.6;
  margin: 0 0 1.5rem;
}

.appt-modal-done-btn {
  width: 100%;
  padding: 0.95rem;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  color: #fff;
  border: none;
  border-radius: var(--r-lg);
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  font-family: var(--font);
  transition: all var(--ease);
  box-shadow: 0 4px 14px rgba(13, 148, 136, 0.35);
}

.appt-modal-done-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(13, 148, 136, 0.45);
}

/* ============================================================
   DURATION RADIO BUTTONS — .duration-btn .btn-text
   (alternative radio style used in duration.html)
   ============================================================ */
.duration-btn {
  display: block;
  cursor: pointer;
  position: relative;
}

.duration-btn input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  width: 0;
  height: 0;
}

.duration-btn .btn-text {
  display: block;
  padding: 0.85rem 1rem;
  text-align: center;
  background: var(--bg);
  border: 1.5px solid var(--border-mid);
  border-radius: var(--r-md);
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--text-light);
  transition: all var(--ease);
}

.duration-btn:hover .btn-text {
  border-color: var(--primary);
  background: var(--primary-light);
  color: var(--primary);
}

.duration-btn input:checked + .btn-text {
  background: var(--primary);
  border-color: var(--primary);
  color: #fff;
  font-weight: 700;
  box-shadow: 0 4px 12px rgba(13, 148, 136, 0.3);
}

/* ============================================================
   MEDICINES DRAWER & FAB
   ============================================================ */
#medicines-fab {
  position: fixed;
  bottom: 5rem;
  left: 1rem;
  background: linear-gradient(135deg, #0D9488, #2DD4BF);
  color: #fff;
  border: none;
  border-radius: 50px;
  padding: 0.75rem 1.25rem;
  font-size: 0.88rem;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(13,148,136,.4);
  z-index: 200;
  font-family: var(--font);
  transition: all 0.2s ease;
}

#medicines-fab:hover { transform: translateY(-2px); }

#medicines-overlay {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,.45);
  backdrop-filter: blur(4px);
  z-index: 300;
}

#medicines-overlay.open { display: block; }

#medicines-drawer {
  position: fixed;
  bottom: -100%;
  left: 0; right: 0;
  background: var(--surface);
  border-radius: 24px 24px 0 0;
  padding: 1.5rem;
  z-index: 400;
  transition: bottom 0.35s cubic-bezier(.34,1.56,.64,1);
  max-height: 70vh;
  overflow-y: auto;
}

#medicines-drawer.open { bottom: 0; }

.drawer-handle {
  width: 40px; height: 4px;
  background: var(--border-mid);
  border-radius: 2px;
  margin: 0 auto 1.25rem;
}

.med-chip {
  display: inline-block;
  background: var(--primary-light);
  color: var(--primary-dark);
  border-radius: 50px;
  padding: 0.4rem 1rem;
  font-size: 0.85rem;
  font-weight: 600;
  margin: 0.25rem;
}

.drawer-disclaimer {
  font-size: 0.75rem;
  color: var(--text-muted);
  text-align: center;
  margin-top: 1rem;
  font-style: italic;
}
```