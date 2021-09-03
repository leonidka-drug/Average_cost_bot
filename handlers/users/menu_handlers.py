from aiogram.types import Message
from aiogram.dispatcher.filters import Command

from loader import dp
from keyboards.default import menu

@dp.message_handler(Command('menu'))
async def show_menu(message: Message):
    await message.answer("Выбери действие",reply_markup=menu)