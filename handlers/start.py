from aiogram import Router, html
from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram.filters import CommandStart
from ui.menu import get_main_menu
from database.requests import CreateRequest


router = Router()


@router.message(CommandStart())
async def command_start_handlers(message: Message) -> None:
    user_id = message.from_user.id
    await CreateRequest.add_notes_id(user_id)

    await message.answer(
        f'Привет, {html.bold(message.from_user.full_name)}! Я твой личный менеджер заметок. \n\n'
        f'Ипользуй меню ниже для работы со мной',
        reply_markup=get_main_menu(),
    )
