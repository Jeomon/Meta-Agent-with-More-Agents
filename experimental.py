from src.tool import tool
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
load_dotenv()

class Weather(BaseModel):
    location:str=Field(...,description="The location to fetch the weather data for.",example=['London'])

@tool("Weather Tool",args_schema=Weather)
def weather_tool(location:str)->str:
    """
    Fetches the current weather data for a given location.
    """
    import requests
    import os
    import json
    api_key=os.environ.get('OPENWEATHERMAP_API_KEY')
    try:
        base_url="http://api.openweathermap.org/data/2.5/weather"
        params={
            'q':location,
            'appid':api_key,
            'units':'metric'
        }
        response=requests.get(base_url,params=params)
        response.raise_for_status()
        data=response.json()
        weather_data={
            'location':location,
            'temperature':data['main']['temp'],
            'humidity':data['main']['humidity'],
            'weather_conditions':data['weather'][0]['description']
        }
        return json.dumps(weather_data,indent=4)
    except Exception as err:
        return f"Error: {err}"

