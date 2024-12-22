
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv('DB_URL', 'sqlite:///users.db')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', 'e83b3c4c08285bf87b99f9bbc0abe3f0') # украл с гиста