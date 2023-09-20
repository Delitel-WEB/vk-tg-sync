from .core import bot
from . import handlers


def start_vk():
    bot.run_forever()
