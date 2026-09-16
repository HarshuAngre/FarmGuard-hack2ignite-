from services.weather_service import get_coordinates, get_weather


location = "Pune"

coordinates = get_coordinates(location)

if coordinates is None:
    print("Location not found")
else:
    print("Location:")
    print(coordinates)

    weather = get_weather(
        coordinates["latitude"],
        coordinates["longitude"]
    )

    print("\nCurrent Weather:")
    print(weather["current"])