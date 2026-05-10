# handlers/create_notes.py — модуль для кнопки создания записи

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database.requests import CreateRequest
from ui.menu import back_to_main_menu


router = Router()

class NoteForm(StatesGroup):
    waiting_for_note = State()


@router.callback_query(F.data == 'menu_add_not')
async def add_note_start(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(NoteForm.waiting_for_note)
    await callback.message.edit_text(
        text='Напишите свою заметку',
        reply_markup=back_to_main_menu()
    )
    await callback.answer()

@router.message(NoteForm.waiting_for_note)
async def add_note_save(message: Message, state: FSMContext) -> None:
    user_text = message.text
    user_id = message.from_user.id

    await CreateRequest.add_notes_table(username_id=user_id, text=user_text)

    await message.answer("Заметка успешно сохранена")
    await state.clear()
