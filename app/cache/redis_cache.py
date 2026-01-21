import json
from typing import Any, Optional, cast

import redis

from app.core.config import settings


# Lazy Redis client initialization to avoid import-time connection errors
_redis_client: Optional[redis.Redis] = None


def _get_redis_client() -> redis.Redis:
    """Get or create Redis client."""
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=False)
    return _redis_client


def get_cached_prediction(key: str) -> Optional[float]:
    """Return a cached prediction for the given key, or None if missing."""
    try:
        client = _get_redis_client()
        value = cast(bytes | None, client.get(key))
        if value is None:
            return None
        return float(json.loads(value))
    except (redis.RedisError, json.JSONDecodeError, ValueError):
        return None


def set_cached_predicition(
    key: str,
    value: float,
    expiry: int = 3600,
) -> None:
    """Cache a prediction under the given key with an expiry in seconds."""
    try:
        client = _get_redis_client()
        client.setex(key, expiry, json.dumps(value))
    except redis.RedisError:
        pass  # Silently fail if Redis is unavailable
