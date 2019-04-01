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


async def read_stream(app, ws, chans):
    try:
        while True:
            chunk_msgs = await app["redis"].xread(list(chans.keys()), latest_ids=list(chans.values()), timeout=None)

            for msg in chunk_msgs:
                name, stamp, _ = msg
                if chans[name] < stamp:
                    chans[name] = stamp
                await ws.send_str(str(msg))

            await asyncio.sleep(1)

    except asyncio.CancelledError:
        pass
    except aioredis.ConnectionForcedCloseError:
        pass
