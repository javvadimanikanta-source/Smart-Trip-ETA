from flask import Flask, render_template, request
import joblib
import pandas as pd
import sqlite3
from datetime import datetime

app = Flask(__name__)

model = joblib.load("model.pkl")


def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

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

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO predictions (
            distance, hour, minute, rounded_hour, month,
            weekday, passenger_count, predicted_duration, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
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
        rounded_hour=rounded_hour
    )


@app.route("/history")
def history():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT distance, hour, minute, rounded_hour, month,
               weekday, passenger_count, predicted_duration, created_at
        FROM predictions
        ORDER BY id DESC
    """)

    records = cursor.fetchall()
    conn.close()

    return render_template("history.html", records=records)


if __name__ == "__main__":
    app.run(debug=True)