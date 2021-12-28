from aiogram.dispatcher.storage import FSMContext
from aiogram.types import Message
from aiogram.dispatcher.filters import Command
# from aiohttp.helpers import parse_http_date

from loader import dp
from keyboards.default import menu
from data.config import db


@dp.message_handler(Command('start'))
async def show_menu(message: Message) -> None:
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
    await message.answer("Выбери действие", reply_markup=menu)


@dp.message_handler(text="🔙Главное меню", state="*")
async def back_to_menu(message: Message, state: FSMContext) -> None:
    await message.answer("Выбери действие", reply_markup=menu)
    await state.finish()
