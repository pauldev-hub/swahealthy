# SwaHealthy 🏥
### Rural Health Companion for West Bengal

> Multilingual symptom checker with AI health assistant, mental wellness tools, and GPS-based facility finder — in Bengali, Hindi & English. Works offline.

🔗 **Live App:** [https://swahealthy-1.onrender.com](https://swahealthy-1.onrender.com)

---

## What is SwaHealthy?

SwaHealthy is a multilingual, offline-capable Progressive Web App (PWA) that helps rural and semi-urban residents in West Bengal check their symptoms, receive first-aid guidance, and find the nearest government health facility — all in their preferred language.

An independent project designed and built by **Pratyush**.

---

## Features

- **Symptom Checker** — Select symptoms by body area; rule-based engine matches 20+ conditions with weighted scoring
- **Severity Classification** — Color-coded results: 🟢 Low / 🟠 Medium / 🔴 High
- **AI Health Assistant** — Groq-powered Llama 3 chatbot answers health questions in real time
- **Photo Analysis** — Upload images of skin conditions, rashes, or wounds for AI-powered visual assessment via OpenRouter
- **Doctor Appointments** — Browse specialists, check availability, and book consultation slots
- **Mental Wellness** — PHQ-9 and GAD-7 assessments, mood tracking, journaling, and crisis detection
- **Facility Finder** — GPS-based map showing nearest PHCs, hospitals & Jan Aushadhi stores (Haversine distance)
- **Multilingual** — Full support for English, Bengali (বাংলা), and Hindi (हिंदी)
- **Offline PWA** — Works without internet after first load via Service Worker caching
- **Session History** — Last 10 checks stored locally; shareable summary for doctor visits
- **Emergency SOS** — One-tap access to 108 Ambulance, 100 Police, 112, and 1091 Women Helpline
- **User Profiles** — Google OAuth login with age/gender personalisation

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.10+ + Flask |
| Database | SQLite |
| Frontend | HTML5 + CSS3 + Vanilla JS |
| Maps | Leaflet.js + OpenStreetMap |
| AI Assistant | Groq API (Llama 3) |
| Photo Analysis | OpenRouter API (vision model) |
| Authentication | Google OAuth + Flask-Login |
| Offline | PWA Service Worker |
| Hosting | Render.com |

---

## Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/pauldev-hub/swahealthy.git
cd swahealthy/swahealthy

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python run.py
```

Then open your browser at `http://localhost:5000`

On first run, the database is automatically created and seeded with 40 symptoms, 20 conditions, 10 West Bengal facilities, and 5 sample doctors.

---

## Project Structure

```
swahealthy/
├── run.py                        # App entry point
├── config.py                     # Flask configuration
├── requirements.txt
├── backend/
│   ├── routes/
│   │   ├── main.py               # Core routes (diagnosis, facilities, history)
│   │   ├── auth.py               # Google OAuth login/logout
│   │   └── appointments.py       # Doctor booking endpoints
│   ├── models/
│   │   ├── schema.py             # Database schema
│   │   ├── helpers.py            # Haversine, DB utilities
│   │   └── seed.py               # Symptoms, conditions, doctors seed data
│   └── services/
│       ├── engine.py             # Rule-based diagnosis engine
│       └── photo_analyzer.py     # OpenRouter vision integration
└── frontend/
    ├── templates/
    │   ├── base.html             # Shared layout (nav, SOS, AI sheet)
    │   └── pages/
    │       ├── index.html        # Symptom selection
    │       ├── results.html      # Diagnosis results + facility map
    │       ├── history.html      # Past diagnoses
    │       ├── appointments.html # Doctor booking UI
    │       ├── ai_analysis.html  # Photo upload + AI analysis
    │       ├── wellness.html     # Mental health assessments
    │       └── profile.html      # User profile
    └── static/
        ├── css/style.css
        ├── js/app.js
        ├── js/translations.js    # i18n strings (EN/BN/HI)
        └── pwa/
            ├── manifest.json
            └── service-worker.js
```

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home — symptom selection |
| `/diagnose` | POST | Run symptom diagnosis |
| `/results` | GET | Diagnosis results page |
| `/facilities` | GET | Nearby hospitals + Jan Aushadhi |
| `/analyze-photo` | POST | AI photo analysis |
| `/chat` | POST | AI health assistant |
| `/history` | GET, DELETE | User diagnosis history |
| `/appointments` | GET | Browse doctors |
| `/book-appointment` | POST | Book a slot |
| `/wellness` | GET | Mental wellness page |
| `/wellness/phq9` | POST | PHQ-9 depression assessment |
| `/wellness/gad7` | POST | GAD-7 anxiety assessment |
| `/profile` | GET, POST | User profile |
| `/login` | GET | Google OAuth login |
| `/logout` | GET | Logout |

---

## Supported Languages

| Code | Language |
|------|----------|
| `en` | English (default) |
| `bn` | বাংলা — Bengali |
| `hi` | हिंदी — Hindi |

Language preference is stored in `localStorage` and applied to all UI labels, symptom names, condition names, and first-aid steps.

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
- [Groq API](https://groq.com)
- [OpenRouter](https://openrouter.ai)
