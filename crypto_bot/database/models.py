"""
Файл с моделями машины состояний
"""


from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMDeal(StatesGroup):
    partner_id = State()
    first_cur = State()
    first_amount = State()
    second_cur = State()
    second_amount = State()
    city = State()
    profit = State()
