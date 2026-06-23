import asyncio
import os
from typing import Dict, Any

import aiohttp

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

async def fetch_weather_async(city: str) -> Dict[str, Any]:
    """Fetches real-time weather data from the API asynchronously."""
    if not API_KEY:
        await asyncio.sleep(0.5)  # Simulate network latency
        return {
            "name": city.capitalize(),
            "main": {"temp": 72.5, "humidity": 45},
            "weather": [{"description": "clear sky intermittent mock data"}],
            "source": "Mock API"
        }

    params = {"q": city, "appid": API_KEY, "units": "imperial"}
    timeout = aiohttp.ClientTimeout(total=10)
    
    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            async with session.get(BASE_URL, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    data["source"] = "Live OpenWeather API"
                    return data
                else:
                    return {"error": f"API responded with status {response.status}", "city": city}
        except Exception as e:
            return {"error": f"Connection error: {str(e)}", "city": city}
