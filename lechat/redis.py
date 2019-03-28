import aioredis


async def init_redis(app):
    redis = await aioredis.create_redis_pool("redis://localhost", minsize=5, maxsize=10)
    app["redis"] = redis


async def close_redis(app):
    app["redis"].close()
    await app["redis"].wait_closed()
