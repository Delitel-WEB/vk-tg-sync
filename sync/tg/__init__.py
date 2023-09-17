from .core import dp
from aiogram import executor
from .import inline

def start_tg():
    executor.start_polling(dp, skip_updates=True)
