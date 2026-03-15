# SwaHealthy 🏥
### Local Health Symptom Checker for West Bengal

> Rural health symptom checker in Bengali, Hindi & English. Find nearby clinics. Works offline.

🔗 **Live App:** [https://swahealthy-1.onrender.com](https://swahealthy-1.onrender.com)

---

## What is SwaHealthy?

SwaHealthy is a multilingual, offline-capable Progressive Web App (PWA) that helps rural and semi-urban residents in West Bengal check their symptoms, get first-aid guidance, and find the nearest government health facility — in their preferred language.

Built as a fun project by **Pratyush**.

---

## Features

- **Symptom Checker** — Select symptoms by body area; rule-based engine matches 20+ conditions
- **Severity Classification** — Color-coded results: 🟢 Low / 🟠 Medium / 🔴 High
- **Multilingual** — Full support for English, Bengali (বাংলা), and Hindi (हिंदी)
- **Facility Finder** — GPS-based map showing 5 nearest PHCs, hospitals & Jan Aushadhi stores
- **Offline PWA** — Works without internet after first load via Service Worker caching
- **Session History** — Last 10 checks stored locally; printable for doctor visits
- **Emergency Contacts** — Dial-able numbers shown for high-severity results

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3 + Flask |
| Database | SQLite |
| Frontend | HTML5 + CSS3 + Vanilla JS |
| Maps | Leaflet.js + OpenStreetMap |
| Offline | PWA Service Worker |
| Hosting | Render.com |

---

## Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/pauldev-hub/swahealthy.git
cd swahealthy

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py
```

Then open your browser at `http://localhost:5000`

---

## Project Structure

```
swahealthy/
├── app.py               # Flask routes
├── db.py                # SQLite init, seed data, Haversine formula
├── engine.py            # Rule-based diagnosis engine
├── requirements.txt
├── static/
│   ├── style.css
│   ├── app.js
│   ├── service-worker.js
│   └── manifest.json
└── templates/
    ├── base.html
    ├── index.html
    ├── results.html
    └── history.html
```

---

## Medical Disclaimer

> SwaHealthy is **not** a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified health provider for medical concerns.

---

## References

- [National Health Portal India](https://nhp.gov.in)
- [WHO First Aid Guidelines](https://who.int/health-topics/first-aid)
- [Government of West Bengal PHC Directory](https://wbhealth.gov.in)
- [Flask Documentation](https://flask.palletsprojects.com)
- [Leaflet.js](https://leafletjs.com)

---

*BCA Final Year Project • MAKAUT • 2026*
