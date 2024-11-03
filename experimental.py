from src.tool import tool
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
load_dotenv()

class StockPrice(BaseModel):
    symbol:str=Field(...,description="The stock symbol.",example=['AAPL'])

@tool("Stock Price Tool",args_schema=StockPrice)
def stock_price_tool(symbol:str):
    '''
    Retrieves the current stock price for the given stock symbol using Alpha Vantage API.
    '''
    import requests
    import os
    import json
    api_key=os.environ.get('ALPHA_VANTAGE_API_KEY')
    try:
        response=requests.get(f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}')
        data=response.json()
        if 'Global Quote' in data:
            return f"Current stock price for {symbol}: ${data['Global Quote']['05. price']}"
        else:
            return f"Failed to retrieve stock price for {symbol}."
    except Exception as err:
        return f"Error: {err}"

class Weather(BaseModel):
    city:str=Field(...,description="The city to get the weather for.",example=['New York'])
    api_key:str=Field(...,description="The OpenWeatherMap API key.",example=['your_api_key'])

@tool("Weather Tool",args_schema=Weather)
def weather_tool(city:str,api_key:str):
    '''
    Gets the current weather for the given city using OpenWeatherMap API and returns the formatted results.
    '''
    import requests
    import os
    api_key=os.environ.get('OPENWEATHERMAP_API_KEY')
    try:
        response=requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric')
        data=response.json()
        weather=data['weather'][0]['description']
        temperature=data['main']['temp']
        humidity=data['main']['humidity']
        return f'Weather in {city}: {weather}\nTemperature: {temperature}°C\nHumidity: {humidity}%'
    except Exception as err:
        return f'Error: {err}'

