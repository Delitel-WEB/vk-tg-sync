from ..core import dp
from ...vk.core import bot as vk
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from ..states import BindChats
from ..keyboard import select_chat_type_kb, yes_or_no_kb
# from ...db import Sessions
# from ...db.models import Conversations
# from sqlalchemy import select


@dp.message_handler(commands=["bind_chats"], state="*")
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
        else: ... # Выбор группы
    else:
        await message.answer(
            "Введите <b>ID</b> вк группы в формате <code>123456789</code> или <code>-123456789</code>.\n\n⚠️ <u>Целым числом!</u>",
            parse_mode="html"
        )


#####################################
#    Подтверждение выбора чата вк   #
#####################################
@dp.callback_query_handler(text="yes", state=BindChats.verify_choice_vk)
async def correct_choice(query: CallbackQuery, state: FSMContext):
    await BindChats.tg_id.set()
    await query.message.edit_text(
        "Отлично! Теперь введите ID группы Телеграм или перешлите любое сообщение из него!\n"
        "Бот должен быть администратором этой группы и иметь все права!"
    )
    


@dp.callback_query_handler(text="no", state=BindChats.verify_choice_vk)
async def wrong_choice(query: CallbackQuery, state: FSMContext):
    await BindChats.vk_id.set()
    await query.message.edit_text(
        "Введите <b>ID</b> вк Чата в формате <code>123456789</code>.",
        parse_mode="html"
    )




# @dp.message_handler(state=BindChats.vk_id)
# async def get_vk_id(message: Message, state: FSMContext):
#     """Получение id ВК чата"""
#     if message.text.isdigit():
#         # chat = await bot.api.messages.send(peer_id=2000000000+211, message="123", random_id=randint(10,5000))
#         # chat = await bot.api.messages.get_conversations_by_id(peer_ids=)
#         # print(chat)
#     else:
#         await message.answer(
#             "Введите id чата в формате <code>123456789</code> или <code>-123456789</code>",
#             parse_mode="html",
#         )
