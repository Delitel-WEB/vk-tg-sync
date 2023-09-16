from .core import dp
from aiogram import executor



async def execute():
    executor.start_polling(dp, skip_updates=True)