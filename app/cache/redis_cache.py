import json
from typing import Any, Optional, cast

import redis

from app.core.config import settings


# Lazy Redis client initialization to avoid import-time connection errors
redis_client = redis.StrictRedis.from_url(settings.REDIS_URL, decode_responses=False)


def get_cached_prediction(key: str) -> Optional[float]:
    """Return a cached prediction for the given key, or None if missing."""
    try:
        value = cast(bytes | None, redis_client.get(key))
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
        redis_client.setex(key, expiry, json.dumps(value))
    except redis.RedisError:
        pass  # Silently fail if Redis is unavailable
