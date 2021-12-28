from aiogram.dispatcher.storage import FSMContext
from aiogram.types import Message
from aiogram.dispatcher.filters import Command
from aiohttp.helpers import parse_http_date

from loader import dp
from keyboards.default import menu, back_to_menu, analysis_menu
from data.conf import GH_data
from data.config import db, BASE_DIR
from utils.google_sheets.calculations import calculate_cost
from utils.booking_scrapping.scrapper import Scrapper
from states.first_adding_url import FirstURL

changing_url_info = 'Чтобы проанализировать конкурентов, нужно отправить'
changing_url_info += ' сюда URL booking.com сообщением. Для этого' 
changing_url_info += ' войдите на сайт booking.com, выберите все'
changing_url_info += ' соответсвующие поиску ваших конкурентов фильтры,'
changing_url_info += ' которые можно видеть на фото в жёлтом окне'
changing_url_info += ' "Найти" и под ним, и после загрузки страницы'
changing_url_info += ' выделите весь URL-адрес как показано на фото,'
changing_url_info += ' скопируйте и отправьте его сюда.' 


def prepare_data(url: str) -> str:
    scr = Scrapper(url)
    scr.download_html()
    hotels_data = scr.parse()
    info = f'Средний чек {hotels_data[1]} отелей: {hotels_data[0]:.1f}'
    for hotel in hotels_data[2]:
        info += f'\n<a href="{hotel[3]}">{hotel[0].title()}</a> имеет среднюю стоимость {hotel[1]} и {hotel[2]}'
    return info


@dp.message_handler(Command('start'))
async def show_menu(message: Message) -> None:
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
    await message.answer("Выбери действие", reply_markup=menu)


@dp.message_handler(text="🔙Главное меню", state="*")
async def show_menu(message: Message, state: FSMContext) -> None:
    await message.answer("Выбери действие", reply_markup=menu)
    await state.finish()


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


@dp.message_handler(text="♻️Обновить URL")
async def update_url(message: Message) -> None:
    photo_path = BASE_DIR / "data/booking_screen.png"
    with photo_path.open("rb") as photo:
            await message.answer_photo(photo=photo,
                                       caption=changing_url_info,
                                       reply_markup=back_to_menu)
        
    await FirstURL.first()


@dp.message_handler(text="🏨Проанализировать конкурентов")
async def analyse_booking(message: Message, state: FSMContext) -> None:
    url = db.get_entry("users", "tg_id", message.from_user.id)[2]
    if url != None:
        info_with_URL = 'Чтобы проанализировать конкурентов,'
        info_with_URL += ' можно добавить новый URL или использовать'
        info_with_URL += ' ранее добавленный'
        await message.answer(text=info_with_URL, reply_markup=analysis_menu)
        await state.update_data({"url": url})
    else:
        await update_url(message)


@dp.message_handler(text="✅Использовать старый URL")
async def analyse_exisiting_url(message: Message, state: FSMContext):
    data = await state.get_data()
    url = data.get("url")
    info = prepare_data(url)

    await message.answer(text=info, reply_markup=menu)
    await state.finish()


@dp.message_handler(state=FirstURL.sending_URL)
async def take_url(message: Message, state: FSMContext) -> None:
    url = message.text
    db.update_user_url(message.from_user.id, url)
    info = prepare_data(url)

    await message.answer(text=info, reply_markup=menu)
    await state.finish()