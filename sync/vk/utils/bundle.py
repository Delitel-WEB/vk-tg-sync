from ...db import Sessions
from ...db.models import Conversations
from sqlalchemy import select
from functools import wraps
from vkbottle.user import Message


def check_bundle(func):
    @wraps(func)
    async def wrapper(message: Message, *args):
        async with Sessions() as session:
            bundle = await session.scalar(
                select(Conversations).where(Conversations.vk_id == message.peer_id)
            )
            if bundle:
                await func(message, bundle, *args)

    return wrapper
