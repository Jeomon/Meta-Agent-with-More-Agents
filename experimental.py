from src.tool import tool
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
load_dotenv()

class Weather(BaseModel):
    location: str = Field(..., description='The location for which the weather information is to be retrieved.', example=['London'])

@tool('Weather Tool', args_schema=Weather)
def weather_tool(location: str):
    """
    Retrieves the current weather information for a specific location.
    """
    import requests
    import os
    import json
    api_key = os.environ.get('OPENWEATHERMAP_API_KEY')
    try:
        base_url = 'http://api.openweathermap.org/data/2.5/weather'
        params = {'q': location, 'appid': api_key, 'units': 'metric'}
        response = requests.get(base_url, params=params)
        weather_data = response.json()
        weather_info = f'Current weather in {location}: {weather_data['weather'][0]['description']}.\nTemperature: {weather_data['main']['temp']}°C.\nHumidity: {weather_data['main']['humidity']}%'
        return weather_info
    except Exception as err:
        return f'Error: {err}'

class StockPrice(BaseModel):
    symbol:str=Field(...,description="The stock symbol.",example=['NVDA'])

@tool("Stock Price Tool",args_schema=StockPrice)
def stock_price_tool(symbol:str):
    '''
    Fetches real-time financial data, including the current stock price of the given symbol.
    '''
    import requests
    import json
    api_key=os.environ.get('ALPHA_VANTAGE_API_KEY')
    try:
        url=f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}'
        response=requests.get(url)
        data=response.json()
        if 'Global Quote' in data:
            return json.dumps(data['Global Quote'],indent=4)
        else:
            return 'Error: Invalid symbol or API key'
    except Exception as err:
        return f'Error: {err}'

