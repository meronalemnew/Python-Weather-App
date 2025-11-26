import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

API_KEY = os.getenv("API_KEY")


def get_weather(city):
    if not city:
        return "Please enter a city name."

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException:
        return "Network error. Please check your internet connection and try again."

    if response.status_code != 200:
        return "City not found or error fetching data."

    data = response.json()

    # Extract main pieces of info
    name = data.get("name", city)
    country = data.get("sys", {}).get("country", "Unknown")
    temperature = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    description = data["weather"][0]["description"].capitalize()
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]

    # Build a nice formatted string
    result = (
        f"\nWeather for {name}, {country}\n"
        f"---------------------------\n"
        f"Temperature : {temperature}°C\n"
        f"Feels like  : {feels_like}°C\n"
        f"Condition   : {description}\n"
        f"Humidity    : {humidity}%\n"
        f"Wind speed  : {wind_speed} m/s\n"
    )

    return result

# Main loop: let the user check multiple cities
while True:
    city = input("\nEnter a city name (or type 'quit' to exit): ").strip()

    if city.lower() == "quit":
        print("Goodbye! 👋")
        break

    print(get_weather(city))
