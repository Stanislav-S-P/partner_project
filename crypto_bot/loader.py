"""Файл - инициализирующий бота, диспетчер, логгер и хранилище для машины состояния"""


from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from logging_config import custom_logger
from settings import settings
from aiogram.contrib.fsm_storage.memory import MemoryStorage


logger = custom_logger('bot_logger')


storage = MemoryStorage()


bot = Bot(token=settings.TOKEN)
dp = Dispatcher(bot, storage=storage)