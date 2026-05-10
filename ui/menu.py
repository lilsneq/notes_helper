from aiogram import Router
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup


router = Router()


def get_main_menu():
    builder = ReplyKeyboardBuilder()

    builder.button(text='🗒️Добавить заметку')
    builder.button(text='🗒️Мои заметки')
    builder.button(text='⚒️Настройки')

    builder.adjust(2, 1)

    return builder.as_markup(resize_keyboard=True)
