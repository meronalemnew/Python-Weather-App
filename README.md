# 🌦️ Python Weather App

A small weather application built with Python.  
It has two versions:

- a command-line version  
- a simple web version built with Flask (and deployed on Render)

Both versions use the OpenWeather API to fetch real-time weather data for any city.

---

## 🌐 Live Demo

You can try the web version here:

👉 https://python-weather-app-aepm.onrender.com/

---

## 📸 CLI Screenshot

![Weather App Screenshot](assets/weather-app.png)

---

## ✨ Features

- Get current weather for any city  
- Temperature in Celsius and Fahrenheit  
- Short description (clear sky, overcast clouds, etc.)  
- Error handling for invalid city names or network issues  
- Keeps API keys out of source code using environment variables  
- Works both in the terminal and in the browser  

---

## 🛠 Tools Used

- Python 3  
- Flask  
- Requests  
- python-dotenv  
- Gunicorn (for deployment)  
- OpenWeather API  
- Render (hosting)

---

# ⚙️ Setup (Local)

## 1. Clone the project

```bash
git clone https://github.com/meronalemnew/Python-Weather-App.git
cd Python-Weather-App
