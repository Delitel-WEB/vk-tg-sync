from ..core import bot
from .photos import get_photo_from_url


async def update_chat_info(chat_id: int, title: str, preview: str):
    """
    Обновление информации о группе.
    Название, Фото
    """

    if preview:
        photo = await get_photo_from_url(preview)
        await bot.set_chat_photo(chat_id, photo)

    await bot.set_chat_title(chat_id, title)
