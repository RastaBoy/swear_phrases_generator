from .metaconfig.io import YAMLFileConfigIO
from .metaconfig.types import IntField, StrField, ConfigRoot



class Config(ConfigRoot):
    __io_class__ = YAMLFileConfigIO('settings.yaml')

    server_port = IntField(label='Server Port', default=5000)
    telegram_bot_token = StrField(label='Telegram Bot Token', default='')