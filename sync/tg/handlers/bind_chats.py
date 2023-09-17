from ..core import dp
from ...vk.core import bot as vk
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from ..states import BindChats
from ..keyboard import select_chat_type_kb, yes_or_no_kb
from aiogram.utils.exceptions import ChatNotFound
from ...db import Sessions
from ...db.models import Conversations
from sqlalchemy import select


@dp.message_handler(commands=["bind_chat"], state="*")
async def bind_chats(message: Message, state: FSMContext):
    """Связка чатов ВК и ТГ"""
    await state.finish()  # Заканчиваем предыдущее состояние на случай повтора ввода
    await BindChats.select_type.set()
    await message.answer("Выберите тип Чата ВК!", reply_markup=select_chat_type_kb())


@dp.callback_query_handler(text="direct_message", state=BindChats.select_type)
async def direct_message_select(query: CallbackQuery, state: FSMContext):
    data = {}
    data["chat_type"] = "DM"
    await state.set_data(data)
    await BindChats.vk_id.set()

    await query.message.edit_text(
        "Введите <b>ID</b> вк Чата в формате <code>123456789</code>.",
        parse_mode="html"
    )


@dp.callback_query_handler(text="group", state=BindChats.select_type)
async def group_select(query: CallbackQuery, state: FSMContext):
    data = {}
    data["chat_type"] = "GR"
    await state.set_data(data)
    await BindChats.vk_id.set()

    await query.message.edit_text(
        "Введите <b>ID</b> вк группы в формате <code>123</code>.",
        parse_mode="html"
    )


@dp.message_handler(state=BindChats.vk_id)
async def get_vk_id(message: Message, state: FSMContext):
    if message.text.lstrip("-").isdigit():
        data = await state.get_data()
        if data["chat_type"] == "DM":
            chat = await vk.api.users.get(message.text)
            if chat:

                data["vk_chat_id"] = 2000000000+int(message.text)
                await state.set_data(data)

                await BindChats.verify_choice_vk.set()
                await message.answer(
                    f"Найден <b>{chat[0].first_name} {chat[0].last_name}</b>.\n\nПравильно?",
                    reply_markup=yes_or_no_kb(),
                    parse_mode="html"
                )
            else:
                await message.answer(
                    "Не удалось ничего найти!"
                )
        else:
            try:
                chat = await vk.api.messages.get_conversations_by_id(2000000000+int(message.text))
            except Exception as err:
                await message.answer(err)
                chat = None
            if chat:
                if not chat.items or not chat.items[0].chat_settings:
                    await message.answer(
                        "Не удалось ничего найти!"
                    )
                else:
                    data["vk_chat_id"] = 2000000000+int(message.text)
                    await state.set_data(data)

                    await BindChats.verify_choice_vk.set()
                    await message.answer(
                        f"Найден <b>{chat.items[0].chat_settings.title}</b>.\n\nПравильно?",
                        reply_markup=yes_or_no_kb(),
                        parse_mode="html"
                    )
    else:
        await message.answer(
            "Введите <b>ID</b> вк группы в формате <code>123</code>.\n\n⚠️ <u>Целым числом!</u>",
            parse_mode="html"
        )


#####################################
#    Подтверждение выбора чата вк   #
#####################################
@dp.callback_query_handler(text="yes", state=BindChats.verify_choice_vk)
async def correct_choice(query: CallbackQuery, state: FSMContext):
    await BindChats.tg_id.set()
    await query.message.edit_text(
        "👌 Отлично! Теперь пришлите ID чата телеграм который вы хотите соеденить с чатом ВК!\n"
        "🤖 Бот должен быть администратором этой группы и иметь все права!"
    )
    


@dp.callback_query_handler(text="no", state=BindChats.verify_choice_vk)
async def wrong_choice(query: CallbackQuery, state: FSMContext):
    await BindChats.vk_id.set()
    await query.message.edit_text(
        "Введите <b>ID</b> вк Чата в формате <code>123456789</code>.",
        parse_mode="html"
    )


#####################################
#       Получение чата Телеграм     #
#####################################
@dp.message_handler(state=BindChats.tg_id)
async def get_tg_id(message: Message, state: FSMContext):
    if message.text.lstrip("-").isdigit():
        if int(message.text) >= 0:
            await message.answer(
                "ID группы должен быть со знаком минус!\n"
                "Например: -123455667"
            )
        else:
            try:
                member = await message.bot.get_chat_member(int(message.text), message.bot.id)
            except ChatNotFound:
                await message.answer(
                    "Чат не существует или бот не имеет досутпа к чату!"
                )
            if not member.is_chat_admin():
                await message.answer(
                    "Бот должен быть администратором группы!\n"
                    "Сделайте его администратором и повторите попытку!"
                )
            else:
                async with Sessions() as session:
                    data = await state.get_data()
                    chat_exists = await session.scalar(select(Conversations).where(Conversations.vk_id == data["vk_chat_id"]))
                    if not chat_exists:

                        conversations = Conversations(
                            vk_id=data["vk_chat_id"],
                            tg_id=int(message.text)
                        )

                        session.add(conversations)
                        await session.commit()

                        await message.answer(
                            "Отлично!\n"
                            "Чаты успешно связаны!"
                        )
                    else:
                        await message.answer(
                            "Чат уже к чему-то подключен!"
                        )
                
                


    else:
        await message.answer(
            "Пришлите ID чата телеграм который вы хотите соеденить с чатом ВК!\n"
            "<u>Целым числом!</u>",
            parse_mode="html"
        )


