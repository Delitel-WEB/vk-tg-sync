from aiogram.dispatcher.filters.state import State, StatesGroup


class BindChats(StatesGroup):
    """Связка чатов"""

    select_type = State() # Выбор типа чата ВК 
    vk_id = State() # Ввод id чата ВК
    verify_choice_vk = State() # Подтверждение выбора чата ВК
    tg_id = State() # Ввод id чата ТГ