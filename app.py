import os
import requests
from dotenv import load_dotenv
from flask import Flask, request, render_template_string

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

app = Flask(__name__)

# -------------------------
# Core weather logic
# -------------------------
def fetch_weather(city_name: str):
    if not API_KEY:
        return None, "API key is missing. Please set OPENWEATHER_API_KEY in your .env file."

    params = {"q": city_name, "appid": API_KEY}

    try:
        resp = requests.get(BASE_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        kelvin = data["main"]["temp"]
        celsius = kelvin - 273.15
        fahrenheit = celsius * 9 / 5 + 32
        description = data["weather"][0]["description"].capitalize()
        city = data["name"]
        country = data["sys"]["country"]

        weather = {
            "city": city,
            "country": country,
            "celsius": round(celsius, 1),
            "fahrenheit": round(fahrenheit, 1),
            "description": description,
        }
        return weather, None

    except requests.exceptions.HTTPError:
        return None, "City not found. Please check the spelling."
    except Exception:
        return None, "Error fetching weather data. Please try again."


# -------------------------
# HTML template
# -------------------------
TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Weather App</title>
  <style>
    body {
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: #f5f5f7;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      margin: 0;
    }
    .card {
      background: white;
      padding: 24px 28px;
      border-radius: 16px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.08);
      max-width: 360px;
      width: 100%;
    }
    h1 {
      font-size: 1.5rem;
      margin-bottom: 16px;
      text-align: center;
    }
    form {
      display: flex;
      gap: 8px;
      margin-bottom: 16px;
    }
    input[type="text"] {
      flex: 1;
      padding: 8px 10px;
      border-radius: 8px;
      border: 1px solid #ccc;
      font-size: 0.95rem;
    }
    button {
      padding: 8px 12px;
      border-radius: 8px;
      border: none;
      background: #2563eb;
      color: white;
      font-size: 0.95rem;
      cursor: pointer;
    }
    button:hover {
      background: #1d4ed8;
    }
    .error {
      color: #b91c1c;
      margin-bottom: 8px;
      font-size: 0.9rem;
    }
    .weather {
      font-size: 0.98rem;
      line-height: 1.5;
    }
    .city {
      font-weight: 600;
      margin-bottom: 4px;
    }
    .muted {
      color: #6b7280;
      font-size: 0.85rem;
    }
  </style>
</head>
<body>
  <div class="card">
    <h1>🌦️ Weather App</h1>
    <form method="post">
      <input type="text" name="city" placeholder="Enter a city" value="{{ city or '' }}" />
      <button type="submit">Get weather</button>
    </form>

    {% if error %}
      <div class="error">❌ {{ error }}</div>
    {% endif %}

    {% if weather %}
      <div class="weather">
        <div class="city">📍 {{ weather.city }}, {{ weather.country }}</div>
        <div>🌡️ {{ weather.celsius }} °C / {{ weather.fahrenheit }} °F</div>
        <div>🌥️ {{ weather.description }}</div>
      </div>
    {% else %}
      <div class="muted">Type a city name and press "Get weather".</div>
    {% endif %}
  </div>
</body>
</html>
"""


# -------------------------
# Flask route
# -------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    error = None
    city = None

    if request.method == "POST":
        city = (request.form.get("city") or "").strip()
        if not city:
            error = "Please enter a city name."
        else:
            weather, error = fetch_weather(city)

    return render_template_string(TEMPLATE, weather=weather, error=error, city=city)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
    # debug=True auto-reloads on code changes
    
