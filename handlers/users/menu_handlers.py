from aiogram.types import Message
from aiogram.dispatcher.filters import Command

from loader import dp
from keyboards.default import menu
from utils.google_sheets_data.calculations import calculate_cost
from data.conf import GH_data

@dp.message_handler(Command('menu'))
async def show_menu(message: Message):
    await message.answer("Выбери действие",reply_markup=menu)


@dp.message_handler(text="Посмотреть средний чек номера")
async def show_avarage_cost(message: Message):
    params = await calculate_cost(GH_data['sofia'])
    full_info = '\n За {} дней средний чек: {:.2f},\n Недостача: {:.2f},'.format(
        days_gone,
        sold_avarege,
        shortage,
    )

    
# print('\n За {} дней средний чек: {:.2f},\n Недостача: {:.2f},'.format(
#         days_gone,
#         sold_avarege,
#         shortage,
#     ))
#     print(' Средний чек за номер на следующие дни: {:.2f}'.format(next_days_cost))
#     print(' Минимальна сумма прихода на следующие дни: {:.2f}'.format(next_days_cost * data['ROOMS_NUMBER']))
#     print('---------------------------------------------------------')