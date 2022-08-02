"""
Файл с хэндлерами старт/хэлп и регистрация
"""
import re
from datetime import datetime
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from database.database import insert_buy_request, insert_sell_request, select_operator
from database.models import FSMDeal
from keyboards import key_text
from keyboards.keyboards import menu_keyboard, crypto_keyboard, fiat_keyboard
from loader import bot, logger
from settings import constants
from settings.settings import PARTNER_ID


async def start_command(message: types.Message) -> None:
    """
    Хэндлер - обрабатывает команду /start
    :param message: Message
    :return: None
    """
    try:
        await bot.send_message(message.from_user.id, constants.WELCOME, reply_markup=menu_keyboard())
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def help_command(message: types.Message) -> None:
    """
    Хэндлер - обрабатывает команду /help
    :param message: Message
    :return: None
    """
    try:
        await bot.send_message(message.from_user.id, constants.HELP)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def buy_sell_command(message: types.Message, state: FSMContext) -> None:
    """
    Хэндлер - обрабатывает команды /buy и /sell
    :param message: Message
    :param state: FSMContext
    :return: None
    """
    try:
        await FSMDeal.crypto.set()
        async with state.proxy() as data:
            if message.text in [key_text.BUY, 'buy']:
                data['action'] = key_text.BUY
                text = constants.BUY_CUR
            else:
                data['action'] = key_text.SELL
                text = constants.SELL_CUR
            await bot.send_message(message.from_user.id, text, reply_markup=crypto_keyboard())
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def crypto_state(call: types.CallbackQuery, state: FSMContext) -> None:
    """
    Хэндлер - обрабатывает состояние crypto
    :param call: CallbackQuery
    :param state: FSMContext
    :return: None
    """
    try:
        await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id)
        async with state.proxy() as data:
            data['crypto'] = call.data
            if data['action'] == key_text.BUY:
                text = constants.QUANTITY_BUY
            elif data['action'] == key_text.SELL:
                text = constants.QUANTITY_SELL
        await FSMDeal.next()
        await bot.send_message(call.from_user.id, text)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def quantity_state(message: types.Message, state: FSMContext) -> None:
    """
    Хэндлер - обрабатывает состояние quantity
    :param message: Message
    :param state: FSMContext
    :return: None
    """
    try:
        if [message.text] == re.findall(r'\d+[.,]\d+', message.text) or message.text.isdigit():
            if [message.text] == re.findall(r'\d+[,]\d+', message.text):
                quantity = re.sub(r'[,]', '.', message.text)
            elif [message.text] == re.findall(r'\d+[.]\d+', message.text) or message.text.isdigit():
                quantity = message.text
            async with state.proxy() as data:
                data['quantity'] = quantity
                if data['action'] == key_text.BUY:
                    text = constants.BUY_FIAT_CUR
                elif data['action'] == key_text.SELL:
                    text = constants.SELL_FIAT_CUR
            await FSMDeal.next()
            await bot.send_message(message.from_user.id, text, reply_markup=fiat_keyboard())
        else:
            await bot.send_message(message.from_user.id, constants.INCORRECT_AMOUNT)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def fiat_state(call: types.CallbackQuery, state: FSMContext) -> None:
    """
    Хэндлер - обрабатывает состояние fiat
    :param call: CallbackQuery
    :param state: FSMContext
    :return: None
    """
    try:
        await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id)
        async with state.proxy() as data:
            data['fiat'] = call.data
        await FSMDeal.next()
        await bot.send_message(call.from_user.id, constants.CITY)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def city_state(message: types.Message, state: FSMContext) -> None:
    """
    Хэндлер - обрабатывает состояние city
    :param message: Message
    :param state: FSMContext
    :return: None
    """
    try:
        async with state.proxy() as data:
            operator = select_operator()
            un_operator = '@' + operator[1]
            await bot.send_message(
                message.from_user.id, constants.COMPLETE.format(un_operator), reply_markup=menu_keyboard()
            )
            if data['action'] == key_text.BUY:
                text = 'Покупка'
                insert_buy_request(
                    (PARTNER_ID, datetime.today(), data['crypto'],
                     data['quantity'], data['fiat'], message.text, 'Новая')
                )
            elif data['action'] == key_text.SELL:
                text = 'Продажа'
                insert_sell_request(
                    (PARTNER_ID, datetime.today(), data['fiat'],
                     data['quantity'], data['crypto'], message.text, 'Новая')
                )
            if message.from_user.username:
                username = '@' + message.from_user.username
            else:
                username = message.from_user.id
            await bot.send_message(
                operator[0], constants.OPERATOR.format(
                    text, username, datetime.today().strftime('%d.%m.%Y %H:%M:%S'),
                    data['crypto'], data['quantity'], data['fiat'], message.text
                ), parse_mode='Markdown'
            )
        await state.finish()
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def cancel_state(message: types.Message, state: FSMContext) -> None:
    """
    Хэндлер - реагирует на команды и выводит из машины состояния пользователя
    :param message: Message
    :param state: FSMContext
    :return: None
    """
    try:
        current_state = await state.get_state()
        if current_state is not None:
            await state.finish()
        if message.text == '/start':
            await start_command(message)
        elif message.text == '/help' or message.text == key_text.HELP:
            await help_command(message)
        elif message.text in ['/buy', key_text.BUY, '/sell', key_text.SELL]:
            await buy_sell_command(message, state)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


def register_start_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(start_command, commands=['start'], state=None)
    dp.register_message_handler(help_command, commands=['help'], state=None)
    dp.register_message_handler(help_command, lambda message: message.text == key_text.HELP, state=None)
    dp.register_message_handler(buy_sell_command, commands=['buy', 'sell'], state=None)
    dp.register_message_handler(
        buy_sell_command, lambda message: message.text in [key_text.BUY, key_text.SELL], state=None
    )
    dp.register_message_handler(cancel_state, Text(startswith=['/start', '/help', '/buy', '/sell']), state='*')
    dp.register_message_handler(
        cancel_state, lambda message: message.text in [key_text.HELP, key_text.BUY, key_text.SELL], state='*'
    )
    dp.register_callback_query_handler(
        crypto_state, lambda call: call.data in key_text.CRYPTO, state=FSMDeal.crypto
    )
    dp.register_message_handler(quantity_state, content_types=['text'], state=FSMDeal.quantity)
    dp.register_callback_query_handler(fiat_state, lambda call: call.data in key_text.FIAT, state=FSMDeal.fiat)
    dp.register_message_handler(city_state, content_types=['text'], state=FSMDeal.city)
