from aiohttp import web

from websocket import websocket_handler


def setup_routes(app):
    app.add_routes([web.get("/ws", websocket_handler)])
