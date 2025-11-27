import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")  # Make sure this name matches your .env file
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
def get_weather(city_name: str):
    """
    Fetch and display weather information for a given city.
    """

    if not API_KEY:
        print("❌ Error: API key not found. Make sure OPENWEATHER_API_KEY is set in your .env file.")
        return

    params = {
        "q": city_name,
        "appid": API_KEY
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()  # Raises error for 400+ responses
    except requests.exceptions.HTTPError:
        if response.status_code == 404:
            print(f"\n❌ City '{city_name}' not found. Check the spelling.\n")
        else:
            print(f"\n❌ HTTP Error: {response.status_code}\n")
        return
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Network error: {e}\n")
        return

    data = response.json()

    try:
        kelvin = data["main"]["temp"]
        feels_like_k = data["main"]["feels_like"]
        description = data["weather"][0]["description"]
        city = data["name"]
        country = data["sys"]["country"]
    except (KeyError, IndexError):
        print("❌ Unexpected response format from the API.")
        return

    # Convert Kelvin → Celsius → Fahrenheit
    celsius = kelvin - 273.15
    fahrenheit = celsius * 9/5 + 32

    feels_like_c = feels_like_k - 273.15
    feels_like_f = feels_like_c * 9/5 + 32

    # Nicely formatted output
    print(f"\n📍 Weather in {city}, {country}")
    print(f"🌡️ Temperature: {celsius:.1f}°C / {fahrenheit:.1f}°F")
    print(f"🤗 Feels like:  {feels_like_c:.1f}°C / {feels_like_f:.1f}°F")
    print(f"🌥️ Condition:   {description.capitalize()}\n")
if __name__ == "__main__":
    city = input("Enter a city name: ")
    get_weather(city)
