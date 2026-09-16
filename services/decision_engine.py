def generate_recommendation(profile, weather):
    current = weather["current"]

    temperature = current["temperature_2m"]
    humidity = current["relative_humidity_2m"]
    precipitation = current["precipitation"]

    crop = profile["crop"]
    soil = profile["soil_type"]
    irrigation = profile["irrigation"]
    stage = profile["crop_stage"]

    recommendation = "No immediate action required."
    reasons = []

    # Check current rainfall
    if precipitation > 0:
        recommendation = "Consider delaying irrigation."
        reasons.append("Rainfall is currently being recorded.")

    # High humidity
    elif humidity >= 85:
        recommendation = "Monitor the crop for excess moisture."
        reasons.append("High humidity may increase moisture-related crop risks.")

    # High temperature
    elif temperature >= 35:
        recommendation = "Consider checking soil moisture before irrigation."
        reasons.append("High temperature can increase water demand.")

    # Otherwise
    else:
        recommendation = "Check soil moisture before deciding on irrigation."
        reasons.append("Current weather conditions do not indicate an immediate irrigation requirement.")

    # Add farm-specific context
    reasons.append(
        f"The farm is growing {crop} in {soil} soil using {irrigation} irrigation."
    )

    reasons.append(
        f"The crop is currently in the {stage} stage."
    )

    return {
        "recommendation": recommendation,
        "reasons": reasons
    }