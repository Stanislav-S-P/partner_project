from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from keyboards import key_text


def menu_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    return keyboard.add(KeyboardButton(text=key_text.MAKE_A_DEAL), KeyboardButton(text=key_text.HELP),)


def cur_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=3)
    currency_list = []
    for cur in key_text.CURRENCY:
        currency_list.append(InlineKeyboardButton(text=cur, callback_data=cur))
    return keyboard.add(
        currency_list[0], currency_list[1], currency_list[2], currency_list[3], currency_list[4],
        currency_list[5], currency_list[6], currency_list[7], currency_list[8]
    )
