from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def yes_or_no_kb():
    """Клавиатура Да или Нет"""

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text="✅ Да",
            callback_data="yes"
        ),
        InlineKeyboardButton(
            text="❌ Нет",
            callback_data="no"
        )
    )
    
    return keyboard