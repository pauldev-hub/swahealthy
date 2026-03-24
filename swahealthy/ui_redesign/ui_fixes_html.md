# ui_fixes_html.md
# These are targeted HTML/JS changes only
# Tell AntiGravity to apply these alongside ui_fixes_v1.md

---

## CHANGE 1 — Doctor avatars in appointments/appointments.html

Find the doctor card template block (inside {% for doc in doctors %}):

FIND:
```html
<div class="appt-doc-avatar">{{ doc.name[3] }}</div>
```

REPLACE WITH:
```html
<div class="appt-doc-avatar" data-name="{{ doc.name }}">
  <!-- Avatar injected by JS below -->
</div>
```

Then add this script BEFORE the closing </div> of .appt-page
(or just before the existing <script src="appointments.js"> line):

```html
<script>
// Assign male/female avatar based on doctor name
const FEMALE_NAMES = [
  'shampa','ananya','priya','sunita','rekha','kavita','meena','rita',
  'sita','lata','gita','mita','puja','rima','tina','nina','rina',
  'sneha','sudha','usha','asha','nisha','disha','swati','preeti',
  'shilpa','rupa','soma','mala','bela','hela','sima','dipa','riya',
  'tara','sara','maya','lila','kamla','ratna','shanta','aparna',
  'barnali','chandrima','debjani','esha','farida','gargi','hema',
  'indira','jayanti','kalyani','laboni','mamata','namita','oishi'
];

const MALE_SVG = `<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <circle cx="32" cy="22" r="13" fill="rgba(255,255,255,0.9)"/>
  <ellipse cx="32" cy="54" rx="20" ry="13" fill="rgba(255,255,255,0.9)"/>
</svg>`;

const FEMALE_SVG = `<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <circle cx="32" cy="20" r="13" fill="rgba(255,255,255,0.9)"/>
  <path d="M12 58 Q12 38 32 38 Q52 38 52 58" fill="rgba(255,255,255,0.9)"/>
  <path d="M22 44 Q20 50 18 56 Q25 54 32 54 Q39 54 46 56 Q44 50 42 44" fill="rgba(255,255,255,0.85)"/>
</svg>`;

document.querySelectorAll('.appt-doc-avatar[data-name]').forEach(el => {
  const name = el.getAttribute('data-name').toLowerCase();
  const firstName = name.split(' ')[1] || name.split(' ')[0]; // skip "Dr."
  const isFemale = FEMALE_NAMES.some(fn => firstName.includes(fn));
  el.innerHTML = isFemale ? FEMALE_SVG : MALE_SVG;

  // Alternate gradient colors per card for visual variety
  const idx = [...document.querySelectorAll('.appt-doc-avatar')].indexOf(el);
  const gradients = [
    'linear-gradient(135deg, #0D9488, #2DD4BF)',
    'linear-gradient(135deg, #0F766E, #14B8A6)',
    'linear-gradient(135deg, #115E59, #0D9488)',
    'linear-gradient(135deg, #134E4A, #0F766E)',
    'linear-gradient(135deg, #0D9488, #06B6D4)',
  ];
  el.style.background = gradients[idx % gradients.length];
});
</script>
```

---

## CHANGE 2 — Profile page hero in pages/profile.html

Find the opening of the profile page content. It likely looks like:

```html
<div class="profile-page-container">
  <div class="profile-card">
    <div class="profile-icon-wrapper">
      <span>...</span>
    </div>
    <h2>...</h2>
    <p>...</p>
```

REPLACE that entire opening section (up to but NOT including the form) with:

```html
<div class="profile-page-container">
  <div class="profile-card">

    <!-- Hero Banner -->
    <div class="profile-hero">
      <div class="profile-avatar-ring">
        <svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
          <circle cx="32" cy="22" r="13" fill="rgba(255,255,255,0.9)"/>
          <ellipse cx="32" cy="54" rx="20" ry="13" fill="rgba(255,255,255,0.9)"/>
        </svg>
      </div>
      <h2 class="profile-hero-title" data-i18n="my_health_profile">My Health Profile</h2>
      <p class="profile-hero-sub" data-i18n="profile_subtitle">Enter your age and gender to get more personalized health insights.</p>
    </div>

    <!-- Form Section -->
    <div class="profile-form-section">
```

Then at the very end of the form, before the closing `</div></div>` tags, add the logout button:

```html
      {% if session.get('user') %}
      <a href="/logout" class="profile-logout-btn">
        <svg viewBox="0 0 24 24"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
        <span data-i18n="logout">Logout</span>
      </a>
      {% endif %}

    </div><!-- end profile-form-section -->
```

IMPORTANT: Make sure you add one extra closing `</div>` to close `.profile-form-section`
and keep the existing `</div></div>` for `.profile-card` and `.profile-page-container`.

---

## CHANGE 3 — Remove logout from top navbar on mobile

In templates/base.html, the logout link is already inside `.user-profile`.
No change needed — it will be hidden naturally since `.user-name` is
hidden on mobile and the profile pic is tiny. The profile page logout
button replaces it functionally on mobile.

---

## JINJA2 SAFETY CHECK
After all changes verify:
- {{ doc.name }} still renders ✓
- {{ doc.doctor_id }} still renders ✓  
- {% for doc in doctors %} loop unchanged ✓
- {% if session.get('user') %} unchanged ✓
- /logout href unchanged ✓
- All data-i18n attributes preserved ✓