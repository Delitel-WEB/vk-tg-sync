from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def select_chat_type_kb():
    """Клавиатура выбора Типа чата ВКонтакте"""

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(text="📬 Личный Чат", callback_data="direct_message"),
        InlineKeyboardButton(text="👥 Группа", callback_data="group"),
    )

    return keyboard
