from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from datetime import datetime, timedelta

from aiogram.fsm.state import State, StatesGroup

from database.requests import CreateRequest
from ui.menu import back_to_main_menu




router = Router()




@router.callback_query(F.data == 'menu_show_notes')
async def show_note(callback: CallbackQuery) -> None:
    builder = InlineKeyboardBuilder()

    user_id = callback.from_user.id
    notes = await CreateRequest.get_notes(username_id=user_id)

    if not notes:
        await callback.message.edit_text(
            'У вас пока нет сохраненных заметок ',
            reply_markup=back_to_main_menu()
        )
        await callback.answer()
        return


    text = "📋 Выберите заметку из списка:"

    for index, note in enumerate(notes, 1):
        builder.button(
            text=f"{index}. {note['note_text'][:20]}...",
            callback_data=f'view_note_{note["id"]}'
        )
    builder.button(text='🔙 Назад', callback_data='to_main_menu')
    builder.adjust(1)

    await callback.message.edit_text(text=text, reply_markup=builder.as_markup())
    await callback.answer()



@router.callback_query(F.data.startswith('view_note_'))
async def show_single_note(callback: CallbackQuery) -> None:
    note_id = int(callback.data.split('_')[-1])
    note_text = await CreateRequest.get_single_note(note_id)

    builder = InlineKeyboardBuilder()

    builder.button(text='⏰ Напомнить', callback_data=f'set_remind_{note_id}')
    builder.button(text='🔙 К списку заметок', callback_data=f'menu_show_notes')

    builder.adjust(1)

    await callback.message.edit_text(text=note_text, reply_markup=builder.as_markup())

    await callback.answer()




@router.callback_query(F.data.startswith('set_remind_'))
async def set_remind(callback: CallbackQuery) -> None:
    note_id = int(callback.data.split('_')[-1])

    builder = InlineKeyboardBuilder()

    builder.button(text="⏱️ За 1 час", callback_data=f"time_1h_{note_id}")
    builder.button(text="🕐 За 3 часа", callback_data=f"time_3h_{note_id}")
    builder.button(text="📅 За 12 часов", callback_data=f"time_12h_{note_id}")
    builder.button(text="🔙 Назад к заметке", callback_data=f"view_note_{note_id}")

    builder.adjust(1)

    await callback.message.edit_text(
        text="⏰ Выберите, через какое время вам напомнить об этой заметке:",
        reply_markup=builder.as_markup()
    )
    await callback.answer()



@router.callback_query(F.data.startswith('time_'))
async def set_time(callback: CallbackQuery) -> None:

    note_id = int(callback.data.split('_')[-1])

    current_time = datetime.now()

    if "1h" in callback.data:
        remind_time = current_time + timedelta(hours=1)
    elif "3h" in callback.data:
        remind_time = current_time + timedelta(hours=3)
    elif "12h" in callback.data:
        remind_time = current_time + timedelta(hours=12)

    await CreateRequest.set_notion_notes(
        user_id=callback.from_user.id,
        note_id=note_id,
        remind_at=remind_time
    )

    await callback.message.edit_text(
        text=f"✅ Напоминание успешно установлено на {remind_time.strftime('%H:%M')}",
        reply_markup=back_to_main_menu()
    )
    await callback.answer()




