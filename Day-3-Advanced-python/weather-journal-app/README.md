# Weather Journal App

A personal weather journal that fetches live weather data and lets you log your own notes,
combining Day 3 Advanced Python concepts into one working project.

## What This Project Does

1. **Fetches today's real weather** for a location (default: Bengaluru) from the free
   **Open-Meteo API** — no API key required.
2. **Stores it as a `JournalEntry`** alongside any **manual entries** you add yourself
   (e.g. "carried an umbrella, roads were flooded").
3. **Displays all entries sorted by date**, and calculates the average temperature logged.
4. **Lets you query entries within a date range** (e.g. "show me the last 2 days") using a generator.
5. **Saves the entire journal to a JSON file** so your history persists between runs, and can reload it back.
6. **Logs every major action** (opening the journal, adding entries, API calls, saving/loading)
   with timestamps, instead of using plain print statements.

In short: it's a small diary that mixes automated weather logging with your own personal notes,
and keeps a running, searchable, saved history of both.

## Concept → Code Mapping

| Concept | Where it's used |
|---|---|
| Classes & Objects | `JournalEntry`, `APIWeatherEntry`, `ManualWeatherEntry`, `WeatherJournal` |
| Constructors | `__init__` in every class, with `super().__init__()` chaining |
| Inheritance | `APIWeatherEntry` and `ManualWeatherEntry` inherit from `JournalEntry` |
| Polymorphism | `summary()` produces different output for API vs. manual entries |
| Encapsulation | `__temperature_c` is private, validated through a property setter |
| Abstraction | `JournalEntry` is an `ABC` with an abstract `summary()` method |
| Iterators & Generators | `WeatherJournal.__iter__` (sorted iteration), `find_by_date_range()` (generator) |
| Decorators | `@log_action` and `@timer` in `decorators.py` |
| Context Managers | `WeatherJournal.__enter__`/`__exit__`, and `with open(...)` in `storage.py` |
| Logging | Configured in `main.py`, used throughout via the `logging` module |
| JSON handling | `storage.py` — `save_to_json()` / `load_from_json()` |
| REST API consumption | `api_client.py` — live weather from Open-Meteo via `requests` |

## Folder Structure
```
weather-journal-app/
├── main.py            # entry point - runs the full demo
├── models.py            # JournalEntry (abstract), APIWeatherEntry, ManualWeatherEntry
├── journal.py            # WeatherJournal container - iterator/generator/context manager
├── decorators.py          # @log_action and @timer decorators
├── storage.py              # JSON save/load
├── api_client.py            # Open-Meteo REST API calls via requests
└── requirements.txt
```

## How to Run
```bash
cd weather-journal-app
pip install -r requirements.txt
python main.py
```

This will:
1. Open a `WeatherJournal` (as a context manager)
2. Fetch today's live weather for Bengaluru from Open-Meteo and log it as an `APIWeatherEntry`
3. Add two manual entries with personal notes
4. Print all entries sorted by date, and the average temperature
5. Print only entries from the last 2 days (generator-based filtering)
6. Save everything to `data/journal.json` and reload it to confirm persistence

## Notes
- No API key is needed — Open-Meteo's forecast endpoint is free and open.
- If there's no internet connection, the app logs the failure and falls back to a
  sample entry instead of crashing.
- To change the location, edit `LOCATION_NAME`, `LATITUDE`, and `LONGITUDE` in `main.py`.
