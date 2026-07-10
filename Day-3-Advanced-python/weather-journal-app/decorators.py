"""
decorators.py
Custom decorators used across the weather journal app.

Demonstrates: Decorators, Logging.
"""

import functools
import logging
import time

logger = logging.getLogger("weather_journal")


def log_action(func):
    """Logs the name of the function called and confirms completion."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Calling '{func.__name__}' with args={args[1:]} kwargs={kwargs}")
        result = func(*args, **kwargs)
        logger.info(f"'{func.__name__}' completed successfully")
        return result
    return wrapper


def timer(func):
    """Logs how long a function took to execute."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.info(f"'{func.__name__}' took {elapsed:.4f} seconds")
        return result
    return wrapper
