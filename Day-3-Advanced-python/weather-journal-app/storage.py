"""
storage.py
Handles saving/loading the weather journal to and from a JSON file.

Demonstrates: JSON handling, Context Managers (via 'with open'), Exception handling, Logging.
"""

import json
import logging

logger = logging.getLogger("weather_journal")


def save_to_json(journal, filepath):
    """Save all entries in a WeatherJournal object to a JSON file."""
    try:
        with open(filepath, "w") as f:
            data = {
                "owner": journal.owner,
                "entries": [entry.to_dict() for entry in journal],
            }
            json.dump(data, f, indent=2)
        logger.info(f"Journal data saved to {filepath}")
    except OSError as e:
        logger.error(f"Failed to save journal data: {e}")
        raise


def load_from_json(filepath):
    """Load journal data from a JSON file and return it as a Python dict."""
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
        logger.info(f"Journal data loaded from {filepath}")
        return data
    except FileNotFoundError:
        logger.warning(f"{filepath} not found. Returning empty data.")
        return {"owner": "Unknown", "entries": []}
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {filepath}: {e}")
        raise
