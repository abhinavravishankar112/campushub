import os
from flask import Flask, render_template, request, redirect, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from functools import wraps
from datetime import date, timedelta, datetime
from flask import flash

# Configure application
app = Flask(__name__)

# Ensure templates auto-reload
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (not cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# -----------------------------
# DATABASE CONNECTION FUNCTION
# -----------------------------
def get_db():
    conn = sqlite3.connect("instance/campushub.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


# -----------------------------
# LOGIN REQUIRED DECORATOR
# -----------------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# -----------------------------
# ROUTES
# -----------------------------

@app.route("/")
@login_required
def index():
    return redirect("/dashboard")


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return "Missing username or password"

        db = get_db()

        # Check if username exists
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if user:
            return "Username already exists"

        hash_pw = generate_password_hash(password, method="pbkdf2:sha256")


        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hash_pw))
        db.commit()

        return redirect("/login")

    return render_template("register.html")


# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        if user is None or not check_password_hash(user["hash"], password):
            return "Invalid username or password"

        session["user_id"] = user["id"]
        return redirect("/dashboard")

    return render_template("login.html")


# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/tasks", methods=["GET"])
@login_required
def tasks_page():
    db = get_db()
    user_id = session["user_id"]
    rows = db.execute(
        "SELECT * FROM tasks WHERE user_id = ? ORDER BY deadline IS NULL, deadline ASC, completed ASC", 
        (user_id,)
    ).fetchall()
    # convert rows to list of dicts for templating (sqlite3.Row works in Jinja, but explicit is fine)
    tasks = [dict(row) for row in rows]
    return render_template("tasks.html", tasks=tasks)


@app.route("/tasks/add", methods=["POST"])
@login_required
def tasks_add():
    title = request.form.get("title")
    description = request.form.get("description") or ""
    deadline = request.form.get("deadline") or None
    category = request.form.get("category") or "General"

    if not title:
        flash("Title is required.")
        return redirect("/tasks")

    db = get_db()
    db.execute(
        "INSERT INTO tasks (user_id, title, description, deadline, category, completed) VALUES (?, ?, ?, ?, ?, 0)",
        (session["user_id"], title, description, deadline, category)
    )
    db.commit()
    return redirect("/tasks")


@app.route("/tasks/toggle/<int:task_id>", methods=["POST"])
@login_required
def tasks_toggle(task_id):
    db = get_db()
    user_id = session["user_id"]

    row = db.execute("SELECT completed FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id)).fetchone()
    if not row:
        return jsonify({"success": False, "error": "Task not found"}), 404

    new_completed = 0 if row["completed"] else 1
    completed_at = datetime.now().isoformat(sep=' ', timespec='seconds') if new_completed else None

    db.execute(
        "UPDATE tasks SET completed = ?, completed_at = ? WHERE id = ? AND user_id = ?",
        (new_completed, completed_at, task_id, user_id)
    )
    db.commit()
    return jsonify({"success": True, "completed": bool(new_completed)})


@app.route("/tasks/delete/<int:task_id>", methods=["POST"])
@login_required
def tasks_delete(task_id):
    db = get_db()
    user_id = session["user_id"]
    db.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))
    db.commit()
    return jsonify({"success": True})


# Optional JSON endpoint to fetch tasks (useful for Chart or SPA work)
@app.route("/api/tasks", methods=["GET"])
@login_required
def api_tasks():
    db = get_db()
    user_id = session["user_id"]
    rows = db.execute("SELECT * FROM tasks WHERE user_id = ? ORDER BY deadline ASC", (user_id,)).fetchall()
    tasks = [dict(r) for r in rows]
    return jsonify(tasks)

@app.route("/progress-data")
@login_required
def progress_data():
    user_id = session["user_id"]
    db = get_db()

    # Fetch all completed tasks with a completion date
    rows = db.execute(
        """
        SELECT DATE(completed_at) as date, COUNT(*) as count
        FROM tasks
        WHERE user_id = ? AND completed = 1 AND completed_at IS NOT NULL
        GROUP BY DATE(completed_at)
        """,
        (user_id,)
    ).fetchall()

    # Convert rows -> dict { "2025-01-01": X, ... }
    counts = {row["date"]: row["count"] for row in rows}

    # Build last 14 days dataset
    labels = []
    values = []

    for i in range(13, -1, -1):
        d = (date.today() - timedelta(days=i)).isoformat()
        labels.append(d)
        values.append(counts.get(d, 0))

    return jsonify({"labels": labels, "values": values})

# NOTES FEATURE
@app.route("/notes", methods=["GET", "POST"])
@login_required
def notes_page():
    db = get_db()
    user_id = session["user_id"]

    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        if not title:
            flash("Title is required.")
            return redirect("/notes")

        db.execute(
            "INSERT INTO notes (user_id, title, content) VALUES (?, ?, ?)",
            (user_id, title, content)
        )
        db.commit()
        return redirect("/notes")

    # GET → Show all notes
    rows = db.execute(
        "SELECT * FROM notes WHERE user_id = ? ORDER BY id DESC",
        (user_id,)
    ).fetchall()

    notes = [dict(row) for row in rows]
    return render_template("notes.html", notes=notes)


@app.route("/notes/delete/<int:note_id>", methods=["POST"])
@login_required
def notes_delete(note_id):
    db = get_db()
    user_id = session["user_id"]

    db.execute("DELETE FROM notes WHERE id = ? AND user_id = ?", (note_id, user_id))
    db.commit()

    return jsonify({"success": True})

# RESOURCES FEATURE
@app.route("/resources", methods=["GET", "POST"])
@login_required
def resources_page():
    db = get_db()
    user_id = session["user_id"]

    if request.method == "POST":
        name = request.form.get("name")
        type_ = request.form.get("type") or "General"
        status = request.form.get("status") or "Not Started"

        if not name:
            flash("Resource name is required.")
            return redirect("/resources")

        db.execute(
            "INSERT INTO resources (user_id, name, type, status) VALUES (?, ?, ?, ?)",
            (user_id, name, type_, status)
        )
        db.commit()
        return redirect("/resources")

    rows = db.execute(
        "SELECT * FROM resources WHERE user_id = ? ORDER BY id DESC",
        (user_id,)
    ).fetchall()

    resources = [dict(r) for r in rows]
    return render_template("resources.html", resources=resources)


@app.route("/resources/update/<int:res_id>", methods=["POST"])
@login_required
def resources_update(res_id):
    db = get_db()
    user_id = session["user_id"]
    status = request.form.get("status")

    db.execute(
        "UPDATE resources SET status = ? WHERE id = ? AND user_id = ?",
        (status, res_id, user_id)
    )
    db.commit()

    return jsonify({"success": True})


@app.route("/resources/delete/<int:res_id>", methods=["POST"])
@login_required
def resources_delete(res_id):
    db = get_db()
    user_id = session["user_id"]

    db.execute("DELETE FROM resources WHERE id = ? AND user_id = ?", (res_id, user_id))
    db.commit()

    return jsonify({"success": True})
