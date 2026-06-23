import asyncio
import sys
import argparse
from src.database import init_db, get_cached_weather, save_to_cache
from src.api import fetch_weather_async

async def process_city(city: str, cache_ttl: int) -> None:
    """Orchestrates the cache-first lookups and API calls for a single city."""
    cached_data = get_cached_weather(city, expiry_seconds=cache_ttl)
    if cached_data:
        print(f"\n[CACHE HIT] {city.upper()}:")
        display_weather(cached_data)
        return

    print(f"\n[CACHE MISS] Fetching data for {city.upper()}...")
    result = await fetch_weather_async(city)
    
    if "error" in result:
        print(f"[ERROR] Error fetching {city}: {result['error']}")
    else:
        save_to_cache(city, result)
        display_weather(result)

def display_weather(data: dict) -> None:
    """Helper function to print output cleanly."""
    name = data.get("name", "Unknown")
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    desc = data["weather"][0]["description"]
    source = data.get("source", "Unknown")
    
    print(f"  City:        {name}")
    print(f"  Temperature: {temp} F")
    print(f"  Humidity:    {humidity}%")
    print(f"  Condition:   {desc.capitalize()}")
    print(f"  Data Source: {source}")

async def main():
    # Setup Argument Parsing
    parser = argparse.ArgumentParser(description="Async Weather CLI Utility with Caching")
    parser.add_argument(
        "--cities", 
        nargs="+", 
        required=True, 
        help="Space-separated list of cities to inspect (e.g., --cities London NewYork Tokyo)"
    )
    parser.add_argument(
        "--cache-ttl",
        type=int,
        default=600,
        help="Seconds before cached weather expires. Defaults to 600."
    )
    args = parser.parse_args()

    init_db()

    tasks = [process_city(city, args.cache_ttl) for city in args.cities]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    # Standard boilerplate to execute async main loop in modern Python 3
    asyncio.run(main())
