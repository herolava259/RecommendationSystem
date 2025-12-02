import redis.asyncio as aioredis
from redis import Redis

from config import Config


JTI_EXPIRY = 3600 * 2

token_blocklist: Redis = aioredis.from_url(Config.REDIS_URL)

async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.set(nam=jti, value="", ex=JTI_EXPIRY)

async def token_in_blocklist(jti: str)-> bool:
    jti = await token_blocklist.get(jti)

    return jti is not None