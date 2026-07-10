"""
models.py
Defines the abstract base class and concrete entry types for the weather journal.

Demonstrates: Classes & Objects, Constructors, Inheritance, Polymorphism,
Encapsulation & Abstraction.
"""

from abc import ABC, abstractmethod
from datetime import date as date_cls


class JournalEntry(ABC):
    """Abstract base class representing a single day's weather journal entry."""

    def __init__(self, entry_date, location, temperature_c, condition):
        self.date = entry_date if isinstance(entry_date, date_cls) else date_cls.fromisoformat(entry_date)
        self.location = location
        self._condition = condition
        self.__temperature_c = None
        self.temperature_c = temperature_c  # goes through the validating setter below

    @property
    def temperature_c(self):
        return self.__temperature_c

    @temperature_c.setter
    def temperature_c(self, value):
        # Encapsulation: reject physically impossible temperatures
        if value < -90 or value > 60:
            raise ValueError(f"Temperature {value}°C is outside a realistic range.")
        self.__temperature_c = value

    @property
    def condition(self):
        return self._condition

    @abstractmethod
    def summary(self):
        """Every subclass must define how it summarizes itself (Abstraction)."""
        raise NotImplementedError

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "date": self.date.isoformat(),
            "location": self.location,
            "temperature_c": self.__temperature_c,
            "condition": self._condition,
        }


class APIWeatherEntry(JournalEntry):
    """A weather entry automatically fetched from a live weather API."""

    def __init__(self, entry_date, location, temperature_c, condition, wind_speed_kmh=None, humidity=None):
        super().__init__(entry_date, location, temperature_c, condition)
        self.wind_speed_kmh = wind_speed_kmh
        self.humidity = humidity

    def summary(self):
        # Polymorphism: API entries emphasize measured data
        wind = f", wind {self.wind_speed_kmh} km/h" if self.wind_speed_kmh is not None else ""
        humidity = f", humidity {self.humidity}%" if self.humidity is not None else ""
        return (f"[API] {self.date} @ {self.location}: {self.temperature_c}°C, "
                f"{self.condition}{wind}{humidity}")

    def to_dict(self):
        data = super().to_dict()
        data["wind_speed_kmh"] = self.wind_speed_kmh
        data["humidity"] = self.humidity
        return data


class ManualWeatherEntry(JournalEntry):
    """A weather entry logged manually by the user, with a personal note."""

    def __init__(self, entry_date, location, temperature_c, condition, note=""):
        super().__init__(entry_date, location, temperature_c, condition)
        self.note = note

    def summary(self):
        # Polymorphism: manual entries emphasize the personal note
        note_part = f' — "{self.note}"' if self.note else ""
        return f"[Manual] {self.date} @ {self.location}: {self.temperature_c}°C, {self.condition}{note_part}"

    def to_dict(self):
        data = super().to_dict()
        data["note"] = self.note
        return data
