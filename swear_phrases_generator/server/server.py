from quart import Quart
from hypercorn.asyncio import serve
from hypercorn.config import Config as HyperCFG


from .blueprints.webgui import webgui

def build_app():
    app = Quart(__name__)
    app.register_blueprint(webgui)

    return app


async def run_server(app : Quart):
    cfg = HyperCFG()
    cfg.bind = f'0.0.0.0:{5000}'

    return await serve(app, cfg)

