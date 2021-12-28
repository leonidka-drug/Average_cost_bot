from aiogram.types import Message
from utils.google_sheets.calculations import calculate_cost

from data.conf import GH_data
from loader import dp

@dp.message_handler(text="📈Cредний чек номера")
async def show_average_cost(message: Message) -> None:
    params = await calculate_cost(GH_data['sofia'])
    full_info = 'За {} дней средний чек: {:.2f},\nНедостача: {:.2f},'.format(
        params["days_gone"],
        params["sold_average"],
        params["shortage"],
    )
    full_info += '\nСредний чек за номер на следующие дни: {:.2f}'.format(
        params["next_days_cost"])
    full_info += '\nМинимальна сумма прихода на следующие дни: {:.2f}'.format(
        params["next_days_cost"] * params["number_of_rooms"])

    await message.answer(text=full_info)
