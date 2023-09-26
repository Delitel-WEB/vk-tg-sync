from ..core import bot
from vkbottle.user import Message
from ...tg.core import bot as tg
from ..utils import create_vk_link, check_bundle, get_best_quality_video
from ...utils import get_file_from_url
from vkbottle.dispatch.rules import ABCRule


class CircleRule(ABCRule[Message]):
    """
    Кастомное правило которое будет срабатывать если
    будет отправлен кружок
    """

    async def check(self, event: Message):
        if event.attachments:
            if event.attachments[0].video:
                width = event.attachments[0].video.width
                height = event.attachments[0].video.width
                if width == 480 and height == 480:
                    return True

        return False


@bot.on.message(CircleRule())
@check_bundle
async def on_circle(message: Message, bundle):
    user_info = await bot.api.users.get(message.from_id)
    text = f"<a href='{create_vk_link(message.from_id)}'>{user_info[0].first_name} {user_info[0].last_name}</a>\n"

    circle = await get_file_from_url(
        await get_best_quality_video(message.attachments[0].video.files)
    )

    circle_message = await tg.send_video_note(chat_id=bundle.tg_id, video_note=circle)
    await circle_message.reply(
        text,
        parse_mode="html",
        disable_web_page_preview=True,
        disable_notification=True,
    )
