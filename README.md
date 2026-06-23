# SkyCache

SkyCache is an async Python weather CLI that fetches weather for multiple cities concurrently and stores recent responses in a local SQLite cache.

It is designed to be simple to run without credentials. If `OPENWEATHER_API_KEY` is not set, SkyCache uses mock weather data so the CLI and cache behavior still work during demos.

## Features

- Concurrent city lookups with `asyncio.gather`
- Async HTTP requests with `aiohttp`
- SQLite cache with configurable expiration
- Mock fallback for credential-free demos
- Optional live OpenWeather integration

## Project Structure

```text
.
|-- main.py              # CLI entrypoint
|-- src/
|   |-- api.py           # Async OpenWeather/mock weather fetcher
|   `-- database.py      # SQLite cache helpers
|-- tests/               # Cache behavior tests
|-- requirements.txt
`-- .env.example
```

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
.venv/bin/python3 -m pip install -r requirements.txt
```

## Usage

Run with mock data:

```bash
.venv/bin/python3 main.py --cities London Tokyo Anchorage
```

Run again to see cache hits:

```bash
.venv/bin/python3 main.py --cities London Tokyo Anchorage
```

Set a custom cache expiration in seconds:

```bash
.venv/bin/python3 main.py --cities London Tokyo --cache-ttl 60
```

## Live Weather

To use live OpenWeather data, set an API key before running the CLI:

```bash
export OPENWEATHER_API_KEY=your_api_key_here
.venv/bin/python3 main.py --cities London Tokyo Anchorage
```

You can also change where the SQLite cache is stored:

```bash
export SKYCACHE_DB_PATH=db/cache.db
```

## Example Output

```text
[CACHE MISS] Fetching data for LONDON...
  City:        London
  Temperature: 72.5 F
  Humidity:    45%
  Condition:   Clear sky intermittent mock data
  Data Source: Mock API

[CACHE HIT] LONDON:
  City:        London
  Temperature: 72.5 F
  Humidity:    45%
  Condition:   Clear sky intermittent mock data
  Data Source: Mock API
```

## Tests

Run the test suite with:

```bash
.venv/bin/python3 -m unittest discover
```

## GitHub Showcase Tips

- Add a terminal screenshot or GIF showing a cache miss followed by a cache hit.
- Use the repo description: `Async Python weather CLI with SQLite caching`.
- Add topics: `python`, `asyncio`, `sqlite`, `cli`, `aiohttp`, `weather-api`, `caching`.
