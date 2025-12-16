# 📚 CampusHub

> A clean and intuitive productivity dashboard designed to help students manage their academic life efficiently.

CampusHub is a full-stack web application built with Flask that centralizes task management, note-taking, and resource tracking in one streamlined interface. This project was created as a final submission for **Harvard's CS50x** course.

---

## ✨ Features

### 🔐 User Authentication
- **Secure Registration & Login**: User accounts with password hashing using Werkzeug
- **Session Management**: Flask-Session for persistent, secure login sessions
- **Protected Routes**: Login-required decorator for secure access control

### 📊 Dashboard
- **Task Completion Visualization**: Interactive 14-day task completion graph powered by Chart.js
- **Productivity Statistics**: At-a-glance view of tasks, notes, and resources
- **Responsive Design**: Modern Bootstrap 5 UI that works on all devices

### ✅ Task Management
- **Complete Task Lifecycle**: Create, edit, complete, and delete tasks
- **Smart Organization**: Categorize tasks and set deadlines
- **Visual Progress**: Auto-updating completion graphs
- **Seamless UX**: AJAX-powered interactions without page reloads

### 📝 Notes
- **Quick Note-Taking**: Create and organize personal notes instantly
- **Clean Interface**: Minimal, distraction-free note editor
- **Easy Management**: Delete notes with a single click

### 📖 Resources Tracker
- **Multi-Format Support**: Track books, videos, courses, movies, podcasts, and more
- **Status Tracking**: Monitor progress from "Not Started" to "Completed"
- **Instant Updates**: Real-time status changes and deletions via AJAX

---

## 🛠️ Technology Stack

- **Backend**: Python 3, Flask
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **UI Framework**: Bootstrap 5
- **Charts**: Chart.js
- **Session Management**: Flask-Session
- **Security**: Werkzeug (password hashing)

---

## 📁 Project Structure

```
campushub/
│
├── app.py                    # Flask application & route handlers
├── schema.sql                # Database schema (users, tasks, notes, resources)
├── README.md                 # Project documentation
│
├── instance/
│   └── campushub.db          # SQLite database (auto-generated)
│
├── flask_session/            # Session storage
│
├── templates/                # Jinja2 HTML templates
│   ├── layout.html          # Base template with navbar
│   ├── login.html           # Login page
│   ├── register.html        # Registration page
│   ├── dashboard.html       # Main dashboard with stats
│   ├── tasks.html           # Task management interface
│   ├── notes.html           # Note-taking interface
│   └── resources.html       # Resource tracking interface
│
└── static/                   # Static assets
    ├── styles.css           # Custom CSS styles
    ├── dashboard.js         # Dashboard chart logic
    ├── tasks.js             # Task AJAX operations
    ├── notes.js             # Notes AJAX operations
    └── resources.js         # Resources AJAX operations
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/campushub.git
   cd campushub
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install flask flask-session werkzeug
   ```

4. **Initialize the database**
   ```bash
   sqlite3 instance/campushub.db < schema.sql
   ```

5. **Run the application**
   ```bash
   flask run
   ```

6. **Open in browser**
   Navigate to `http://127.0.0.1:5000`

---

## 📖 Usage

1. **Register**: Create a new account on the registration page
2. **Login**: Sign in with your credentials
3. **Dashboard**: View your productivity overview and task completion trends
4. **Tasks**: Add tasks with deadlines and categories, mark them complete
5. **Notes**: Jot down quick notes for classes or ideas
6. **Resources**: Track your learning materials and their progress status

---

## 🗄️ Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `hash`: Hashed password

### Tasks Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `title`: Task name
- `description`: Task details
- `deadline`: Due date
- `category`: Task category
- `completed`: Boolean status (0/1)
- `completed_at`: Timestamp of completion

### Notes Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `title`: Note title
- `content`: Note body

### Resources Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `name`: Resource name
- `type`: Type (book, video, course, etc.)
- `status`: Progress status (Not Started, In Progress, Completed)

---

## 🎨 Design Choices

- **SQLite**: Chosen for simplicity and portability; easy to set up without external database servers
- **AJAX**: Implemented for smooth, single-page-application feel without full page reloads
- **Bootstrap**: Provides a professional, responsive UI with minimal custom CSS
- **Chart.js**: Simple yet powerful for visualizing task completion trends
- **Flask-Session**: Server-side sessions for better security compared to client-side cookies

---

## 🔮 Future Enhancements

- [ ] Task priority levels (High, Medium, Low)
- [ ] Note editing functionality
- [ ] Resource URL links and tags
- [ ] Calendar view for tasks
- [ ] Email reminders for upcoming deadlines
- [ ] Dark mode toggle
- [ ] Export data (CSV/JSON)
- [ ] Mobile app version

---

## 🤝 Contributing

This is a personal educational project, but suggestions and feedback are welcome! Feel free to open an issue or submit a pull request.

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👨‍💻 Author

Created by **[Your Name]** as part of Harvard's CS50x final project.

- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- **CS50x**: Harvard's Introduction to Computer Science course
- **Flask Documentation**: Comprehensive guides and examples
- **Bootstrap**: For the responsive UI components
- **Chart.js**: For beautiful data visualization

---

**⭐ If you found this project helpful, please consider giving it a star!**