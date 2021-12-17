from aiogram.types import Message
from aiogram.dispatcher.filters import Command

from loader import dp
from keyboards.default import menu
from data.conf import GH_data
from data.config import DATA_BASE_FILE
from utils.db_api.sqlite import Database
from utils.google_sheets.calculations import calculate_cost
from utils.booking_scrapping.scrapper import Scrapper

db = Database(DATA_BASE_FILE)


@dp.message_handler(Command('start'))
async def show_menu(message: Message) -> None:
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
    await message.answer("Выбери действие", reply_markup=menu)


@dp.message_handler(text="Посмотреть средний чек номера")
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


@dp.message_handler(text="Проанализировать канкурентов")
async def analyse_booking(message: Message) -> None:
    url = "https://www.booking.com/searchresults.ru.html?label=gen173nr-1DCAsowgFCB3Utc29mLWlIIVgEaMIBiAEBmAEhuAEYyAEM2AED6AEB-AEDiAIBqAIEuALTqYSNBsACAdICJGVmZDg5MTEwLTRhNmUtNDVjYi05ZTBjLTljNGQ3NGQ3MjkxMdgCBOACAQ&sid=9bd2289d5de1707f8ee8ac0660d6c1fe&aid=304142&src=searchresults&error_url=https%3A%2F%2Fwww.booking.com%2Fsearchresults.ru.html%3Flabel%3Dgen173nr-1DCAsowgFCB3Utc29mLWlIIVgEaMIBiAEBmAEhuAEYyAEM2AED6AEB-AEDiAIBqAIEuALTqYSNBsACAdICJGVmZDg5MTEwLTRhNmUtNDVjYi05ZTBjLTljNGQ3NGQ3MjkxMdgCBOACAQ%3Bsid%3D9bd2289d5de1707f8ee8ac0660d6c1fe%3Btmpl%3Dsearchresults%3Bcheckin_month%3D12%3Bcheckin_monthday%3D30%3Bcheckin_year%3D2021%3Bcheckout_month%3D12%3Bcheckout_monthday%3D31%3Bcheckout_year%3D2021%3Bcity%3D-2874290%3Bclass_interval%3D1%3Bdest_id%3D-2874290%3Bdest_type%3Dcity%3Bdtdisc%3D0%3Bfrom_sf%3D1%3Bgroup_adults%3D2%3Bgroup_children%3D0%3Bhighlighted_hotels%3D5509798%3Bhp_sbox%3D1%3Binac%3D0%3Bindex_postcard%3D0%3Blabel_click%3Dundef%3Bno_rooms%3D1%3Boffset%3D0%3Bpostcard%3D0%3Broom1%3DA%252CA%3Bsb_price_type%3Dtotal%3Bshw_aparth%3D1%3Bslp_r_match%3D0%3Bsrc%3Dhotel%3Bsrc_elem%3Dsb%3Bsrpvid%3D7f8d78b1580b017d%3Bss%3D%25D0%2590%25D0%25B4%25D0%25BB%25D0%25B5%25D1%2580%3Bss_all%3D0%3Bssb%3Dempty%3Bsshis%3D0%3Bssne%3D%25D0%2590%25D0%25B4%25D0%25BB%25D0%25B5%25D1%2580%3Bssne_untouched%3D%25D0%2590%25D0%25B4%25D0%25BB%25D0%25B5%25D1%2580%3Btop_ufis%3D1%26%3B&highlighted_hotels=5509798&ss=%D0%90%D0%B4%D0%BB%D0%B5%D1%80&is_ski_area=0&ssne=%D0%90%D0%B4%D0%BB%D0%B5%D1%80&ssne_untouched=%D0%90%D0%B4%D0%BB%D0%B5%D1%80&city=-2874290&checkin_year=2021&checkin_month=12&checkin_monthday=30&checkout_year=2022&checkout_month=1&checkout_monthday=1&group_adults=2&group_children=0&no_rooms=1&from_sf=1&nflt=pri%3D1%3Bht_id%3D216%3Breview_score%3D90%3Bdistance%3D1000"
    scr = Scrapper(url)
    scr.check_and_prepare()
    hotels_data = scr.parse()
    info = f'Средний чек {hotels_data[1]} отелей: {hotels_data[0]:.1f}'
    for hotel in hotels_data[2]:
        info += f'\n<a href="{hotel[3]}">{hotel[0].title()}</a> имеет среднюю стоимость {hotel[1]} и {hotel[2]}'
    await message.answer(text=info)