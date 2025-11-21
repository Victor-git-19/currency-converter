# app/cache.py
import time

CACHE_LIFETIME = 600
_cache = {}


def get_cached(key):
    if key in _cache:
        value, timestamp = _cache[key]
        if time.time() - timestamp < CACHE_LIFETIME:
            return value
    return None


def set_cached(key, value):
    _cache[key] = (value, time.time())
