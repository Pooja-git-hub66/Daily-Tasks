"""
api_client.py
Consumes the Open-Meteo REST API to fetch real-time weather (no API key required).

Demonstrates: REST API consumption using requests, Exception handling, Logging.
"""

import logging

import requests

logger = logging.getLogger("weather_journal")

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

# WMO Weather interpretation codes -> human-readable condition
# https://open-meteo.com/en/docs (see "WMO Weather interpretation codes")
WEATHER_CODE_MAP = {
    0: "Clear sky",
    1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
    80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
    95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail",
}


def describe_weather_code(code):
    return WEATHER_CODE_MAP.get(code, f"Unknown (code {code})")


def fetch_current_weather(latitude, longitude):
    """
    Fetch current weather for a given latitude/longitude from Open-Meteo.

    Returns a dict with temperature_c, condition, wind_speed_kmh, humidity,
    or None if the request fails.
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": "true",
        "hourly": "relative_humidity_2m",
        "timezone": "auto",
    }
    try:
        response = requests.get(FORECAST_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        current = data.get("current_weather", {})
        temperature_c = current.get("temperature")
        wind_speed_kmh = current.get("windspeed")
        weather_code = current.get("weathercode")
        condition = describe_weather_code(weather_code)

        # Try to grab the humidity value closest to the current hour
        humidity = None
        hourly = data.get("hourly", {})
        if "time" in hourly and "relative_humidity_2m" in hourly and current.get("time") in hourly["time"]:
            idx = hourly["time"].index(current["time"])
            humidity = hourly["relative_humidity_2m"][idx]

        result = {
            "temperature_c": temperature_c,
            "condition": condition,
            "wind_speed_kmh": wind_speed_kmh,
            "humidity": humidity,
        }
        logger.info(f"Fetched current weather for ({latitude}, {longitude}): {result}")
        return result

    except requests.exceptions.RequestException as e:
        logger.error(f"Weather API request failed for ({latitude}, {longitude}): {e}")
        return None
