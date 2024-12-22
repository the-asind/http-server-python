import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv('DB_URL', 'postgresql://postgres:postgres@db:5432/userdb')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', '7ce731362434298690dc01b8acdad9ae')