# AI QuizMaster 🎯

A dynamic AI-powered quiz platform built with Flask + OpenAI.

## Features
- User Registration and Login 🔐
- Dynamic Quiz Generation (OpenAI) 🧠
- Real-time Scoring System 🏆
- Leaderboard Tracking 📈
- Challenge a Friend via Email 📧
- Admin Panel for Approving Questions 🔒
- Category-based Quizzes 🎨
- Timed Quiz Mode (Optional) ⏱

## Tech Stack
- Backend: Flask (Python)
- Database: SQLite
- AI: OpenAI GPT API
- Frontend: HTML + Bootstrap 5
- Email: Flask-Mail (SMTP)

## Installation

```bash
git clone https://github.com/Nuraj250/ai_quizmaster.git
cd ai_quizmaster
python -m venv venv
source venv/bin/activate    # or venv\Scripts\activate on Windows
pip install -r requirements.txt
````

## Environment Setup

Create a `.env` file with:

```plaintext
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-api-key
DATABASE_URL=sqlite:///quizmaster.db

MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-email-password
```

## Running Locally

```bash
python app.py
```

---

## Folder Structure

```plaintext
ai_quizmaster/
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── database/
├── models/
├── services/
├── utils/
├── static/
└── templates/
```

---

## Future Improvements

* OAuth (Google/Facebook login)
* Timer with progress bar
* Leaderboard by country
* REST API for mobile apps