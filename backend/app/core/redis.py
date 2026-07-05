"""
Fleet-Ryan Backend — Redis Configuration
"""

import redis.asyncio as redis
import structlog
from app.core.config import settings

logger = structlog.get_logger()

# Redis client
redis_client: redis.Redis = None


async def init_redis():
    """Initialize Redis connection (optional — works without Redis)."""
    global redis_client
    try:
        redis_client = redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
        )
        # Test connection
        await redis_client.ping()
        logger.info("Redis connected", url=settings.REDIS_URL)
    except Exception as e:
        logger.warning("Redis not available — running without cache", error=str(e))
        redis_client = None


async def close_redis():
    """Close Redis connection."""
    global redis_client
    if redis_client:
        await redis_client.close()
        logger.info("Redis disconnected")


async def get_redis() -> redis.Redis:
    """Get Redis client."""
    return redis_client


# ========== Cache Helpers ==========

async def cache_set(key: str, value: str, ttl: int = 300):
    """Set a cache value with TTL (default 5 min)."""
    if redis_client:
        await redis_client.setex(key, ttl, value)


async def cache_get(key: str) -> str:
    """Get a cached value."""
    if redis_client:
        return await redis_client.get(key)
    return None


async def cache_delete(key: str):
    """Delete a cached value."""
    if redis_client:
        await redis_client.delete(key)


# ========== Rate Limiting ==========

async def check_rate_limit(key: str, limit: int, window: int = 60) -> bool:
    """Check if rate limit is exceeded. Returns True if allowed."""
    if not redis_client:
        return True

    current = await redis_client.get(key)
    if current is None:
        await redis_client.setex(key, window, 1)
        return True

    if int(current) >= limit:
        return False

    await redis_client.incr(key)
    return True
