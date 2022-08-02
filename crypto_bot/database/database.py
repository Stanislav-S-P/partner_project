"""
Файл - взаимодействует с базой данных
"""


import sqlite3
from sqlite3 import Cursor
from typing import Callable, Tuple
from loader import logger


def db_decorator(func: Callable) -> Callable:
    """
    Декоратор - Производит подключение к БД.
    :param func: Callablе
    :return: Callable
    """

    def wrapped_func(*args, **kwargs):
        try:
            connection = sqlite3.connect('../crypto/db.sqlite3')
            connection.isolation_level = None
            cursor = connection.cursor()
            result = func(*args, **kwargs, cursor=cursor)
            return result
        except TypeError as ex:
            print(ex)
        except Exception as ex:
            logger.error('Ошибка БД', exc_info=ex)
            print(ex, 'Ошибка БД')
        finally:
            connection.close()

    return wrapped_func


"""Запросы к таблице auth_user"""


@db_decorator
def select_auth_user(partner_id: int, cursor: Cursor) -> bool:
    cursor.execute("SELECT partner_id FROM app_crypto_customuser WHERE partner_id=?", (partner_id, ))
    result = cursor.fetchall()
    if result:
        return True


"""Запросы к таблице list_deal"""


@db_decorator
def insert_list_deal(list_deal: Tuple, cursor: Cursor) -> None:
    cursor.execute("INSERT INTO list_deal ("
                   "partner_id, created_at, first_cur, first_amount, second_cur, city, second_amount, profit, status"
                   ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", list_deal)
