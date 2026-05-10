from aiogram import Router, F
from aiogram.types import Message

from aiogram.fsm.state import State, StatesGroup


from database.requests import CreateRequest

router = Router()


@router.message(F.text.contains("Мои заметки"))
async def show_note(message: Message):
    user_id = message.from_user.id
    notes = await CreateRequest.get_notes(username_id=user_id)

    if not notes:
        await message.answer('У вас пока нет сохраненных заметок ')
        return

    text = "📋 Ваши сохраненные заметки:\n\n"

    for index, note in enumerate(notes, 1):
        text += f"{index}. {note}\n"
    await message.answer(text)


