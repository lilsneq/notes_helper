# МОДУЛЬ ПОДКЛЮЧЕНИЯ К БД


# ИМПОРТЫ
import os
import sys
import asyncpg
from dotenv import load_dotenv



load_dotenv()

db_pool = None

async def conn_bd_pool():
    """Инициализирует пул подключений к PostgreSQL"""
    global db_pool

    if db_pool is not None:
        return db_pool

    DATABASE_URL = os.getenv('DATABASE_URL')
    if not DATABASE_URL:
        sys.exit('ОШИБКА: Ключ переменной не найден в файле .env')
        return False

    db_pool = await asyncpg.create_pool(
        DATABASE_URL,
        min_size=5,
        max_size=10
    )

    return db_pool


async def close_bd_pool():
    """ЗАКРЫТИЕ ПУЛА"""
    global db_pool
    if db_pool:
        await db_pool.close()



