from redis.asyncio import Redis
from src.config import Config

_redis_client: Redis | None = None
_blocklist: set[str] = set()  # in-memory fallback if Redis is unavailable


async def _get_redis() -> Redis | None:
    global _redis_client
    if _redis_client is None:
        try:
            client = Redis.from_url(Config.REDIS_URL, decode_responses=True)
            await client.ping()
            _redis_client = client
        except Exception:
            _redis_client = None
    return _redis_client


async def add_token_to_blocklist(jti: str) -> None:
    client = await _get_redis()
    if client:
        await client.set(f"blocklist:{jti}", "1", ex=Config.REFRESH_TOKEN_EXPIRY)
    else:
        _blocklist.add(jti)


async def token_in_blocklist(jti: str) -> bool:
    client = await _get_redis()
    if client:
        return await client.exists(f"blocklist:{jti}") > 0
    return jti in _blocklist
