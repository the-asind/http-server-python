import requests
import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from config import WEATHER_API_KEY

load_dotenv()

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

app = Flask(__name__)

@app.route('/weather')
def get_weather():
    city = request.args.get('city', 'Moscow')
    if not city:
        return jsonify({"error": "City parameter is required"}), 400
    weather_data = get_weather_info(city)
    return jsonify(weather_data)

def get_weather_info(city="Novosibirsk"):
    """Get real weather data from OpenWeatherMap API"""
    try:
        params = {
            'q': city,
            'appid': WEATHER_API_KEY,
            'units': 'metric' 
        }
        
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        
        data = response.json()
        return {
            "city": city,
            "weather": data['weather'][0]['description'],
            "temperature": round(data['main']['temp'], 1),
            "humidity": data['main']['humidity'],
            "wind_speed": data['wind']['speed']
        }
    except requests.exceptions.RequestException as e:
        return {
            "error": "Weather service unavailable",
            "details": str(e)
        }
    except (KeyError, ValueError) as e:
        return {
            "error": "Invalid weather data received",
            "details": str(e)
        }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)