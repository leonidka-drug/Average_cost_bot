from aiogram.types import Message
from aiogram.dispatcher.filters import Command

from loader import dp
from keyboards.default import menu
from utils.google_sheets_data.calculations import calculate_cost
from data.conf import GH_data


@dp.message_handler(Command('menu'))
async def show_menu(message: Message):
    await message.answer("Выбери действие", reply_markup=menu)


@dp.message_handler(text="Посмотреть средний чек номера")
async def show_average_cost(message: Message):
    params = await calculate_cost(GH_data['sofia'])
    full_info = 'За {} дней средний чек: {:.2f},\n Недостача: {:.2f},'.format(
        params["days_gone"],
        params["sold_average"],
        params["shortage"],
    )
    full_info += '\n Средний чек за номер на следующие дни: {:.2f}'.format(
        params["next_days_cost"])
    full_info += '\n Минимальна сумма прихода на следующие дни: {:.2f}'.format(
        params["next_days_cost"] * params["number_of_rooms"])

    await message.answer(text=full_info)
