# main файл для запуска бота
import asyncio

# Импорты
import logging
import sys
import os

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from handlers.start import router as start_router
from handlers.create_notes import router as create_notes_router
from handlers.show_notes import router as show_notes_router
from handlers.settings_notes import router as settings_notes_router

from database.connection import conn_bd_pool, close_bd_pool
from database.requests import CreateRequest



load_dotenv()


async def main() -> None:
    TOKEN = os.getenv("TOKENTG")
    if not TOKEN:
        sys.exit("TOKENTG НЕ НАЙДЕН В ФАЙЛЕ .env")

    dp = Dispatcher()

    if not await conn_bd_pool():
        sys.exit('ОШИБКА: Ключ переменной не найден в файле .env')

    print('ПУЛ ПОДКЛЮЧЕНИЙ К PostgreSQL ИНИЦИАЛИЗИРОВАН')
    await CreateRequest.create_table()


    dp.include_routers(
    start_router,show_notes_router,
                create_notes_router, settings_notes_router)

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    try:
        print('Бот успешно запущен и готов к работе')
        await dp.start_polling(bot)
    finally:
        await close_bd_pool()
        print('Бот успешно завершил работу')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    asyncio.run(main())




