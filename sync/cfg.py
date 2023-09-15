import os
from .exc import ConfigError


try:
    tgBotToken = os.environ["tgBotToken"]
    vkBotToken = os.environ["vkBotToken"]
except KeyError:
    raise ConfigError