from flask import Flask, request, render_template_string
import requests
import os
from dotenv import load_dotenv

# Load .env locally
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

app = Flask(__name__)

# --------------------------
# Fetch Weather Function
# --------------------------
def fetch_weather(city):
    if not API_KEY:
        return None, "API key is missing. Please set OPENWEATHER_API_KEY."

    params = {"q": city, "appid": API_KEY}

    try:
        resp = requests.get(BASE_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        # Temperature conversion
        kelvin = data["main"]["temp"]
        celsius = kelvin - 273.15
        fahrenheit = celsius * 9 / 5 + 32

        weather = {
            "city": data["name"],
            "country": data["sys"]["country"],
            "celsius": round(celsius, 1),
            "fahrenheit": round(fahrenheit, 1),
            "description": data["weather"][0]["description"].capitalize(),
        }

        return weather, None

    except requests.exceptions.HTTPError:
        if resp.status_code == 401:
            return None, "❌ API Error: Unauthorized. Your API key is invalid or incorrect."
        elif resp.status_code == 404:
            return None, "❌ City not found. Please check the spelling."
        else:
            return None, f"❌ HTTP Error: {resp.status_code}"

    except Exception:
        return None, "❌ Error fetching weather data. Please try again."


# --------------------------
# HTML Template
# --------------------------
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Weather App</title>
    <style>
        body { 
            font-family: Arial; 
            max-width: 600px; 
            margin: 40px auto; 
            padding: 20px;
        }
        input, button {
            padding: 10px; 
            font-size: 16px;
        }
        .result { margin-top: 20px; font-size: 20px; }
    </style>
</head>
<body>
    <h1>🌦️ Weather App</h1>

    <form method="POST">
        <input type="text" name="city" placeholder="Type a city..." required>
        <button type="submit">Get weather</button>
    </form>

    {% if error %}
        <p class="result">{{ error }}</p>
    {% endif %}

    {% if weather %}
        <div class="result">
            <p>📍 {{ weather.city }}, {{ weather.country }}</p>
            <p>🌡️ {{ weather.celsius }}°C / {{ weather.fahrenheit }}°F</p>
            <p>🌥️ {{ weather.description }}</p>
        </div>
    {% endif %}
</body>
</html>
"""

# --------------------------
# Routes
# --------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    error = None

    if request.method == "POST":
        city = request.form.get("city", "").strip()
        if city:
            weather, error = fetch_weather(city)

    return render_template_string(HTML_TEMPLATE, weather=weather, error=error)


# --------------------------
# Local run
# --------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5001)
