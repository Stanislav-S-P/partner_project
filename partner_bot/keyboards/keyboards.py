from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from keyboards import key_text


def menu_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    return keyboard.add(
        KeyboardButton(text=key_text.BUY), KeyboardButton(text=key_text.SELL), KeyboardButton(text=key_text.HELP),
    )


def crypto_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=3)
    currency_list = []
    for cur in key_text.CRYPTO:
        currency_list.append(InlineKeyboardButton(text=cur, callback_data=cur))
    return keyboard.add(
        currency_list[0], currency_list[1], currency_list[2], currency_list[3], currency_list[4], currency_list[5]
    )


def fiat_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=3)
    currency_list = []
    for cur in key_text.FIAT:
        currency_list.append(InlineKeyboardButton(text=cur, callback_data=cur))
    return keyboard.add(
        currency_list[0], currency_list[1], currency_list[2]
    )
