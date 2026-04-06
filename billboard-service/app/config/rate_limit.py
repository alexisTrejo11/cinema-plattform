"""Shared SlowAPI limiter instance."""

from slowapi import Limiter
from slowapi.util import get_remote_address

# Default cap for routes that do not set an explicit @limiter.limit (matches previous main.py).
limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])
