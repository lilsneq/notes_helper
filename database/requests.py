# ЗПРОСЫ НА ПОЛУЧЕНИЕ ОТВЕТА БЕЗ ИЗМЕНЕНИЙ В БД


# ИМПОРТЫ
import asyncpg
import logging
import sys
from database import connection



class CreateRequest:

    @staticmethod
    async def create_table():
        """Создание таблицы при включении бота"""

        try:
            async with connection.db_pool.acquire() as conn:
                query = """
                    CREATE TABLE IF NOT EXISTS public.notes_tg_bot(
                        username_id BIGINT PRIMARY KEY,
                        notes_id VARCHAR(255) NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """
                await conn.execute(query)
                print("ТАБЛИЦА УСПЕШНО СОЗДАНА")


        except Exception as e:
            logging.error(f'ОШИБКА СОЗДАНИЯ ТАБЛИЦЫ {e}', exc_info=True)


    @staticmethod
    async def add_notes_id(username_id):
        """Добавление пользователя в таблицу при инициализации бота в первый раз"""

        try:
            async with connection.db_pool.acquire() as conn:
                query = """
                    INSERT INTO public.notes_tg_bot(username_id)
                    VALUES($1)
                    ON CONFLICT (username_id) DO NOTHING;
                """

                await conn.execute(query, username_id, )

        except Exception as e:
            logging.error(f'ОШИБКА ДОБАВЛЕНИЯ ПОЛЬЗОВАТЕЛЯ В ТАБЛИЦУ {e}', exc_info=True)







