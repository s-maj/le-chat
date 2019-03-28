import logging
import weakref

from aiohttp import web

from redis import init_redis, close_redis
from routes import setup_routes
from websocket import close_websockets


async def init_app():
    app = web.Application()
    app["websockets"] = weakref.WeakSet()

    app.on_startup.append(init_redis)
    app.on_shutdown.append(close_websockets)
    app.on_cleanup.append(close_redis)
    setup_routes(app)

    return app


def main():
    logging.basicConfig(level=logging.DEBUG)

    app = init_app()
    web.run_app(app)


if __name__ == "__main__":
    main()
