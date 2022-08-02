"""Файл для запуска бота. Содержит в себе все регистраторы приложения"""
from aiogram import types, Dispatcher
from loader import dp
from aiogram.utils import executor
from handlers import start, echo


async def set_default_commands(dp: Dispatcher):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Старт"),
            types.BotCommand("help", "Помощь"),
            types.BotCommand("buy", "Купить"),
            types.BotCommand("sell", "Продать"),
        ]
    )


start.register_start_handlers(dp)
echo.register_echo_handlers(dp)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=set_default_commands, skip_updates=True)