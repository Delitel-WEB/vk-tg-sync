from aiogram import Bot, Dispatcher
from ...cfg import tgBotToken

bot = Bot(tgBotToken)
dp = Dispatcher(bot)