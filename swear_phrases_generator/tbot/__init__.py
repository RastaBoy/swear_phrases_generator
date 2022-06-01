from ..aiotelegrambot.types import Incoming
from ..aiotelegrambot import Bot, Client, Content, Handlers, Message, handler
from ..aiotelegrambot.rules import Contains

class TBot():
    _handlers = Handlers()
    state = dict()

    def __init__(self):
        ...
    


    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
    
        return cls._instance
