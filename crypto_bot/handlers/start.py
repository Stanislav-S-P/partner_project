"""
Файл с хэндлерами старт/хэлп и регистрация
"""
import re
from datetime import datetime
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from database.database import select_auth_user, insert_list_deal
from database.models import FSMDeal
from keyboards import key_text
from keyboards.keyboards import menu_keyboard, cur_keyboard
from loader import bot, logger
from settings import constants


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


async def make_a_deal_command(message: types.Message) -> None:
    """
    Хэндлер - обрабатывает команду /make_a_deal
    :param message: Message
    :return: None
    """
    try:
        await FSMDeal.partner_id.set()
        await bot.send_message(message.from_user.id, constants.PARTNER_ID)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def partner_id_state(message: types.Message, state: FSMContext) -> None:
    """
    Хэндлер - обрабатывает состояние partner_id
    :param message: Message
    :param state: FSMContext
    :return: None
    """
    try:
        if message.text.isdigit():
            if select_auth_user(message.text):
                async with state.proxy() as data:
                    data['partner_id'] = message.text
                await FSMDeal.next()
                await bot.send_message(message.from_user.id, constants.FIRST_CUR, reply_markup=cur_keyboard())
            else:
                await bot.send_message(message.from_user.id, constants.EMPTY_PARTNER)
        else:
            await bot.send_message(message.from_user.id, constants.INCORRECT_PARTNER_ID)
            await bot.send_message(message.from_user.id, constants.PARTNER_ID)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def first_cur_state(call: types.CallbackQuery, state: FSMContext) -> None:
    """
    Хэндлер - обрабатывает состояние first_cur
    :param call: CallbackQuery
    :param state: FSMContext
    :return: None
    """
    try:
        await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id)
        async with state.proxy() as data:
            data['first_cur'] = call.data
        await FSMDeal.next()
        await bot.send_message(call.from_user.id, constants.FIRST_AMOUNT)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def first_amount_state(message: types.Message, state: FSMContext) -> None:
    """
    Хэндлер - обрабатывает состояние first_amount
    :param message: Message
    :param state: FSMContext
    :return: None
    """
    try:
        if [message.text] == re.findall(r'\d+[.,]\d+', message.text) or message.text.isdigit():
            if [message.text] == re.findall(r'\d+[,]\d+', message.text):
                amount = re.sub(r'[,]', '.', message.text)
            elif [message.text] == re.findall(r'\d+[.]\d+', message.text) or message.text.isdigit():
                amount = message.text
            async with state.proxy() as data:
                data['first_amount'] = amount
            await FSMDeal.next()
            await bot.send_message(message.from_user.id, constants.SECOND_CUR, reply_markup=cur_keyboard())
        else:
            await bot.send_message(message.from_user.id, constants.INCORRECT_AMOUNT)
            await bot.send_message(message.from_user.id, constants.FIRST_AMOUNT)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def second_cur_state(call: types.CallbackQuery, state: FSMContext) -> None:
    """
    Хэндлер - обрабатывает состояние second_cur
    :param call: CallbackQuery
    :param state: FSMContext
    :return: None
    """
    try:
        await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id)
        async with state.proxy() as data:
            data['second_cur'] = call.data
        await FSMDeal.next()
        await bot.send_message(call.from_user.id, constants.SECOND_AMOUNT)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def second_amount_state(message: types.Message, state: FSMContext) -> None:
    """
    Хэндлер - обрабатывает состояние second_amount
    :param message: Message
    :param state: FSMContext
    :return: None
    """
    try:
        if [message.text] == re.findall(r'\d+[.,]\d+', message.text) or message.text.isdigit():
            if [message.text] == re.findall(r'\d+[,]\d+', message.text):
                amount = re.sub(r'[,]', '.', message.text)
            elif [message.text] == re.findall(r'\d+[.]\d+', message.text) or message.text.isdigit():
                amount = message.text
            async with state.proxy() as data:
                data['second_amount'] = amount
            await FSMDeal.next()
            await bot.send_message(message.from_user.id, constants.CITY)
        else:
            await bot.send_message(message.from_user.id, constants.INCORRECT_AMOUNT)
            await bot.send_message(message.from_user.id, constants.SECOND_AMOUNT)
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
            data['city'] = message.text
        await FSMDeal.next()
        await bot.send_message(message.from_user.id, constants.PROFIT)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def profit_state(message: types.Message, state: FSMContext) -> None:
    """
    Хэндлер - обрабатывает состояние profit
    :param message: Message
    :param state: FSMContext
    :return: None
    """
    try:
        if [message.text] == re.findall(r'\d+[.,]\d+', message.text) or message.text.isdigit():
            if [message.text] == re.findall(r'\d+[,]\d+', message.text):
                amount = re.sub(r'[,]', '.', message.text)
            elif [message.text] == re.findall(r'\d+[.]\d+', message.text) or message.text.isdigit():
                amount = message.text
            async with state.proxy() as data:
                insert_list_deal((
                    data['partner_id'], datetime.today(), data['first_cur'],
                    data['first_amount'], data['second_cur'], data['city'],
                    data['second_amount'], amount, 'Проведена'
                ))
            await bot.send_message(message.from_user.id, constants.COMPLETE, reply_markup=menu_keyboard())
            await state.finish()
        else:
            await bot.send_message(message.from_user.id, constants.INCORRECT_PROFIT)
            await bot.send_message(message.from_user.id, constants.PROFIT)
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
        elif message.text == '/make_a_deal' or message.text == key_text.MAKE_A_DEAL:
            await make_a_deal_command(message)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


def register_start_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(cancel_state, Text(startswith=['/start', '/help', '/make_a_deal']), state='*')
    dp.register_message_handler(
        cancel_state, lambda message: message.text in [key_text.HELP, key_text.MAKE_A_DEAL], state='*'
    )
    dp.register_message_handler(start_command, commands=['start'], state=None)
    dp.register_message_handler(help_command, commands=['help'], state=None)
    dp.register_message_handler(help_command, lambda message: message.text == key_text.HELP, state=None)
    dp.register_message_handler(make_a_deal_command, commands=['make_a_deal'], state=None)
    dp.register_message_handler(make_a_deal_command, lambda message: message.text == key_text.MAKE_A_DEAL, state=None)
    dp.register_message_handler(partner_id_state, content_types=['text'], state=FSMDeal.partner_id)
    dp.register_callback_query_handler(
        first_cur_state, lambda call: call.data in key_text.CURRENCY, state=FSMDeal.first_cur
    )
    dp.register_message_handler(first_amount_state, content_types=['text'], state=FSMDeal.first_amount)
    dp.register_callback_query_handler(
        second_cur_state, lambda call: call.data in key_text.CURRENCY, state=FSMDeal.second_cur
    )
    dp.register_message_handler(second_amount_state, content_types=['text'], state=FSMDeal.second_amount)
    dp.register_message_handler(city_state, content_types=['text'], state=FSMDeal.city)
    dp.register_message_handler(profit_state, content_types=['text'], state=FSMDeal.profit)
