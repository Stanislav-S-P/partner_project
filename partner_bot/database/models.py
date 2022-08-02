"""
Файл с моделями машины состояний
"""

from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMDeal(StatesGroup):
    crypto = State()
    quantity = State()
    fiat = State()
    city = State()
