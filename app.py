import profile

from flask import Flask, render_template, request, redirect
import sqlite3
from services.weather_service import get_coordinates, get_weather
from services.decision_engine import generate_recommendation

app = Flask(__name__)

DATABASE = "farmguard.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_database():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS farm_profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_name TEXT NOT NULL,
            location TEXT NOT NULL,
            crop TEXT NOT NULL,
            farm_size REAL NOT NULL,
            soil_type TEXT NOT NULL,
            irrigation TEXT NOT NULL,
            crop_stage TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


@app.route("/")
def home():
    return render_template("profile.html")


@app.route("/save-profile", methods=["POST"])
def save_profile():

    farmer_name = request.form["farmer_name"]
    location = request.form["location"]
    crop = request.form["crop"]
    farm_size = request.form["farm_size"]
    soil_type = request.form["soil_type"]
    irrigation = request.form["irrigation"]
    crop_stage = request.form["crop_stage"]

    connection = get_db_connection()

    connection.execute("""
        INSERT INTO farm_profile
        (farmer_name, location, crop, farm_size, soil_type, irrigation, crop_stage)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        farmer_name,
        location,
        crop,
        farm_size,
        soil_type,
        irrigation,
        crop_stage
    ))

    connection.commit()
    connection.close()

    return redirect("/dashboard")
@app.route("/dashboard")

@app.route("/dashboard")
def dashboard():
    connection = get_db_connection()

    profile = connection.execute("""
        SELECT * FROM farm_profile
        ORDER BY id DESC
        LIMIT 1
    """).fetchone()

    connection.close()

    if profile is None:
        return redirect("/")

    weather = None
    coordinates = get_coordinates(profile["location"])

    if coordinates:
        weather = get_weather(
            coordinates["latitude"],
            coordinates["longitude"]
        )

    recommendation = None

    if weather:
        recommendation = generate_recommendation(profile, weather)

    return render_template(
        "dashboard.html",
        profile=profile,
        weather=weather,
        coordinates=coordinates,
        recommendation=recommendation
    )


if __name__ == "__main__":
    init_database()
    app.run(debug=True)