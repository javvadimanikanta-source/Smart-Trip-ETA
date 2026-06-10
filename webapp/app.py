from flask import Flask, render_template, request, redirect, url_for, session, flash
import joblib
import pandas as pd
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", "smarttrip_secret_key")

model = joblib.load("model.pkl")


def get_db():
    return sqlite3.connect("database.db")


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            distance REAL,
            hour INTEGER,
            minute INTEGER,
            rounded_hour INTEGER,
            month INTEGER,
            weekday INTEGER,
            passenger_count INTEGER,
            predicted_duration REAL,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


init_db()


@app.route("/")
def home():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("index.html", username=session["username"])


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip().lower()
        password = request.form["password"]

        password_hash = generate_password_hash(password)

        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            conn.commit()
            conn.close()

            flash("Account created successfully. Please login.")
            return redirect(url_for("login"))

        except sqlite3.IntegrityError:
            flash("Username already exists. Please choose another username.")
            return redirect(url_for("register"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip().lower()
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT password_hash FROM users WHERE username = ?",
            (username,)
        )
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[0], password):
            session["username"] = username
            return redirect(url_for("home"))

        flash("Invalid username or password.")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))


@app.route("/predict", methods=["POST"])
def predict():
    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]

    distance = float(request.form["distance"])
    hour = int(request.form["hour"])
    minute = int(request.form["minute"])
    month = int(request.form["month"])
    weekday = int(request.form["weekday"])
    passenger_count = int(request.form["passenger_count"])

    rounded_hour = hour

    if minute >= 30:
        rounded_hour += 1

    if rounded_hour == 24:
        rounded_hour = 0

    data = pd.DataFrame({
        "distance": [distance],
        "hour": [rounded_hour],
        "month": [month],
        "weekday": [weekday],
        "passenger_count": [passenger_count]
    })

    prediction = model.predict(data)[0]
    minutes = round(prediction / 60, 2)

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO predictions (
            username, distance, hour, minute, rounded_hour, month,
            weekday, passenger_count, predicted_duration, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        username,
        distance,
        hour,
        minute,
        rounded_hour,
        month,
        weekday,
        passenger_count,
        minutes,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    return render_template(
        "result.html",
        prediction=minutes,
        username=username
    )


@app.route("/history")
def history():
    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT distance, hour, minute, rounded_hour, month,
               weekday, passenger_count, predicted_duration, created_at
        FROM predictions
        WHERE username = ?
        ORDER BY id DESC
    """, (username,))

    records = cursor.fetchall()
    conn.close()

    return render_template(
        "history.html",
        records=records,
        username=username
    )


if __name__ == "__main__":
    app.run(debug=True)