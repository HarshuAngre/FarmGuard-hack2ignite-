def generate_recommendation(profile, weather):
    current = weather["current"]
    hourly = weather["hourly"]

    temperature = current["temperature_2m"]
    humidity = current["relative_humidity_2m"]
    precipitation = current["precipitation"]

    crop = profile["crop"]
    soil = profile["soil_type"]
    irrigation = profile["irrigation"]
    stage = profile["crop_stage"]

    # Next 6 hours
    rain_probabilities = hourly["precipitation_probability"][:6]
    rainfall_forecast = hourly["precipitation"][:6]

    max_rain_probability = max(rain_probabilities)
    expected_rainfall = sum(rainfall_forecast)

    reasons = []

    # Strong rainfall conditions
    if max_rain_probability >= 70 and expected_rainfall >= 2:
        recommendation = "Consider delaying irrigation."
        confidence = "High"

        reasons.append(
            f"Rain probability reaches {max_rain_probability}% "
            "in the next few hours."
        )

        reasons.append(
            f"Expected rainfall is approximately "
            f"{expected_rainfall:.1f} mm."
        )

        if irrigation.lower() == "drip":
            reasons.append(
                "Drip irrigation allows precise water application, "
                "so delaying irrigation can help avoid unnecessary watering."
            )

    # Moderate rainfall
    elif max_rain_probability >= 50:
        recommendation = "Monitor upcoming rainfall before irrigating."
        confidence = "Moderate"

        reasons.append(
            f"Rain probability reaches {max_rain_probability}% "
            "in the next few hours."
        )

        if soil.lower() == "clay":
            reasons.append(
                "Clay soil can retain moisture for longer periods."
            )

    # High humidity
    elif humidity >= 85 and precipitation > 0.5:
        recommendation = "Monitor the crop for excess moisture."
        confidence = "Moderate"

        reasons.append(
            f"Current humidity is {humidity}%."
        )

        reasons.append(
            f"Current precipitation is {precipitation} mm."
        )

        reasons.append(
            "High humidity combined with recent precipitation "
            "may indicate increased moisture conditions."
        )

    # High temperature
    elif temperature >= 35:
        recommendation = "Check soil moisture before irrigation."
        confidence = "Moderate"

        reasons.append(
            f"Current temperature is {temperature}°C."
        )

        if soil.lower() == "sandy":
            reasons.append(
                "Sandy soil generally loses moisture more quickly."
            )

    # Normal conditions
    else:
        recommendation = "Check soil moisture before deciding on irrigation."
        confidence = "Low"

        reasons.append(
            "Current weather does not indicate a strong irrigation signal."
        )

    # Farm context
    reasons.append(
        f"The farm is growing {crop} in {soil} soil "
        f"using {irrigation} irrigation."
    )

    reasons.append(
        f"The crop is currently in the {stage} stage."
    )

    return {
        "recommendation": recommendation,
        "confidence": confidence,
        "reasons": reasons
    }