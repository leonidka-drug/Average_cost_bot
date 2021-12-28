from utils.booking_scrapping.scrapper import Scrapper


def prepare_data(url: str) -> str:
    scr = Scrapper(url)
    scr.download_html()
    hotels_data = scr.parse()
    info = f'Средний чек {hotels_data[1]} отелей: {hotels_data[0]:.1f}'
    for hotel in hotels_data[2]:
        info += f'\n<a href="{hotel[3]}">{hotel[0].title()}</a> имеет среднюю стоимость {hotel[1]} и {hotel[2]}'
    return info
