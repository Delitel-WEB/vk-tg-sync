from .core import dp
from aiogram import executor
from .import inline

def execute():
    executor.start_polling(dp, skip_updates=True)
