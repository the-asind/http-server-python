import requests
import os
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', '')
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather_info(city="Moscow"):
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