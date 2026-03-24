# bottom_nav_css.md
# File location: paste at the VERY BOTTOM of static/css/style.css
# Paste AFTER missing_pages_css.md content — do not replace anything above

```css
/* ============================================================
   BOTTOM NAVIGATION BAR
   Targets: .bottom-nav .bottom-nav-item .bottom-nav-icon
            .bottom-nav-label + active state
   ============================================================ */

.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 64px;
  background: var(--surface);
  border-top: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-around;
  z-index: 150;
  box-shadow: 0 -4px 20px rgba(13, 148, 136, 0.08);
  padding: 0 0.5rem;
  padding-bottom: env(safe-area-inset-bottom); /* iPhone notch support */
}

.bottom-nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 3px;
  flex: 1;
  padding: 0.4rem 0.25rem;
  text-decoration: none;
  color: var(--text-muted);
  border-radius: var(--r-md);
  transition: all var(--ease);
  position: relative;
  min-width: 0;
}

.bottom-nav-item:hover {
  color: var(--primary);
  background: var(--primary-light);
}

.bottom-nav-item.active {
  color: var(--primary);
}

/* Active indicator dot above icon */
.bottom-nav-item.active::before {
  content: '';
  position: absolute;
  top: 2px;
  left: 50%;
  transform: translateX(-50%);
  width: 20px;
  height: 3px;
  background: linear-gradient(90deg, var(--primary), var(--accent2));
  border-radius: 99px;
}

.bottom-nav-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: var(--r-sm);
  transition: all var(--ease);
}

.bottom-nav-item.active .bottom-nav-icon {
  background: var(--primary-light);
  color: var(--primary);
}

.bottom-nav-item.active .bottom-nav-icon svg {
  stroke: var(--primary);
}

.bottom-nav-label {
  font-size: 0.65rem;
  font-weight: 600;
  letter-spacing: 0.2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 52px;
  text-align: center;
}

/* Push page content above bottom nav */
.main-content {
  padding-bottom: 72px;
}

/* SOS FAB sits above bottom nav */
.sos-fab {
  bottom: 5rem !important;
  right: 1rem !important;
}

/* AI upload FAB sits above SOS */
.upload-fab {
  bottom: 9rem !important;
  right: 1rem !important;
}

/* Hide old top nav links — bottom nav replaces them */
/* (The history-link items were removed from base.html already) */

/* Desktop: hide bottom nav, show as sidebar or nothing */
@media (min-width: 768px) {
  .bottom-nav {
    display: none;
  }
  .main-content {
    padding-bottom: 0;
  }
  .sos-fab {
    bottom: 2rem !important;
  }
  .upload-fab {
    bottom: 6.5rem !important;
  }
}
```