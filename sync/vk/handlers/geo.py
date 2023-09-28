from ..core import bot
from vkbottle.user import Message
from ...tg.core import bot as tg
from ..utils import create_vk_link, check_bundle
from vkbottle.dispatch.rules import ABCRule


class GeoRule(ABCRule[Message]):
    """
    Кастомное правило которое будет срабатывать если
    будет отправлена геолокация
    """

    async def check(self, event: Message):
        if event.geo:
            return True

        return False


@bot.on.message(GeoRule())
@check_bundle
async def on_geo(message: Message, bundle):
    user_info = await bot.api.users.get(message.from_id)

    latitude = message.geo.coordinates.latitude
    longitude = message.geo.coordinates.longitude

    geo_message = await tg.send_location(
        bundle.tg_id, latitude=latitude, longitude=longitude
    )
    await geo_message.reply(
        f"<a href='{create_vk_link(message.from_id)}'>{user_info[0].first_name} {user_info[0].last_name}</a>\n",
        parse_mode="html",
        disable_web_page_preview=True,
        disable_notification=True,
    )
