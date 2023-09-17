from aiogram.types import Message
from ..core import dp



@dp.message_handler(commands=["id"], state="*")
async def id(message: Message):
    await message.answer(message.chat.id)