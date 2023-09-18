import os
from .exc import ConfigError


try:
    tgBotToken = os.environ["tgBotToken"]
    vkBotToken = os.environ["vkBotToken"]
    dbPassword = os.environ["dbPassword"]
except KeyError:
    raise ConfigError
