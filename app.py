from flask import Flask, render_template, request

app = Flask(__name__)


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

    return f"""
    <h1>Farm Profile Saved!</h1>

    <p>Farmer: {farmer_name}</p>
    <p>Location: {location}</p>
    <p>Crop: {crop}</p>
    <p>Farm Size: {farm_size} acres</p>
    <p>Soil: {soil_type}</p>
    <p>Irrigation: {irrigation}</p>
    <p>Crop Stage: {crop_stage}</p>

    <br>
    <a href="/">Go Back</a>
    """


if __name__ == "__main__":
    app.run(debug=True)