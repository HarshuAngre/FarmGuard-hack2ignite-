# FarmGuard

FarmGuard is a web-based farm decision support project developed for Hack2Ignite.

The application takes basic farm information such as crop, soil type,
irrigation method and crop growth stage. It also uses weather information
for the selected location.

The collected information is used to generate a simple recommendation
for the farmer.

## How it works

Farmer enters farm details
        ↓
Weather data is collected
        ↓
Current farm conditions are checked
        ↓
Decision engine processes the data
        ↓
FarmGuard gives a recommendation
        ↓
Farmer can accept or override it
        ↓
Feedback is saved

## Technologies Used

- Python
- Flask
- HTML
- CSS
- JavaScript
- SQLite
- Open-Meteo API

## Current Features

- Farm profile
- Location-based weather information
- Farm condition analysis
- Crop-specific recommendations
- Recommendation explanation
- Accept / Override feedback
- Farmer feedback history

## Future Work

- ML-based crop recommendation
- Soil pH and NPK based analysis
- Crop information for new farmers
- More localized agricultural data
