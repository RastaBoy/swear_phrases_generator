from ..aiotelegrambot.types import Incoming
from ..aiotelegrambot import Bot, Client, Content, Handlers, Message, handler
from ..aiotelegrambot.rules import Contains

class TBot():
    _handlers = Handlers()
    state = dict()

    def __init__(self):
        ...
    
    async def _init_commands(self):
        commands = list()
        # for cmd in TBotCommands:
        #     commands.append(
        #         {
        #             'command' : cmd.value,
        #             'description' : tbot_commands_description.get(cmd)
        #         }
        #     )
        # await self.client.set_commands(commands)


    async def _initialize(self):
        # self.client = Client(token=Config().telebot.token, loop=asyncio.get_event_loop())
        
        # self.bot = Bot(self.client)
        # self.bot.add_handler(self.new, content_type=Content.COMMAND, rule=Contains(TBotCommands.NEW.value))
        # self.bot.add_handler(self.list, content_type=Content.COMMAND, rule=Contains(TBotCommands.LIST.value))
        # self.bot.add_handler(self.manage_callback, incoming=Incoming.CALLBACK_QUERY)
        # self.bot.add_handler(self.manage_text, content_type=Content.TEXT)
        
        # await self.bot.initialize(webhook=True)
        
        # await self._init_commands()
        ...

    async def poll(self):
        await self.bot._get_updates(.1)


    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
    
        return cls._instance
