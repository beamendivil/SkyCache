import sqlite3
import time
import json
import os
from pathlib import Path
from typing import Optional, Dict, Any

DEFAULT_DB_PATH = Path(os.getenv("SKYCACHE_DB_PATH", "db/cache.db"))

def _resolve_db_path(db_path: Optional[Path] = None) -> Path:
    return Path(db_path or DEFAULT_DB_PATH)

def _normalize_city(city: str) -> str:
    return city.lower().strip()

def init_db(db_path: Optional[Path] = None) -> None:
    """Initializes the database and creates the cache table if it doesn't exist."""
    path = _resolve_db_path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS weather_cache (
                city TEXT PRIMARY KEY,
                data TEXT,
                timestamp REAL
            )
        """)
        conn.commit()

def get_cached_weather(
    city: str,
    expiry_seconds: int = 600,
    db_path: Optional[Path] = None,
) -> Optional[Dict[str, Any]]:
    """
    Retrieves cached weather data if it exists and is newer than expiry_seconds.
    Returns None if cache is expired or missing.
    """
    with sqlite3.connect(_resolve_db_path(db_path)) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT data, timestamp FROM weather_cache WHERE city = ?", 
            (_normalize_city(city),)
        )
        row = cursor.fetchone()
        
        if row:
            data_str, timestamp = row
            # Check if the cache is still fresh
            if time.time() - timestamp < expiry_seconds:
                return json.loads(data_str)
    return None

def save_to_cache(city: str, data: Dict[str, Any], db_path: Optional[Path] = None) -> None:
    """Saves or updates weather data in the local cache with a fresh timestamp."""
    path = _resolve_db_path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO weather_cache (city, data, timestamp)
            VALUES (?, ?, ?)
        """, (_normalize_city(city), json.dumps(data), time.time()))
        conn.commit()
