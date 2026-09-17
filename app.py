from flask import Flask, render_template, request, redirect
import sqlite3

from services.weather_service import get_coordinates, get_weather
from services.decision_engine import generate_recommendation, generate_farm_condition


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


    connection.execute("""
        CREATE TABLE IF NOT EXISTS farmer_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profile_id INTEGER NOT NULL,
            recommendation TEXT NOT NULL,
            decision TEXT NOT NULL,
            reason TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
        (
            farmer_name,
            location,
            crop,
            farm_size,
            soil_type,
            irrigation,
            crop_stage
        )
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
def dashboard():

    feedback_status = request.args.get("feedback")

    connection = get_db_connection()

    profile = connection.execute("""
        SELECT *
        FROM farm_profile
        ORDER BY id DESC
        LIMIT 1
    """).fetchone()


    if profile is None:
        connection.close()
        return redirect("/")

    feedback_history = connection.execute("""
        SELECT *
        FROM farmer_feedback
        WHERE profile_id = ?
        ORDER BY id DESC
        LIMIT 5
    """, (profile["id"],)).fetchall()

    connection.close()


    weather = None
    weather_error = False
    coordinates = get_coordinates(profile["location"])

    if coordinates:
        weather = get_weather(
            coordinates["latitude"],
            coordinates["longitude"]
        )
        if weather is None:
            weather_error = True


    recommendation = None
    farm_condition = None
    rain_probability = None
    expected_rainfall = None

    if weather:

        recommendation = generate_recommendation(
            profile,
            weather,
            feedback_history
        )
        farm_condition = generate_farm_condition(
            profile,
            weather
        )

        rain_probability = max(
            weather["hourly"]["precipitation_probability"][:6]
        )

        # Expected rainfall during next 6 hours
        expected_rainfall = sum(
            weather["hourly"]["precipitation"][:6]
        )


    return render_template(
        "dashboard.html",

        profile=profile,

        weather=weather,

        coordinates=coordinates,

        recommendation=recommendation,
        farm_condition=farm_condition,

        rain_probability=rain_probability,

        expected_rainfall=expected_rainfall,

        feedback_status=feedback_status,

        feedback_history=feedback_history,
        weather_error=weather_error,
    )



@app.route("/feedback", methods=["POST"])
def feedback():

    profile_id = request.form["profile_id"]

    recommendation = request.form["recommendation"]

    decision = request.form["decision"]

    reason = request.form.get("reason", "")


    connection = get_db_connection()

    connection.execute("""
        INSERT INTO farmer_feedback
        (
            profile_id,
            recommendation,
            decision,
            reason
        )
        VALUES (?, ?, ?, ?)
    """, (
        profile_id,
        recommendation,
        decision,
        reason
    ))

    connection.commit()
    connection.close()

    return redirect("/dashboard?feedback=saved")


if __name__ == "__main__":

    init_database()

    app.run(debug=True)