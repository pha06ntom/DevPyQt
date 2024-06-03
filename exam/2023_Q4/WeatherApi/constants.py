import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
OPENWEATHERMAP_API_KEY = os.environ.get("OPENWEATHERMAP_API_KEY")
