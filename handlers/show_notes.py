from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup

from aiogram.fsm.state import State, StatesGroup


from database.requests import CreateRequest
from ui.menu import back_to_main_menu

router = Router()


@router.callback_query(F.data == 'menu_show_notes')
async def show_note(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    notes = await CreateRequest.get_notes(username_id=user_id)

    if not notes:
        await callback.message.edit_text(
            'У вас пока нет сохраненных заметок ',
            reply_markup=back_to_main_menu()
        )
        await callback.answer()
        return

    text = "📋 Ваши сохраненные заметки:\n\n"

    for index, note in enumerate(notes, 1):
        text += f"{index}. {note}\n"
    await callback.message.edit_text(text=text, reply_markup=back_to_main_menu())
    await callback.answer()


