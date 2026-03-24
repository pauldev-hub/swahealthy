# missing_pages_css.md
# File location: paste at the VERY BOTTOM of static/css/style.css
# Paste AFTER everything already in that file — do not replace anything above

```css
/* ============================================================
   LOGIN PAGE
   Targets: .login-container .login-card .google-login-btn .google-icon
   ============================================================ */

.login-container {
  min-height: calc(100vh - 64px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
  background: linear-gradient(135deg, var(--bg) 0%, var(--primary-light) 100%);
}

.login-card {
  width: 100%;
  max-width: 420px;
  background: var(--surface);
  border-radius: var(--r-xl);
  padding: 2.5rem 2rem;
  box-shadow: var(--sh-lg);
  border-top: 4px solid var(--primary);
  text-align: center;
  position: relative;
  overflow: hidden;
}

/* Decorative background circle */
.login-card::before {
  content: '⚕';
  position: absolute;
  top: -1rem;
  right: -0.5rem;
  font-size: 7rem;
  opacity: 0.04;
  pointer-events: none;
  line-height: 1;
}

.login-card h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text);
  letter-spacing: -0.4px;
  margin-bottom: 0.65rem;
  line-height: 1.25;
}

.login-card p {
  font-size: 0.88rem;
  color: var(--text-light);
  line-height: 1.65;
  margin-bottom: 2rem;
  padding: 0 0.5rem;
}

/* Divider line above button */
.login-card::after {
  content: '';
  display: block;
  width: 48px;
  height: 3px;
  background: linear-gradient(90deg, var(--primary), var(--accent2));
  border-radius: 99px;
  margin: 0 auto 1.75rem;
}

.google-login-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  width: 100%;
  padding: 0.9rem 1.5rem;
  background: var(--surface);
  border: 1.5px solid var(--border-mid);
  border-radius: var(--r-lg);
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text);
  font-family: var(--font);
  text-decoration: none;
  transition: all var(--ease);
  box-shadow: var(--sh-sm);
  position: relative;
  overflow: hidden;
}

.google-login-btn::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, var(--primary-light), transparent);
  opacity: 0;
  transition: opacity var(--ease);
}

.google-login-btn:hover {
  border-color: var(--primary);
  box-shadow: var(--sh-md);
  transform: translateY(-1px);
  color: var(--text);
}

.google-login-btn:hover::before {
  opacity: 1;
}

.google-login-btn:active {
  transform: translateY(0);
}

.google-icon {
  flex-shrink: 0;
  position: relative;
  z-index: 1;
}

/* Trust badge below button */
.login-trust {
  margin-top: 1.25rem;
  font-size: 0.75rem;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.35rem;
}

/* ============================================================
   DURATION PAGE
   Targets: .duration-page-container .duration-card
            .duration-icon-wrapper .duration-options-grid
            .duration-option .option-content .option-text
   ============================================================ */

.duration-page-container {
  background: linear-gradient(135deg, var(--bg) 0%, var(--primary-light) 100%) !important;
  margin: 0 !important;
  max-width: 100% !important;
  min-height: calc(100vh - 64px);
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  padding: 2rem 1rem !important;
}

.duration-card {
  max-width: 480px !important;
  width: 100% !important;
  padding: 2.25rem !important;
  border-radius: var(--r-xl) !important;
  box-shadow: var(--sh-lg) !important;
  border: none !important;
  border-top: 4px solid var(--primary) !important;
  background: var(--surface) !important;
  transition: none !important;
}

.duration-icon-wrapper {
  width: 72px !important;
  height: 72px !important;
  background: var(--primary-light) !important;
  border-radius: 50% !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  margin: 0 auto 1.25rem !important;
  font-size: 2rem !important;
}

.duration-card h2 {
  font-size: 1.35rem !important;
  font-weight: 700 !important;
  color: var(--text) !important;
  letter-spacing: -0.3px !important;
  line-height: 1.3 !important;
}

.duration-card > div > p {
  color: var(--text-light) !important;
  font-size: 0.88rem !important;
  margin-top: 0.4rem !important;
}

/* Duration options grid */
.duration-options-grid {
  display: grid !important;
  grid-template-columns: 1fr 1fr !important;
  gap: 0.75rem !important;
  margin-bottom: 1.75rem !important;
}

.duration-option {
  cursor: pointer;
}

/* Override duration's own .option-content
   (profile page shares this class — both get same treatment) */
.duration-option .option-content {
  background: var(--bg) !important;
  border: 1.5px solid var(--border-mid) !important;
  padding: 1rem !important;
  border-radius: var(--r-md) !important;
  text-align: center !important;
  transition: all var(--ease) !important;
  font-weight: 600 !important;
  color: var(--text) !important;
  font-size: 0.9rem !important;
}

.duration-option:hover .option-content {
  border-color: var(--primary) !important;
  background: var(--primary-light) !important;
  transform: translateY(-1px) !important;
}

.duration-option input:checked + .option-content {
  background: var(--primary) !important;
  border-color: var(--primary) !important;
  color: #fff !important;
  font-weight: 700 !important;
  box-shadow: 0 4px 12px rgba(13, 148, 136, 0.3) !important;
  transform: translateY(-1px) !important;
}

.option-text {
  font-size: 0.9rem;
  font-weight: 600;
  display: block;
}

/* Override duration's inline button style to match design system */
.duration-card .btn-primary {
  padding: 1rem !important;
  font-size: 1rem !important;
  font-weight: 700 !important;
  border-radius: var(--r-lg) !important;
  box-shadow: 0 4px 14px rgba(13, 148, 136, 0.35) !important;
}

.duration-card .btn-primary:hover {
  transform: translateY(-1px) !important;
  box-shadow: 0 6px 20px rgba(13, 148, 136, 0.45) !important;
}

.pulse-hover:hover {
  transform: translateY(-1px) !important;
  /* Override the scale() from inline — translateY matches design system */
}

/* Responsive */
@media (max-width: 480px) {
  .duration-card {
    padding: 1.5rem !important;
  }
  .duration-options-grid {
    grid-template-columns: 1fr !important;
  }
  .login-card {
    padding: 1.75rem 1.25rem;
  }
}
```