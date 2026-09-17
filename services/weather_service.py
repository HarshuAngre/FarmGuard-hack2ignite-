import requests
import time


def get_coordinates(location):
    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": location,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()

    if "results" not in data or not data["results"]:
        return None

    result = data["results"][0]

    return {
        "latitude": result["latitude"],
        "longitude": result["longitude"],
        "name": result["name"],
        "country": result.get("country", "")
    }


def get_weather(latitude, longitude):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,

        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation",
            "wind_speed_10m"
        ],

        "hourly": [
            "temperature_2m",
            "precipitation_probability",
            "precipitation"
        ],

        "forecast_days": 3,
        "timezone": "auto"
    }

    # Try the API up to 3 times
    for attempt in range(3):

        try:

            response = requests.get(
                url,
                params=params,
                timeout=10
            )

            if response.status_code == 200:
                return response.json()

            # Temporary server error
            if response.status_code in [502, 503, 504]:

                if attempt < 2:
                    time.sleep(2)
                    continue

                return None

            response.raise_for_status()

        except requests.RequestException:

            if attempt < 2:
                time.sleep(2)
                continue

            return None

    return None