CampusHub

CampusHub is a clean and simple productivity dashboard for students.
It helps organize Tasks, Notes, and Resources all in one place, making academic life easier to manage.
This project is my final submission for CS50x.

Features
1. User Authentication
Register / Login / Logout
Secure password hashing
Session-based login
2. Dashboard
14-day task completion graph (Chart.js)
Quick productivity stats
Modern Bootstrap UI
3. Tasks
Add, delete, mark complete
Deadlines + categories
Auto-updating progress graph
Smooth AJAX interactions (no page reload)
4. Notes
Create and delete personal notes
Clean minimal note-taking interface
5. Resources
Track books, videos, courses, movies, etc.
Status dropdown (Not Started → Completed)
AJAX updates + instant delete

Project Structure
campushub/
│
├── app.py               # Flask backend, routes, DB logic
├── schema.sql           # Database schema
├── requirements.txt     # Dependencies
│
├── instance/
│   └── campushub.db     # SQLite database
│
├── templates/           # HTML templates (Jinja2)
│   ├── layout.html
│   ├── dashboard.html
│   ├── tasks.html
│   ├── notes.html
│   ├── resources.html
│   ├── login.html
│   └── register.html
│
└── static/
    ├── styles.css
    ├── tasks.js
    ├── notes.js
    ├── resources.js
    └── dashboard.js