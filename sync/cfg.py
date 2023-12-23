import os
from .exc import ConfigError


try:
    tgBotToken = os.environ["TG_BOT_TOKEN"]
    vkBotToken = os.environ["VK_BOT_TOKEN"]
    DB_PASS = os.environ["DB_PASS"]
    DB_IP = os.environ["DB_IP"]
    DB_NAME = os.environ["DB_NAME"]
except KeyError:
    raise ConfigError
