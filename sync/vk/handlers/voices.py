from ..core import bot
from vkbottle.user import Message
from ...tg.core import bot as tg
from ..utils import create_vk_link, check_bundle
from ...utils import get_file_from_url


@bot.on.message(attachment=["audio_message"])
@check_bundle
async def on_audio_message(message: Message, bundle):
    user_info = await bot.api.users.get(message.from_id)
    voice_file = await get_file_from_url(message.attachments[0].audio_message.link_ogg)

    await tg.send_voice(
        bundle.tg_id,
        voice_file,
        f"<a href='{create_vk_link(message.from_id)}'>{user_info[0].first_name} {user_info[0].last_name}</a>\n",
        parse_mode="html",
        disable_notification=True,
    )
