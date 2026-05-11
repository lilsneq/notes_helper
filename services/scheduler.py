import logging
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database.requests import CreateRequest






async def check_reminders(bot: Bot):
    # Вызываем ваш созданный метод слияния таблиц
    reminders = await CreateRequest.get_active_reminders()
    if reminders:
        for reminder in reminders:
            try:
                # Отправляем текст заметки пользователю по его ID
                await bot.send_message(
                    chat_id=reminder['user_id'],
                    text=f"⏰ Напоминание об одной из ваших заметок:\n\n{reminder['note_text']}"
                )
            except Exception as e:
                logging.error(f"Не удалось отправить уведомление: {e}")

    print("НАПОМИНАНИЕ ОТПРАВЛЕННО")


def setup_scheduler(bot: Bot) -> None:
    """Инициализация и запуск фонового будильника"""
    scheduler = AsyncIOScheduler()
    # Проверка базы данных каждую минуту
    scheduler.add_job(check_reminders, "interval", minutes=1, args=[bot])
    scheduler.start()