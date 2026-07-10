"""
main.py
Entry point for the Weather Journal App.

Ties together OOP (classes, constructors, inheritance, polymorphism,
encapsulation, abstraction), iterators/generators, decorators, context
managers, logging, JSON handling, and REST API consumption.
"""

import logging
import os
from datetime import date, timedelta

from api_client import fetch_current_weather
from decorators import timer
from journal import WeatherJournal
from models import APIWeatherEntry, ManualWeatherEntry
from storage import load_from_json, save_to_json

# --- Logging setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("weather_journal")

DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "journal.json")

# Example location: Bengaluru, India
LOCATION_NAME = "Bengaluru"
LATITUDE = 12.9716
LONGITUDE = 77.5946


@timer
def build_journal():
    """Create a WeatherJournal, fetch live data, and add a manual entry."""
    with WeatherJournal(f"{LOCATION_NAME} Weather Journal") as journal:  # Context manager

        # 1. Fetch today's real weather from the Open-Meteo API
        live_data = fetch_current_weather(LATITUDE, LONGITUDE)
        if live_data and live_data["temperature_c"] is not None:
            api_entry = APIWeatherEntry(
                entry_date=date.today(),
                location=LOCATION_NAME,
                temperature_c=live_data["temperature_c"],
                condition=live_data["condition"],
                wind_speed_kmh=live_data["wind_speed_kmh"],
                humidity=live_data["humidity"],
            )
            journal.add_entry(api_entry)
        else:
            print("Could not fetch live weather (no internet in this environment) — "
                  "adding a sample API-style entry instead.")
            journal.add_entry(APIWeatherEntry(
                entry_date=date.today(), location=LOCATION_NAME,
                temperature_c=27.5, condition="Partly cloudy",
                wind_speed_kmh=12.0, humidity=65,
            ))

        # 2. Add a couple of manual entries with personal notes (Constructors, Inheritance)
        journal.add_entry(ManualWeatherEntry(
            entry_date=date.today() - timedelta(days=1),
            location=LOCATION_NAME, temperature_c=26.0, condition="Rainy",
            note="Carried an umbrella, roads were flooded near office.",
        ))
        journal.add_entry(ManualWeatherEntry(
            entry_date=date.today() - timedelta(days=2),
            location=LOCATION_NAME, temperature_c=29.0, condition="Sunny",
            note="Great weather for a morning walk.",
        ))

        return journal


def display_journal(journal):
    # Polymorphism: same summary() call, different output for API vs Manual entries
    print("\n--- Weather Journal (sorted by date) ---")
    for entry in journal:          # Iterator protocol
        print(entry.summary())

    print(f"\nAverage temperature logged: {journal.average_temperature():.1f}°C")

    # Generator usage: entries from the last 2 days
    print("\n--- Entries from the last 2 days ---")
    start = date.today() - timedelta(days=2)
    end = date.today()
    for entry in journal.find_by_date_range(start, end):
        print(entry.summary())


def main():
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

    journal = build_journal()
    display_journal(journal)

    print(f"\n--- Saving journal to {DATA_FILE} ---")
    save_to_json(journal, DATA_FILE)

    print(f"\n--- Reloading journal from {DATA_FILE} ---")
    reloaded = load_from_json(DATA_FILE)
    print(reloaded)


if __name__ == "__main__":
    main()
