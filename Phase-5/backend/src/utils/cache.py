"""Caching utilities for the Todo Chatbot backend"""
import asyncio
import time
from typing import Any, Optional, Dict
from datetime import datetime, timedelta
from functools import wraps
import hashlib
import json
from threading import Lock


class SimpleCache:
    """A simple in-memory cache with TTL (Time To Live)"""

    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = Lock()

    def set(self, key: str, value: Any, ttl: int = 300) -> None:  # Default 5 minutes TTL
        """Set a value in cache with TTL in seconds"""
        with self._lock:
            expiration_time = time.time() + ttl
            self._cache[key] = {
                'value': value,
                'expiration': expiration_time
            }

    def get(self, key: str) -> Optional[Any]:
        """Get a value from cache, return None if expired or not found"""
        with self._lock:
            if key not in self._cache:
                return None

            item = self._cache[key]
            if time.time() > item['expiration']:
                # Remove expired item
                del self._cache[key]
                return None

            return item['value']

    def delete(self, key: str) -> bool:
        """Delete a key from cache"""
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False

    def clear(self) -> None:
        """Clear all cache"""
        with self._lock:
            self._cache.clear()

    def cleanup_expired(self) -> int:
        """Remove all expired entries and return count of removed items"""
        with self._lock:
            current_time = time.time()
            expired_keys = [
                key for key, item in self._cache.items()
                if current_time > item['expiration']
            ]

            for key in expired_keys:
                del self._cache[key]

            return len(expired_keys)


# Global cache instance
cache = SimpleCache()


def cache_result(ttl: int = 300):
    """Decorator to cache function results"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            cache_key = f"{func.__name__}:{hashlib.md5(str(args + tuple(sorted(kwargs.items()))).encode()).hexdigest()}"

            # Try to get from cache first
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result

            # Execute function and cache result
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            return result
        return wrapper
    return decorator


def cache_async_result(ttl: int = 300):
    """Async decorator to cache async function results"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            cache_key = f"{func.__name__}:{hashlib.md5(str(args + tuple(sorted(kwargs.items()))).encode()).hexdigest()}"

            # Try to get from cache first
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result

            # Execute function and cache result
            result = await func(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            return result
        return wrapper
    return decorator


def make_cache_key(*args, **kwargs) -> str:
    """Create a cache key from arguments"""
    key_parts = [str(arg) for arg in args]
    key_parts.extend([f"{k}={v}" for k, v in sorted(kwargs.items())])
    return hashlib.md5(":".join(key_parts).encode()).hexdigest()


def cache_with_key(key_prefix: str, ttl: int = 300):
    """Decorator to cache with a custom key prefix"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from prefix and arguments
            cache_key = f"{key_prefix}:{make_cache_key(*args, **kwargs)}"

            # Try to get from cache first
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result

            # Execute function and cache result
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            return result
        return wrapper
    return decorator


def invalidate_cache_pattern(pattern: str) -> int:
    """Remove all cache entries matching a pattern and return count of removed items"""
    with cache._lock:
        keys_to_remove = [key for key in cache._cache.keys() if pattern in key]
        for key in keys_to_remove:
            del cache._cache[key]
        return len(keys_to_remove)


def get_cache_stats() -> Dict[str, Any]:
    """Get cache statistics"""
    with cache._lock:
        total_items = len(cache._cache)
        expired_count = sum(1 for item in cache._cache.values() if time.time() > item['expiration'])

        return {
            'total_items': total_items,
            'expired_items': expired_count,
            'active_items': total_items - expired_count
        }