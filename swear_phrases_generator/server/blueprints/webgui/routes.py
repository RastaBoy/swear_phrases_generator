
from . import webgui

@webgui.get('/')
async def index():
    return '<h1>Здесь будет фронт для настроек бота.</h1><h2>Но пока его нет -___-"</h2>'

