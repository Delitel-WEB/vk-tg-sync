from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from ...cfg import tgBotToken


storage = MemoryStorage()
bot = Bot(tgBotToken)
dp = Dispatcher(bot, storage=storage)