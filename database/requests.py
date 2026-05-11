# ЗПРОСЫ НА ПОЛУЧЕНИЕ И ТВЕТЫ В БД

# ИМПОРТЫ
import asyncpg
import logging
import sys


from database import connection



class CreateRequest:

    @staticmethod
    async def add_notes_table(username_id:int, text:str) -> None:
        """ЗАПРОС НА ДОБПАВЛЕНИЕ ТЕКСТА В БД"""

        try:
            async with connection.db_pool.acquire() as conn:
                query = """
                    INSERT INTO public.notes_tg_bot(user_id, note_text)
                    VALUES($1, $2)
                """
                await conn.execute(query, username_id, text)
                print('ЗАПРОС В БД УСПЕШНО ОТПРАВЛЕН ЗАМЕТКИ ОБНОВЛЕННЫ')

        except Exception as e:
            logging.error(f'ОШИБКА ПРИ ДОБАВЛЕНИЕ ЗАМЕТКИ {e}', exc_info=True)


    @staticmethod
    async def create_table():
        """Создание таблицы при включении бота"""

        try:
            async with connection.db_pool.acquire() as conn:
                query_user = """
                    CREATE TABLE IF NOT EXISTS public.user_tg_bot(
                        username_id BIGINT PRIMARY KEY,
                        notes_id VARCHAR(255) NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """

                query_notes = """
                    CREATE TABLE IF NOT EXISTS public.notes_tg_bot(
                        id SERIAL PRIMARY KEY,
                        user_id BIGINT NOT NULL,
                        note_text TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES public.user_tg_bot(username_id) ON DELETE CASCADE
                    );
                """

                query_notion = """
                    CREATE TABLE IF NOT EXISTS public.notion_tg_bot(
                        id SERIAL PRIMARY KEY,
                        user_id BIGINT NOT NULL,
                        note_id INTEGER NOT NULL,
                        remind_at TIMESTAMP NOT NULL,
                        
                        FOREIGN KEY (user_id) REFERENCES  public.user_tg_bot(username_id) ON DELETE CASCADE,
                        FOREIGN KEY (note_id) REFERENCES  public.notes_tg_bot(id) ON DELETE CASCADE
                    );
                """


                await conn.execute(query_user)
                print("ТАБЛИЦА ПОЛЬЗОВАТЕЛЕЙ УСПЕШНО СОЗДАНА ИЛИ УЖЕ ЕСТЬ")
                await conn.execute(query_notes)
                print("ТАБЛИЦА БЛОКТОНОВ УСПЕШНО СОЗДАНА ИЛИ УЖЕ ЕСТЬ")
                await conn.execute(query_notion)
                print("ТАБЛИЦА УВЕДОМЛЕНИЙ УСПЕШНО СОЗДАНА ИЛИ УЖЕ ЕСТЬ")


        except Exception as e:
            logging.error(f'ОШИБКА СОЗДАНИЯ ТАБЛИЦЫ {e}', exc_info=True)


    @staticmethod
    async def add_notes_id(username_id):
        """Добавление пользователя в таблицу при инициализации бота в первый раз"""

        try:
            async with connection.db_pool.acquire() as conn:
                query = """
                    INSERT INTO public.user_tg_bot(username_id)
                    VALUES($1)
                    ON CONFLICT (username_id) DO NOTHING;
                """

                await conn.execute(query, username_id, )
                print('ПОЛЬЗОВАТЕЛЬ ДОБАВЛЕН В БАЗУ ДАННЫХ ИЛИ УЖЕ ЕСТЬ')

        except Exception as e:
            logging.error(f'ОШИБКА ДОБАВЛЕНИЯ ПОЛЬЗОВАТЕЛЯ В ТАБЛИЦУ {e}', exc_info=True)


    @staticmethod
    async def get_notes(username_id):
        """ЗАПРОС НА ПРОЧТЕНИЕ ЗАМЕТКИ"""

        try:
            async with connection.db_pool.acquire() as conn:
                query = """
                    SELECT id, note_text
                    FROM public.notes_tg_bot  
                    WHERE user_id = $1
                    ORDER BY created_at;  
                """

                rows = await conn.fetch(query, username_id)
                return rows

        except Exception as e:
            logging.error(f'ОШИБКА ЗАПРОСА НА ПРОЧТЕНИЕ {e}', exc_info=True)


    @staticmethod
    async def get_single_note(note_id: int):
        """ """

        try:
            async with connection.db_pool.acquire() as conn:
                query = """
                    SELECT note_text
                    FROM public.notes_tg_bot  
                    WHERE id = $1;
                """
                row = await conn.fetchrow(query, note_id)
                if row: return row['note_text']


        except Exception as e:
            logging.error(f'ОШИБКА ОПЕРАЦИИ ПО ФИЛЬТАЦИИ id {e}', exc_info=True)


    @staticmethod
    async def set_notion_notes(user_id:int, note_id:int, remind_at):
        """Добавдение времени уведомления"""

        try:
            async with connection.db_pool.acquire() as conn:

                query = """
                    INSERT INTO public.notion_tg_bot(user_id, note_id, remind_at)
                    VALUES($1, $2, $3)
                """

                await conn.execute(query, user_id, note_id, remind_at)

        except Exception as e:
            logging.error(f'ОШИБКА ДОБАВЛЕНИЯ УВЕДОМЛЕНИЯ {e}', exc_info=True)


    @staticmethod
    async def get_active_reminders():

        try:
            async with connection.db_pool.acquire() as conn:
                query = """
                    SELECT public.notion_tg_bot.user_id, public.notes_tg_bot.note_text
                    FROM public.notion_tg_bot
                    INNER JOIN public.notes_tg_bot ON public.notion_tg_bot.note_id = public.notes_tg_bot.id
                    WHERE public.notion_tg_bot.remind_at <= NOW();
                """

                rows = await conn.fetch(query)

                query_delete = """
                    DELETE FROM public.notion_tg_bot WHERE remind_at <= NOW();
                """
                await conn.execute(query_delete)

                return rows
        except Exception as e:
            logging.error(f'ОШИБКА ОБРАБОТКИ ВРЕМЕНИ {e}', exc_info=True)


    @staticmethod
    async def get_future_reminders(user_id:int):
        try:
            async with connection.db_pool.acquire() as conn:
                query = """
                    SELECT public.notes_tg_bot.note_text, public.notion_tg_bot.remind_at
                    FROM public.notion_tg_bot
                    INNER JOIN public.notes_tg_bot ON public.notion_tg_bot.note_id = public.notes_tg_bot.id
                    WHERE public.notion_tg_bot.user_id = $1 AND public.notion_tg_bot.remind_at > NOW()
                    ORDER BY public.notion_tg_bot.remind_at;
                """
                rows = await conn.fetch(query, user_id)
                return rows
        except Exception as e:
            logging.error(f'ОШИБКА ПОЛУЧЕНИЯ БУДУЩИХ НАПОМИНАНИЙ {e}', exc_info=True)
            return []

