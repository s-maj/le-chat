import aioredis
import asyncio


async def init_redis(app):
    redis = await aioredis.create_redis_pool(
        "redis://localhost", minsize=10, maxsize=10, encoding="utf-8"
    )
    app["redis"] = redis


async def close_redis(app):
    app["redis"].close()
    await app["redis"].wait_closed()


async def read_stream(app, ws):
    try:
        all_msgs = await app["redis"].xrange("general", count=100)
        latest_id, _ = all_msgs[-1]

        for msg in all_msgs:
            await ws.send_str(str(msg))

        while True:
            print(latest_id)
            chunk_msgs = await app["redis"].xread(["general"], latest_ids=[latest_id])
            stream, latest_id, _ = chunk_msgs[-1]
            for msg in chunk_msgs:
                await ws.send_str(str(msg))

            await asyncio.sleep(1)

    except asyncio.CancelledError:
        pass
    except aioredis.ConnectionForcedCloseError:
        pass
