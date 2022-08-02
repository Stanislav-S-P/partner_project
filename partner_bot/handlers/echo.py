"""
Файл - содержит хэндлер для отлова сообщений вне сценария
"""

from aiogram import Dispatcher, types
from loader import logger, bot
from settings import constants


async def echo_handler(message: types.Message) -> None:
    """
    Хэндлер - оповещает бота о некорректной команде (Эхо)
    :param message: Message
    :return: None
    """
    try:
        await bot.send_message(message.from_user.id, constants.INCORRECT_INPUT)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


def register_echo_handlers(dp: Dispatcher) -> None:
    """
    Функция - регистрирует все хэндлеры файла echo.py
    :param dp: Dispatcher
    :return: None
    """
    dp.register_message_handler(echo_handler)