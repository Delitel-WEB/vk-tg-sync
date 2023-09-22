from ..core import bot
from vkbottle.user import Message
from ...db import Sessions
from ...db.models import Conversations
from sqlalchemy import select
from ...tg.core import bot as tg
from ..utils import create_vk_link
from ...utils import get_file_from_url
from vkbottle.dispatch.rules import ABCRule
from aiogram.types import InputMediaVideo


class VideoRule(ABCRule[Message]):
    """
    Кастомное правило которое будет срабатывать если
    будет отправлено видео
    """

    async def check(self, event: Message):
        if event.attachments:
            if event.attachments[0].video:
                return True
            else:
                return False
        else:
            return False


@bot.on.message(VideoRule())
async def on_video(message: Message):
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

        videos = []
        for index, attachment in enumerate(message.attachments):
            if attachment and attachment.video:
                videos.append(
                    InputMediaVideo(
                        await get_file_from_url(
                            await get_best_quality_video(attachment.video.files)
                        ),
                        parse_mode="html",
                        caption=text if index == 0 else None,
                    )
                )
        await tg.send_media_group(bundle.tg_id, videos)


async def get_best_quality_video(files):
    qualities = [
        'mp4_2160',  # 4K
        'mp4_1440',  # 1440p
        'mp4_1080',  # 1080p
        'mp4_720',  # 720p
        'mp4_480',  # 480p
        'mp4_360',  # 360p
        'mp4_240',  # 240p
        'mp4_144',  # 144p
    ]

    for quality in qualities:
        if getattr(files, quality) is not None:
            return getattr(files, quality)

    return None
