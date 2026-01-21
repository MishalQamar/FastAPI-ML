import json
from typing import Any, Optional, cast

import redis

from app.core.config import settings


# Explicitly type the client so Redis `get` is treated as sync and returns bytes.
redis_client: redis.Redis = redis.Redis.from_url(settings.REDIS_URL)


def get_cached_prediction(key: str) -> Optional[dict[str, Any]]:
    """Return a cached prediction for the given key, or None if missing."""
    value = cast(bytes | None, redis_client.get(key))
    if value is None:
        return None
    return json.loads(value)


def set_cached_predicition(
    key: str,
    value: dict[str, Any],
    expiry: int = 3600,
) -> None:
    """Cache a prediction under the given key with an expiry in seconds."""
    redis_client.setex(key, expiry, json.dumps(value))
