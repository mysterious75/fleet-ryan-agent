"""
Fleet-Ryan Backend — Redis Configuration (Optional)
"""

import structlog
from app.core.config import settings

logger = structlog.get_logger()

# Try to import redis — it's optional
try:
    import redis.asyncio as redis
    HAS_REDIS = True
except ImportError:
    HAS_REDIS = False
    logger.info("Redis package not installed — running without cache")

# Redis client
redis_client = None


async def init_redis():
    """Initialize Redis connection (optional — works without Redis)."""
    global redis_client

    if not HAS_REDIS:
        logger.info("Redis not available — running without cache")
        return

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
        try:
            await redis_client.close()
            logger.info("Redis disconnected")
        except Exception:
            pass
        redis_client = None


async def get_redis():
    """Get Redis client."""
    return redis_client


# ========== Cache Helpers ==========

async def cache_set(key: str, value: str, ttl: int = 300):
    """Set a cache value with TTL (default 5 min)."""
    if redis_client:
        try:
            await redis_client.setex(key, ttl, value)
        except Exception:
            pass


async def cache_get(key: str) -> str:
    """Get a cached value."""
    if redis_client:
        try:
            return await redis_client.get(key)
        except Exception:
            return None
    return None


async def cache_delete(key: str):
    """Delete a cached value."""
    if redis_client:
        try:
            await redis_client.delete(key)
        except Exception:
            pass


# ========== Rate Limiting ==========

async def check_rate_limit(key: str, limit: int, window: int = 60) -> bool:
    """Check if rate limit is exceeded. Returns True if allowed."""
    if not redis_client:
        return True

    try:
        current = await redis_client.get(key)
        if current is None:
            await redis_client.setex(key, window, 1)
            return True

        if int(current) >= limit:
            return False

        await redis_client.incr(key)
        return True
    except Exception:
        return True
