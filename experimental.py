from src.tool import tool
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
load_dotenv()

class WeatherAPI(BaseModel):
    location: str = Field(..., description="The location's name or geographical coordinates (latitude and longitude) in the format 'lat,lon'", example=['London', '48.8567,2.3508'])

@tool("Weather API Tool", args_schema=WeatherAPI)
def weather_api_tool(location: str) -> str:
    '''
    Fetches the current weather data for a specific location using the OpenWeatherMap API and returns the result in JSON format.
    '''
    import requests
    import os
    import json

    api_key = os.environ.get('OPENWEATHERMAP_API_KEY')
    base_url = 'http://api.openweathermap.org/data/2.5/weather'

    try:
        if ',' in location:
            lat, lon = location.split(',')
            params = {
                'lat': lat,
                'lon': lon,
                'appid': api_key,
                'units': 'metric'
            }
        else:
            params = {
                'q': location,
                'appid': api_key,
                'units': 'metric'
            }

        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return json.dumps(response.json(), indent=4)
    except requests.exceptions.RequestException as err:
        return f"Error: {err}"

