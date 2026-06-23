import sqlite3
import tempfile
import time
import unittest
from pathlib import Path

from src.database import get_cached_weather, init_db, save_to_cache


class DatabaseCacheTests(unittest.TestCase):
    def test_save_and_read_fresh_cache_entry(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "cache.db"
            weather = {
                "name": "London",
                "main": {"temp": 72.5, "humidity": 45},
                "weather": [{"description": "clear sky"}],
                "source": "Mock API",
            }

            init_db(db_path)
            save_to_cache(" London ", weather, db_path)

            self.assertEqual(get_cached_weather("london", db_path=db_path), weather)

    def test_expired_cache_entry_returns_none(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "cache.db"
            init_db(db_path)

            with sqlite3.connect(db_path) as conn:
                conn.execute(
                    """
                    INSERT INTO weather_cache (city, data, timestamp)
                    VALUES (?, ?, ?)
                    """,
                    ("tokyo", "{}", time.time() - 999),
                )

            self.assertIsNone(
                get_cached_weather("tokyo", expiry_seconds=1, db_path=db_path)
            )

    def test_init_db_creates_parent_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "nested" / "cache.db"

            init_db(db_path)

            self.assertTrue(db_path.exists())


if __name__ == "__main__":
    unittest.main()
