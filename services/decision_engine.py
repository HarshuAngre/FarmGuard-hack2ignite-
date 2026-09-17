def generate_recommendation(profile, weather, feedback_history=None):

    current = weather["current"]
    hourly = weather["hourly"]

    temperature = current["temperature_2m"]
    humidity = current["relative_humidity_2m"]
    precipitation = current["precipitation"]

    crop = profile["crop"]
    soil = profile["soil_type"]
    irrigation = profile["irrigation"]
    stage = profile["crop_stage"]

    crop_name = crop.lower().strip()
    soil_name = soil.lower().strip()
    irrigation_name = irrigation.lower().strip()
    stage_name = stage.lower().strip()

    rain_probabilities = hourly["precipitation_probability"][:6]
    rainfall_forecast = hourly["precipitation"][:6]

    max_rain_probability = max(rain_probabilities)
    expected_rainfall = sum(rainfall_forecast)

    reasons = []

    recent_overrides = []

    if feedback_history:

        for feedback in feedback_history:

            if feedback["decision"] == "Override":

                if feedback["reason"]:
                    recent_overrides.append(
                        feedback["reason"]
                    )

    crop_group = "general"

    if crop_name in [
        "wheat",
        "maize",
        "corn",
        "barley",
        "millet",
        "sorghum"
    ]:
        crop_group = "cereal"

    elif crop_name in [
        "rice",
        "paddy"
    ]:
        crop_group = "rice"

    elif crop_name in [
        "cotton"
    ]:
        crop_group = "cotton"

    elif crop_name in [
        "tomato",
        "potato",
        "onion",
        "chilli",
        "pepper",
        "vegetable",
        "vegetables"
    ]:
        crop_group = "vegetable"

    elif crop_name in [
        "sugarcane"
    ]:
        crop_group = "sugarcane"

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

        if crop_group == "rice":

            reasons.append(
                "Rice generally requires higher water availability, "
                "but upcoming rainfall may reduce the need for irrigation."
            )

        elif crop_group == "vegetable":

            reasons.append(
                "Vegetable crops can be sensitive to excess moisture, "
                "so unnecessary irrigation should be avoided."
            )

        elif crop_group == "cotton":

            reasons.append(
                "Upcoming rainfall may provide additional moisture "
                "for the cotton crop."
            )

        elif crop_group == "cereal":

            reasons.append(
                "The upcoming rainfall may provide useful moisture "
                "for the cereal crop."
            )

        if irrigation_name == "drip":

            reasons.append(
                "Drip irrigation allows precise water application, "
                "so unnecessary watering can be avoided."
            )

    elif max_rain_probability >= 50:

        recommendation = "Monitor upcoming rainfall before irrigating."
        confidence = "Moderate"

        reasons.append(
            f"Rain probability reaches {max_rain_probability}% "
            "in the next few hours."
        )

        if soil_name == "clay":

            reasons.append(
                "Clay soil can retain moisture for longer periods."
            )

        elif soil_name == "sandy":

            reasons.append(
                "Sandy soil generally loses moisture more quickly."
            )

        if crop_group == "vegetable":

            reasons.append(
                "Vegetable crops may require closer moisture monitoring "
                "during changing weather conditions."
            )

        elif crop_group == "rice":

            reasons.append(
                "Rice generally has higher water requirements, "
                "so rainfall should be considered before irrigation."
            )

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

        if crop_group == "vegetable":

            reasons.append(
                "Vegetable crops can be sensitive to prolonged "
                "wet conditions."
            )

        elif crop_group == "cotton":

            reasons.append(
                "Wet conditions should be monitored closely "
                "during cotton cultivation."
            )

    elif temperature >= 35:

        recommendation = "Check soil moisture before irrigation."
        confidence = "Moderate"

        reasons.append(
            f"Current temperature is {temperature}°C."
        )

        if soil_name == "sandy":

            reasons.append(
                "Sandy soil generally loses moisture more quickly."
            )

        if crop_group == "vegetable":

            reasons.append(
                "Vegetable crops may need closer soil-moisture "
                "monitoring during hot conditions."
            )

        elif crop_group == "cotton":

            reasons.append(
                "Hot conditions can increase crop water demand."
            )

        elif crop_group == "cereal":

            reasons.append(
                "Higher temperatures can increase moisture loss "
                "from the soil."
            )

    else:

        recommendation = "Check soil moisture before deciding on irrigation."
        confidence = "Low"

        reasons.append(
            "Current weather does not indicate a strong irrigation signal."
        )

        if crop_group == "rice":

            reasons.append(
                "Rice generally requires consistent water availability, "
                "so field moisture should be checked regularly."
            )

        elif crop_group == "vegetable":

            reasons.append(
                "Vegetable crops benefit from regular soil-moisture checks."
            )

        elif crop_group == "cereal":

            reasons.append(
                "Soil moisture should be checked according to the "
                "current growth stage."
            )

    if stage_name == "germination":

        reasons.append(
            "The crop is in the germination stage, when moisture "
            "conditions should be monitored carefully."
        )

    elif stage_name == "vegetative":

        reasons.append(
            "The crop is in the vegetative stage, so regular "
            "moisture monitoring is useful."
        )

    elif stage_name == "flowering":

        reasons.append(
            "The crop is in the flowering stage, making moisture "
            "management particularly important."
        )

    elif stage_name == "fruiting":

        reasons.append(
            "The crop is in the fruiting stage, so moisture "
            "conditions should be monitored closely."
        )

    elif stage_name == "harvesting":

        reasons.append(
            "The crop is in the harvesting stage, so field conditions "
            "should be checked before irrigation."
        )

    if recent_overrides:

        most_recent_reason = recent_overrides[0]

        reasons.append(
            f"Recent farmer feedback indicates: "
            f"{most_recent_reason}."
        )

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
def generate_farm_condition(profile, weather):

    current = weather["current"]
    hourly = weather["hourly"]

    temperature = current["temperature_2m"]
    humidity = current["relative_humidity_2m"]
    precipitation = current["precipitation"]

    rain_probabilities = hourly["precipitation_probability"][:6]
    rainfall_forecast = hourly["precipitation"][:6]

    max_rain_probability = max(rain_probabilities)
    expected_rainfall = sum(rainfall_forecast)

    soil = profile["soil_type"]
    crop = profile["crop"]
    stage = profile["crop_stage"]

    if max_rain_probability >= 70 and expected_rainfall >= 2:
        weather_status = "Rain expected"
        weather_detail = f"{max_rain_probability}% probability in the next 6 hours"

    elif max_rain_probability >= 50:
        weather_status = "Rain possible"
        weather_detail = f"{max_rain_probability}% probability in the next 6 hours"

    else:
        weather_status = "No strong rain signal"
        weather_detail = f"{max_rain_probability}% probability in the next 6 hours"

    if humidity >= 85 and precipitation > 0.5:
        moisture_status = "High moisture conditions"
        moisture_detail = f"Humidity is {humidity}% with recent precipitation"

    elif humidity >= 70:
        moisture_status = "Moderate moisture"
        moisture_detail = f"Humidity is {humidity}%"

    else:
        moisture_status = "Lower moisture"
        moisture_detail = f"Humidity is {humidity}%"

    return {
        "weather_status": weather_status,
        "weather_detail": weather_detail,
        "moisture_status": moisture_status,
        "moisture_detail": moisture_detail,
        "crop": crop,
        "stage": stage,
        "soil": soil
    }