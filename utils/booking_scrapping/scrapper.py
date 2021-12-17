import requests
from bs4 import BeautifulSoup
from statistics import mean
from typing import Union
from pprint import pprint


class Scrapper:
    def __init__(self, url: str) -> None:
        self.headers = {
            "Accept" : "*/*",
            "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0"
        }

        try:
            req = requests.get(url, headers=self.headers)
        except Exception as e:
            print(e)
            self.src = 0
        else:
            self.src = req.text

        self.hotel_cardboard_class: str = "_fe1927d9e _0811a1b54 _a8a1be610 _022ee35ec b9c27d6646 fb3c4512b4 fc21746a73"

    def check_and_prepare(self) -> None:
        if self.src != 0:
            self.soup = BeautifulSoup(self.src, "lxml")
            self.ten_offers = self.soup.find_all(class_=self.hotel_cardboard_class)[0:10]

    def parse(self, 
            hotel_room_cost_class: str = "fde444d7ef _e885fdc12",
            hotel_name_class: str = "fde444d7ef _c445487e2",
            hotel_link_class: str = "fb01724e5b",
            hotel_comments_class: str = "_4abc4c3d5 _1e6021d2f _6e869d6e0") -> Union[int, float]:
        names = list()
        urls = list()
        costs = list()
        comments = list()

        for item in self.ten_offers:
            names.append(item.find(class_=hotel_name_class).text)
            urls.append(item.find("a",class_=hotel_link_class).get("href"))
            costs.append(int(item.find(
                "span",
                class_=hotel_room_cost_class
            ).text[0:-5].replace(" ", "")))
            comments.append(item.find(class_=hotel_comments_class).text)

        average = mean(costs)

        return average, len(costs), tuple(zip(names, costs, comments, urls))


def main():
    url = "https://www.booking.com/searchresults.ru.html?label=gen173nr-1DCAsowgFCB3Utc29mLWlIIVgEaMIBiAEBmAEhuAEYyAEM2AED6AEB-AEDiAIBqAIEuALTqYSNBsACAdICJGVmZDg5MTEwLTRhNmUtNDVjYi05ZTBjLTljNGQ3NGQ3MjkxMdgCBOACAQ&sid=9bd2289d5de1707f8ee8ac0660d6c1fe&aid=304142&src=searchresults&error_url=https%3A%2F%2Fwww.booking.com%2Fsearchresults.ru.html%3Flabel%3Dgen173nr-1DCAsowgFCB3Utc29mLWlIIVgEaMIBiAEBmAEhuAEYyAEM2AED6AEB-AEDiAIBqAIEuALTqYSNBsACAdICJGVmZDg5MTEwLTRhNmUtNDVjYi05ZTBjLTljNGQ3NGQ3MjkxMdgCBOACAQ%3Bsid%3D9bd2289d5de1707f8ee8ac0660d6c1fe%3Btmpl%3Dsearchresults%3Bcheckin_month%3D12%3Bcheckin_monthday%3D30%3Bcheckin_year%3D2021%3Bcheckout_month%3D12%3Bcheckout_monthday%3D31%3Bcheckout_year%3D2021%3Bcity%3D-2874290%3Bclass_interval%3D1%3Bdest_id%3D-2874290%3Bdest_type%3Dcity%3Bdtdisc%3D0%3Bfrom_sf%3D1%3Bgroup_adults%3D2%3Bgroup_children%3D0%3Bhighlighted_hotels%3D5509798%3Bhp_sbox%3D1%3Binac%3D0%3Bindex_postcard%3D0%3Blabel_click%3Dundef%3Bno_rooms%3D1%3Boffset%3D0%3Bpostcard%3D0%3Broom1%3DA%252CA%3Bsb_price_type%3Dtotal%3Bshw_aparth%3D1%3Bslp_r_match%3D0%3Bsrc%3Dhotel%3Bsrc_elem%3Dsb%3Bsrpvid%3D7f8d78b1580b017d%3Bss%3D%25D0%2590%25D0%25B4%25D0%25BB%25D0%25B5%25D1%2580%3Bss_all%3D0%3Bssb%3Dempty%3Bsshis%3D0%3Bssne%3D%25D0%2590%25D0%25B4%25D0%25BB%25D0%25B5%25D1%2580%3Bssne_untouched%3D%25D0%2590%25D0%25B4%25D0%25BB%25D0%25B5%25D1%2580%3Btop_ufis%3D1%26%3B&highlighted_hotels=5509798&ss=%D0%90%D0%B4%D0%BB%D0%B5%D1%80&is_ski_area=0&ssne=%D0%90%D0%B4%D0%BB%D0%B5%D1%80&ssne_untouched=%D0%90%D0%B4%D0%BB%D0%B5%D1%80&city=-2874290&checkin_year=2021&checkin_month=12&checkin_monthday=30&checkout_year=2022&checkout_month=1&checkout_monthday=1&group_adults=2&group_children=0&no_rooms=1&from_sf=1&nflt=pri%3D1%3Bht_id%3D216%3Breview_score%3D90%3Bdistance%3D1000"
    scr = Scrapper(url)
    scr.check_and_prepare()
    pprint(scr.parse())


if __name__ == "__main__":
    main()
