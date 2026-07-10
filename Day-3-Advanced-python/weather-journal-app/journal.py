"""
journal.py
The WeatherJournal container class.

Demonstrates: Iterators & Generators, Context Managers, Decorators.
"""

import logging

from decorators import log_action

logger = logging.getLogger("weather_journal")


class WeatherJournal:
    """A collection of JournalEntry objects, iterable in date order and usable as a context manager."""

    def __init__(self, owner="My Weather Journal"):
        self.owner = owner
        self._entries = []

    @log_action
    def add_entry(self, entry):
        self._entries.append(entry)

    def __iter__(self):
        """Iterates over entries sorted by date (Iterator protocol)."""
        return iter(sorted(self._entries, key=lambda e: e.date))

    def find_by_date_range(self, start_date, end_date):
        """Generator - lazily yields entries whose date falls within [start_date, end_date]."""
        for entry in sorted(self._entries, key=lambda e: e.date):
            if start_date <= entry.date <= end_date:
                yield entry

    def average_temperature(self):
        if not self._entries:
            return None
        return sum(e.temperature_c for e in self._entries) / len(self._entries)

    def __len__(self):
        return len(self._entries)

    def __enter__(self):
        logger.info(f"Opening weather journal: {self.owner}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.info(f"Closing weather journal: {self.owner}")
        if exc_type:
            logger.error(f"Exception occurred during session: {exc_val}")
        return False  # do not suppress exceptions

    def all_entries(self):
        return list(self._entries)
