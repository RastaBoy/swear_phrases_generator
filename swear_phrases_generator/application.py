import asyncio

from .server import run_server, build_app

def run_application():
    asyncio.run(run_server(build_app()))
