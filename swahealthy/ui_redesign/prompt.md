# SwaHealthy — UI Redesign Super Prompt
# Place this file at: swahealthy/ui-redesign/PROMPT.md
# Usage in AntiGravity: "Follow the instructions in ui-redesign/PROMPT.md"

---

## YOUR ROLE/IDENTITY FOR THIS TASK

You are a frontend engineer applying a pre-designed CSS system to an existing Flask app.
You are NOT a designer. You are NOT a backend developer. You are a precise executor.
Your only job is to transfer a finished design onto existing HTML templates without
breaking a single line of Python, Jinja2, or JavaScript logic.

---

## ABSOLUTE RULES — READ BEFORE ANYTHING ELSE

These rules override every other instruction. If you feel tempted to break them,
you are wrong. Stop and re-read.

```
NEVER touch: app.py, db.py, engine.py, requirements.txt, any *.db file
NEVER modify: any {{ variable }}, {% tag %}, url_for(), form action, input name
NEVER rewrite: JavaScript logic in any .js file
NEVER add: new routes, new template variables, new Python imports
NEVER remove: existing HTML elements — only update their class attributes
NEVER assume: a class name — read the CSS file first, match exactly
NEVER proceed: if the app throws a 500 error — stop and fix before continuing
```

If the app ran before you started and does not run after you finish, you broke something.
Undo until it works, then try again more carefully.

---

## DESIGN VISION

The visual language is modern healthcare — calm, clinical confidence without sterility.

- **Palette**: Teal (#0D9488) primary on #F0FDFA mint background
- **Cards**: White surfaces with teal-tinted shadows floating on the mint background
- **Gradients**: 135deg teal→mint on CTAs, result headers, hero banners
- **Typography**: DM Sans (300/400/600/700 weights) for hierarchy; Noto Sans Bengali/Devanagari fallback
- **Interactive elements**: Pill-shaped chips, rounded toggles, tactile buttons
- **Motion**: translateY(-1px) hover lifts, slideUp modal, spinner for loading states
- **Severity system**: Green (low) / Amber (medium) / Red (high) — consistent on every screen
- **Trust**: Medical disclaimer always visible on results, no decorative elements without function

Think: a patient in rural West Bengal opening this on a low-end Android phone.
It must load fast, read clearly, and feel trustworthy in 3 seconds.

---

## STEP 1 — READ EVERYTHING BEFORE TOUCHING ANYTHING

Read these files in full before writing a single character:

```
ui-redesign/style_css.md          ← new CSS (this IS the design system)
ui-redesign/swahealthy_additions_css.md  ← additional CSS for new pages
ui-redesign/base_html_update.md   ← exact 2-line change for base.html
templates/base.html
templates/index.html
templates/results.html
templates/history.html
static/css/style.css              ← current CSS (read to understand existing structure)
```

Also read any of these if they exist:
```
templates/profile.html
templates/appointments.html
templates/ai_analysis.html
templates/admin.html
```

While reading templates, build a mental map of:
1. Every CSS class currently in use
2. Every Jinja2 variable and block
3. Every JavaScript hook (id="...", data-* attributes)

Do not start Step 2 until this map is complete.

---

## STEP 2 — REPLACE style.css

**Action**: Replace the ENTIRE contents of `static/css/style.css` with the CSS
found inside the triple-backtick code block in `ui-redesign/style_css.md`.

- Delete everything currently in the file
- Paste the new CSS exactly as written
- Do not add, remove, or modify a single character
- Do not add comments saying "added by AI" or similar

**Verify**: File should start with `/* ============= SwaHealthy — Professional UI v2.0`
and end with the `@media (min-width: 768px)` block.

---

## STEP 3 — APPEND additions CSS

**Action**: Open `static/css/style.css` (now containing Step 2 content).
Scroll to the very last line. Add one blank line. Then paste the ENTIRE contents
of the triple-backtick code block in `ui-redesign/swahealthy_additions_css.md`
starting from the next line.

- This is an APPEND — do not replace anything from Step 2
- The file should now contain Step 2 CSS + Step 3 CSS as one file
- Sections added cover: Profile page, AI Analysis page, Appointments page

**Verify**: The file should now end with `.step-hidden { display: none !important; }`
and the success modal comment line.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## STEP 3B — APPEND MISSING PAGES CSS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

After Step 3, scroll to the very bottom of static/css/style.css again
and APPEND the CSS from ui-redesign/missing_pages_css.md

Then do this one extra thing:
Open templates/pages/duration.html and DELETE the entire embedded
<style>...</style> block at the bottom of that file.
It conflicts with the design system. Remove it completely.
The Jinja2 logic above it is untouched — only remove the <style> block.

## STEP 3C — APPEND bottom_nav_css.md  
Append ui_redesign/bottom_nav_css.md to bottom of static/css/style.css

Also delete the <style> block from:
- templates/pages/duration.html
- templates/appointments/appointments.html
 ---

## STEP 4 — UPDATE base.html (2 CHANGES ONLY)

Read `ui-redesign/base_html_update.md`. It contains exactly 2 changes.
Make those 2 changes. Make NO other changes to base.html.

Change 1 — Google Fonts link (load DM Sans instead of Inter):
```html
<!-- FIND this line: -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+Bengali:wght@400;600;700&family=Noto+Sans+Devanagari:wght@400;600;700&display=swap" rel="stylesheet">

<!-- REPLACE with: -->
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700&family=Noto+Sans+Bengali:wght@400;500;600&family=Noto+Sans+Devanagari:wght@400;500;600&display=swap" rel="stylesheet">
```

Change 2 — Theme color meta tag:
```html
<!-- FIND: -->
<meta name="theme-color" content="#1D6A96">
<!-- REPLACE with: -->
<meta name="theme-color" content="#0D9488">
```

If either of these exact strings is not found, the current base.html may differ slightly.
In that case, find the nearest equivalent line and make the equivalent change.
Do NOT restructure or reformat base.html in any way.

---

## STEP 5 — FIX CLASS NAMES IN TEMPLATES

The CSS in Step 2+3 targets specific class names. Your job is to make the HTML
use those exact class names. You are changing `class="..."` attributes only.

**Golden rule**: If an element already has the correct class — leave it alone.
Only change what doesn't match. Never remove a class without replacing it with
the correct one from this list.

### GLOBAL (all pages)
| Element | Required class |
|---|---|
| Main page wrapper div | `page-container` |
| Page title h1 + subtitle p | inside `page-header` |
| Back arrow link | `back-link` |

### NAVBAR (base.html)
| Element | Required class |
|---|---|
| Language button group | `lang-toggle` |
| Each language button | `lang-btn` (JS adds `active`) |
| Nav links (History, etc.) | `history-link` |
| Icon inside nav link | `history-icon` |
| Login/register links | `auth-link` |
| Logout link | `auth-link logout-link` |

### INDEX PAGE — templates/index.html
| Element | Required class |
|---|---|
| Each collapsible body area wrapper | `group-card` |
| The toggle `<button>` inside it | `group-header` with `aria-expanded="true/false"` |
| Div holding icon + h2 inside button | `group-title` |
| Icon span/div inside group-title | `group-icon` |
| Chevron SVG/span inside button | `chevron` |
| Collapsible content div | `group-content` (JS adds `expanded` to open) |
| Symptom pills wrapper div | `symptom-list` |
| Each symptom `<label>` | `symptom-item` |
| `<input type="checkbox">` inside label | `custom-checkbox` |
| Visual circle span inside label | `checkbox-box` |
| Text span inside label | `symptom-name` |
| Div wrapping the submit button | `sticky-footer` |

### RESULTS PAGE — templates/results.html
| Element | Required class |
|---|---|
| Outer card wrapper | `result-card` |
| Gradient top band | `result-header` |
| Tiny uppercase label above condition name | `pre-title` |
| Condition name heading | `condition-title` |
| Severity indicator | `severity-badge` + one of: `low` `medium` `high` |
| "See a doctor" warning box | `alert-box doctor-alert` |
| Emergency warning box | `alert-box emergency-alert` |
| First aid section wrapper | `first-aid-section` |
| `<ol>` or `<ul>` of steps | `first-aid-list` OR `step-list` |
| Alternate conditions wrapper | `alternates-section` |
| List of alternates | `alternates-list` |
| Facilities card | `facilities-card` |
| Map container div | `map-container` |
| Map div itself | `fac-map` (id, not class) |
| Facility list | `facility-list` |
| Disclaimer wrapper | `disclaimer-block` |
| Disclaimer heading | `disclaimer-title` |
| Disclaimer text | `disclaimer-text` |
| Row of action buttons | `action-buttons` |

### HISTORY PAGE — templates/history.html
| Element | Required class |
|---|---|
| Outer list wrapper | `history-list` |
| Each history entry card | `history-card card` |
| Top row of card (date + badge) | `history-meta` |
| Date text | `history-date` |
| Condition name | `history-condition` |
| Symptoms display area | `history-symptoms` |
| Bottom row of card | `history-footer` |
| Language indicator | `history-lang` |
| "View details" link | `view-details-link` |
| Clear button wrapper | `clear-history-container` |
| Clear button | `btn btn-light clear-btn` |
| Empty state wrapper | `empty-state` |
| Icon in empty state | `empty-icon` |

### SOS EMERGENCY (base.html or wherever it lives)
| Element | Required class |
|---|---|
| Fixed floating button | `sos-fab` |
| Icon inside FAB | `sos-icon` |
| Label inside FAB | `sos-label` |
| Full-screen overlay | `sos-overlay` (JS adds `open`) |
| Modal box inside overlay | `sos-card` |
| Warning bar in modal | `sos-high-alert` |
| Button list in modal | `sos-buttons` |
| Each call button | `sos-btn` |
| Number text in button | `btn-num` |
| Close button | `sos-close-btn` |

### AI ANALYSIS PAGE — templates/ai_analysis.html (if exists)
| Element | Required class/id |
|---|---|
| Upload card | id `ai-upload-card` |
| Drop zone wrapper | `upload-area` |
| Prompt text inside zone | id `ai-upload-prompt` |
| Camera/upload icon | `upload-icon` |
| Preview image wrapper | id `ai-photo-preview-container` |
| Preview `<img>` | id `ai-photo-preview` |
| Analyze + Remove buttons row | id `ai-action-buttons` |
| Remove photo button | `remove-photo-btn` |
| Results card | id `ai-assessment-card` |
| Results header row | `photo-header` |
| Conditions chips wrapper | `photo-conditions-list` |
| Recommendation box | `photo-rec-box` |
| Disclaimer | `photo-disclaimer` |

### APPOINTMENTS PAGE — templates/appointments.html (if exists)
| Element | Required class |
|---|---|
| Page wrapper | `appt-page` |
| Hero banner | `appt-hero` |
| Hero icon | `appt-hero-icon` |
| Hero title | `appt-hero-title` |
| Hero subtitle | `appt-hero-sub` |
| Tab row | `appt-tabs` |
| Each tab button | `appt-tab-btn` (JS adds `active`) |
| Each tab panel | `appt-tab-pane` (JS adds `active`) |
| Section box | `appt-section` |
| Section label | `appt-section-title` |
| Doctor cards wrapper | `appt-doctor-grid` |
| Doctor card | `appt-doc-card` (JS adds `selected`) |
| Doctor avatar | `appt-doc-avatar` |
| Doctor name | `appt-doc-name` |
| Doctor specialty | `appt-doc-spec` |
| Date picker input | `appt-date-input` |
| Time slots wrapper | `appt-slots-grid` |
| Time slot button | `appt-slot-btn` (JS adds `active`) |
| No slots message | `appt-hint` |
| Booking form | `appt-form` |
| Form field group | `appt-form-group` |
| Text/select inputs | `appt-input` |
| Textarea | `appt-input appt-textarea` |
| Booked appointment card | `appt-my-card` |
| Status badge | `status-badge` + `pending` OR `confirmed` OR `cancelled` |
| Cancel button | `btn-cancel` |

### PROFILE PAGE — templates/profile.html (if exists)
| Element | Required class |
|---|---|
| Full-page background wrapper | `profile-page-container` |
| Form card | `profile-card` |
| Avatar circle | `profile-icon-wrapper` |
| All text inputs | `form-control` |
| Gender options grid | `gender-options-grid` |
| Each gender radio label | `gender-option` |
| Visual tile inside label | `option-content` |
| Success message | id `save-msg` |

---

## STEP 6 — JINJA2 INTEGRITY VERIFICATION

After completing all template edits, run this mental checklist on EVERY file you touched:

```
□ Every {{ variable }} is byte-for-byte identical to before
□ Every {% for %}, {% if %}, {% block %}, {% extends %} is unchanged
□ Every url_for('route_name') is unchanged
□ Every form action="" and method="" is unchanged
□ Every input name="" and id="" used by JavaScript is unchanged
□ Every data-* attribute is unchanged
□ No new <script> tags were added
□ No existing <script> tags were removed or modified
□ No Flask route-linked href was changed
□ templates/auth/login.html — only class names changed, href="/google-login" unchanged
□ templates/pages/duration.html — <style> block removed, all Jinja2 and form logic intact
□ templates/appointments/appointments.html — <style> block removed, Jinja2 intact
If any box cannot be checked — fix it before proceeding.

---

## STEP 7 — BUTTONS AUDIT

Every button in the app should use one of these class combinations:

```
Primary action (submit, book, analyse): btn btn-primary btn-block
Secondary action (back, cancel, alt):   btn btn-secondary
Light action (clear, delete):           btn btn-light
Block width (full width):               add btn-block
With icon:                              add btn-icon
```

Check every `<button>` and `<a class="btn">` in every template. Update classes to match.
Do not change what the button does — only its class.

---

## STEP 8 — RUN AND VERIFY

```bash
py app.py
```

Open browser and check every page. For each page confirm:

**/ (Home)**
- [ ] Symptom pills display as rounded chips
- [ ] Selecting a symptom fills it teal with white text
- [ ] Language toggle buttons visible, active state works
- [ ] "Check Symptoms" button is sticky at bottom on mobile
- [ ] SOS button visible bottom-right

**/history**
- [ ] Cards render with date, condition, severity badge
- [ ] Empty state shows if no history (icon + message + button)
- [ ] Hover on card lifts slightly

**/results (after submitting symptoms)**
- [ ] Result card has teal-to-mint gradient header
- [ ] Condition name is large and white inside the header
- [ ] Severity badge is overlaid on the header (correct color)
- [ ] Doctor/emergency alert boxes appear if severity warrants
- [ ] First-aid steps have circular numbered counters
- [ ] Facility map renders
- [ ] Medical disclaimer is visible at bottom
- [ ] "Check Again" and "Save" buttons present

**SOS Modal**
- [ ] Clicking SOS FAB opens the overlay
- [ ] Emergency numbers visible and dialable
- [ ] Close button dismisses modal

**Language Switch**
- [ ] EN → বাংলা → हिंदी switches all visible text
- [ ] Active language button is highlighted teal

---

## WHAT DONE LOOKS LIKE

```
✓ #0D9488 teal is the dominant color on every screen
✓ DM Sans font renders throughout
✓ #F0FDFA mint background on every page
✓ Cards have white surface + teal-tinted shadow
✓ Symptom pills: teal fill + white text when checked (CSS :has selector, no JS needed)
✓ Result header: teal-to-mint gradient with ⚕ watermark
✓ Severity: green badges (low), amber (medium), red (high) — never mixed up
✓ Steps list: circular CSS counter bubbles, no images needed
✓ SOS FAB: red gradient, fixed position, always visible
✓ Mobile first: everything usable on 360px wide screen
✓ py app.py runs without errors
✓ No Jinja2 errors in terminal
✓ All features work identically to before the redesign
✓ Login page: centered card on mint background, Google button with teal hover glow
✓ Duration page: teal selected state on radio tiles, no inline styles fighting the system
```

## VISUAL REFERENCE: 
Screenshots are attached. Every screen you produce must 
match the attached images pixel-for-pixel in layout, spacing, and color. 
If the CSS and the image conflict — the image wins.

---

## IF SOMETHING BREAKS

1. **500 error on a page**: You modified Jinja2. Revert that template and redo class names only.
2. **Styles not applying**: Class name mismatch. Compare HTML class vs CSS selector character by character.
3. **Font not loading**: Check the Google Fonts link in base.html matches Step 4 exactly.
4. **Map not showing**: You may have changed the `id="fac-map"` — restore it.
5. **Checkboxes not working**: You removed an `input name=""` or changed JS-linked IDs.
6. **Language not switching**: You modified the `lang-btn` JS click handlers or localStorage keys.

**When in doubt: revert the file, re-read the CSS, re-apply class names only.**

---

*CSS is the source of truth for design.*
*Flask/Jinja2 is the source of truth for data and logic.*
*They must never be mixed.*