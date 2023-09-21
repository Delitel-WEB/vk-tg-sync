from ..core import bot
from vkbottle.user import Message
from ...db import Sessions
from ...db.models import Conversations
from sqlalchemy import select
from ...tg.core import bot as tg
from ..utils import create_vk_link
from ...utils import get_file_from_url
from vkbottle.dispatch.rules import ABCRule
from aiogram.types import InputMediaPhoto


class PhotoRule(ABCRule[Message]):
    """
    Кастомное правило которое будет срабатывать если
    будет отправлено фото
    """

    async def check(self, event: Message):
        if event.attachments:
            if event.attachments[0].photo:
                return True
            else:
                return False
        else:
            return False


@bot.on.message(PhotoRule())
async def on_photo(message: Message):
    async with Sessions() as session:
        bundle = await session.scalar(
            select(Conversations).where(Conversations.vk_id == message.peer_id)
        )
        if bundle:
            user_info = await bot.api.users.get(message.from_id)
            text = f"<a href='{create_vk_link(message.from_id)}'>{user_info[0].first_name} {user_info[0].last_name}</a>\n"
            if message.text:
                text += "‾" * 10
                text += f"\n{message.text}"

            photos = []
            for index, attachment in enumerate(message.attachments):
                if attachment and attachment.photo:
                    photos.append(
                        InputMediaPhoto(
                            await get_file_from_url(
                                await get_best_quality_image(attachment.photo.sizes)
                            ),
                            parse_mode="html",
                            caption=text if index == 0 else None,
                        )
                    )
            await tg.send_media_group(bundle.tg_id, photos)


async def get_best_quality_image(sizes: list):
    max_quality = None
    max_quality_url = None

    for image_info in sizes:
        width = image_info.width
        height = image_info.height

        if width > 0 and height > 0:
            if max_quality is None or (
                width > max_quality.width and height > max_quality.height
            ):
                max_quality = image_info
                max_quality_url = image_info.url

    return max_quality_url
