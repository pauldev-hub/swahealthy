# SwaHealthy 🏥
### Rural Health Companion for West Bengal

> Multilingual symptom checker with AI health assistant, mental wellness tools, and GPS-based facility finder — in Bengali, Hindi & English. Works offline.

---

### 📌 Version & Languages

![Version](https://img.shields.io/badge/version-2.0-blue?style=for-the-badge&logo=github&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776ab?style=for-the-badge&logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-f7df1e?style=for-the-badge&logo=javascript&logoColor=black)
![HTML5](https://img.shields.io/badge/HTML5-E34C26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

🔗 **Live App:** [https://swahealthy-1.onrender.com](https://swahealthy-1.onrender.com)

---

## 📑 Table of Contents

- [What is SwaHealthy?](#what-is-swahealthy)
- [⭐ Quick Stats](#-quick-stats)
- [Features](#features)
- [🎬 Demo & Screenshots](#-demo--screenshots)
- [Tech Stack](#tech-stack)
- [Run Locally](#run-locally)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Supported Languages](#supported-languages)
- [Contributing](#contributing)
- [License](#license)

---

## What is SwaHealthy?

SwaHealthy is a multilingual, offline-capable Progressive Web App (PWA) that helps rural and semi-urban residents in West Bengal check their symptoms, receive first-aid guidance, and find the nearest government health facility — all in their preferred language.

An independent project designed and built by **Pratyush**.

---

## ⭐ Quick Stats

| Feature | Count |
|---------|-------|
| 🏥 **Health Conditions** | 20+ |
| 🔍 **Symptoms Database** | 40+ |
| 🗺️ **West Bengal Facilities** | 10+ |
| 👨‍⚕️ **Sample Doctors** | 5+ |
| 🌍 **Languages Supported** | 3 (EN, BN, HI) |
| 📱 **Responsive Design** | Mobile-First |
| ⚡ **Offline Capability** | Full PWA Support |

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

## 🎬 Demo & Screenshots

Here's a visual walkthrough of SwaHealthy on mobile:

### 📱 **Splash & Loading**
![Loading Screen](./images/splash.jpeg)

---

### 📱 **Home & Symptom Selection**
![Home Screen](./images/Home.jpeg)

---

### 📱 **Diagnosis Results**
![Diagnosis Results](./images/Result.jpeg)

---

### 📱 **Duration Counter**
![Duration Counter](./images/Duration%20counter.jpeg)

---

### 📱 **Emergency Contacts (SOS)**
![Emergency Modal](./images/emergency.jpeg)

---

### 📱 **Facility Finder**
![Facility Finder](./images/Facility%20Finder.jpeg)

---

### 📱 **Mental Wellness & Mood Tracking**
![Mental Wellness](./images/Mental%20Wellness%20page.jpeg)

---

### 🤖 **AI Health Assistant (MindCare)**
![AI Assistant](./images/MindCare%20AI%20Assisstant.jpeg)

---

### 💬 **SwaHealthy AI Chat**
![AI Chat](./images/Swahealthy%20AI%20Chat%20Assisstant.jpeg)

---

### 🧠 **SwaHealthy Assistant Page**
![Assistant Page](./images/SwaHealthy%20Assitant%20Page.jpeg)

---

### 📅 **Doctor Appointments**
![Appointments](./images/Appointments.jpeg)

---

## Screenshots Overview

All screenshots showcase the app's key features:
- ✅ Loading & Splash screen
- ✅ Home with personalized greeting & symptom selection
- ✅ AI-powered diagnosis results with first-aid guidance
- ✅ Duration tracking for symptom monitoring
- ✅ Emergency SOS contacts (108, 100, 112, 1091)
- ✅ GPS-based facility finder for hospitals & Jan Aushadhi
- ✅ Mental wellness with mood tracking & journaling
- ✅ AI health assistant (MindCare) for symptom queries
- ✅ AI chat interface for health conversations
- ✅ Dedicated assistant page
- ✅ Doctor appointment booking system

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

---

## 🤝 Contributing

We welcome contributions! Whether it's bug fixes, new features, translations, or documentation improvements, your help makes SwaHealthy better.

### How to Contribute

1. **Fork** the repository
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes** and test thoroughly
4. **Commit** with clear messages: `git commit -m "Add feature: description"`
5. **Push** to your fork: `git push origin feature/your-feature-name`
6. **Open a Pull Request** with a description of your changes

### Areas We Need Help With

- 🌍 **Translations** — Add more languages or improve existing ones
- 🐛 **Bug Reports** — Report issues you find
- ✨ **Feature Requests** — Suggest improvements
- 📱 **UI/UX** — Design improvements and responsive fixes
- 📚 **Documentation** — Help improve README and comments
- 🧪 **Testing** — Write unit tests and integration tests

---

## 📜 License

SwaHealthy is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

You are free to use, modify, and distribute this project, as long as you include the original license and copyright notice.

---

## 🙏 Acknowledgments

- **Pratyush** — Creator & Developer
- **Groq** — AI Assistant API
- **OpenRouter** — Vision Model Integration
- **OpenStreetMap & Leaflet** — Mapping Services
- **West Bengal Health Department** — Public Health Data

---

## 📧 Contact & Support

For questions, feedback, or bug reports, please open an issue on [GitHub](https://github.com/pauldev-hub/swahealthy/issues).

**Created with ❤️ for rural health in West Bengal**