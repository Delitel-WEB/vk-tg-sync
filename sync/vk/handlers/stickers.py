from ..core import bot
from vkbottle.user import Message
from ...tg.core import bot as tg
from ..utils import create_vk_link, check_bundle
from ...utils import get_file_from_url
from vkbottle.dispatch.rules import ABCRule


class StrickersRule(ABCRule[Message]):
    """
    Кастомное правило которое будет срабатывать если
    будет отправлен любой стикер
    """

    async def check(self, event: Message):
        if event.attachments:
            if event.attachments[0].sticker:
                return True

        return False


@bot.on.message(StrickersRule())
@check_bundle
async def on_stickers(message: Message, bundle):
    user_info = await bot.api.users.get(message.from_id)
    sticker = await get_file_from_url(
        message.attachments[0].sticker.images_with_background[-1].url
    )
    sticker_message = await tg.send_sticker(bundle.tg_id, sticker=sticker)
    await sticker_message.reply(
        f"<a href='{create_vk_link(message.from_id)}'>{user_info[0].first_name} {user_info[0].last_name}</a>\n",
        parse_mode="html",
        disable_web_page_preview=True,
    )
