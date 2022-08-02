"""
Файл содержащий Token бота и данные для подключения к БД
"""

import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Файл .env отсутствует')
else:
    load_dotenv()


"""Токен бота"""
TOKEN = os.environ.get('TOKEN')