
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database.requests import CreateRequest

router = Router()



@router.message(F.text.contains("Настройки"))
async def show_settings(message: Message):
    await message.answer('Раздел настроек находится в разработке')
