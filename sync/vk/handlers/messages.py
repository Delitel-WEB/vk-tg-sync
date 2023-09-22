from ..core import bot
from vkbottle.user import Message
from ...db import Sessions
from ...db.models import Conversations
from sqlalchemy import select
from ...tg.core import bot as tg
from ..utils import create_vk_link


@bot.on.message()
async def on_message(message: Message):
    async with Sessions() as session:
        bundle = await session.scalar(
            select(Conversations).where(Conversations.vk_id == message.peer_id)
        )
        if bundle:
            user_info = await bot.api.users.get(message.from_id)
            await tg.send_message(
                bundle.tg_id,
                f"<a href='{create_vk_link(message.from_id)}'>{user_info[0].first_name} {user_info[0].last_name}</a>\n"
                + "‾" * 10
                + f"\n{message.text}",
                parse_mode="html",
                disable_web_page_preview=True,
            )
