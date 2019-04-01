from aiohttp import WSMsgType, WSCloseCode
from aiohttp import web
from redis import read_stream
import asyncio


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    request.app["websockets"].add(ws)
    asyncio.create_task(read_stream(request.app, ws))

    try:
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                if msg.data == "close":
                    await ws.close()
                else:

                    await request.app["redis"].xadd(
                        "general", {"msg": msg.data}, max_len=1000
                    )
            elif msg.type == WSMsgType.ERROR:
                print("ws connection closed with exception %s" % ws.exception())
    finally:
        request.app["websockets"].discard(ws)

    return ws


async def close_websockets(app):
    for ws in set(app["websockets"]):
        await ws.close(code=WSCloseCode.GOING_AWAY, message="Server shutdown")
