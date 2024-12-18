"""Module provides a memory cache implementation."""

import logging
import time

_LOGGER = logging.getLogger(__name__)


class MemCacheItem:
    """Class representing an item in the memory cache."""

    def __init__(self, key, value, duration: int):
        """Initialize a MemCacheItem object."""
        self._key = key
        self._value = value
        self._expiry = time.time() + duration

    def value(self):
        """Get the value of the cache item."""
        return self._value

    def expiry(self):
        """Get the expiry time of the cache item."""
        return self._expiry

    def __repr__(self):
        """Return a string representation of the cache item."""
        return f"<MemCacheItem {{{self._key}:{self._value}}} expires at: {self.expiry()}, expired: {self.expiry() < time.time()}>"


class MemCache:
    """Class representing a memory cache."""

    def __init__(self):
        """Initialize an empty cache."""
        self._data = {}

    def exists(self, key):
        """Check if the specified key exists in the cache."""
        return self.get(key) is not None

    def get(self, key):
        """Get the value of the specified key from the cache."""
        if key not in self._data or self._data[key].expiry() < time.time():
            _LOGGER.debug("Cache entry missing for key: '%s'", key)
            return None

        return self._data[key].value()

    def set(self, key, value, duration: int = 30):
        """Set the value of the specified key in the cache."""
        _LOGGER.debug("Caching value for: '%s'", key)
        self._data[key] = MemCacheItem(key, value, duration)
