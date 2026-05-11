from aiogram import Router, html, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import CommandStart
from ui.menu import get_main_menu
from database.requests import CreateRequest
from ui.menu import get_main_menu, back_to_main_menu


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


@router.callback_query(F.data == 'menu_settings')
async def process_settings_click(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        text="⚒️ Настройки блокнота:\n\nЗдесь вы сможете управлять структурой ваших записей.",
        reply_markup=back_to_main_menu()
    )
    await callback.answer()


@router.callback_query(F.data == 'to_main_menu')
async def process_back_click(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        text='Используйте меню ниже для работы со мной',
        reply_markup=get_main_menu()
    )
    await callback.answer()


@router.callback_query(F.data == 'menu_notion')
async def show_all_reminders(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    reminders = await CreateRequest.get_future_reminders(user_id)
    if not reminders:
        await callback.message.edit_text(text='У вас пока нет активных напоминаний', reply_markup=back_to_main_menu())
        await callback.answer()
        return

    text = "🔔 Ваши активные напоминания:\n\n"

    for index, r in enumerate(reminders, 1):
        time_str = r['remind_at'].strftime('%H:%M (%d.%m)')
        text += f"{index}. [{time_str}] {r['note_text'][:20]}...\n"

    await callback.message.edit_text(text=text, reply_markup=back_to_main_menu())
    await callback.answer()













