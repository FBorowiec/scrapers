from datetime import date, datetime
import re
from urllib.parse import urljoin
from urllib3.util import Retry
from requests.adapters import HTTPAdapter
from requests.sessions import Session
from string import ascii_letters
from typing import Optional, Dict
from time import sleep
from bs4 import BeautifulSoup
from tenacity import retry, wait_fixed
from pydantic import BaseModel
from cisei.names import get_names_list
from cisei.cisei_logger import LoggerDB


class PersonalInfo(BaseModel):
    idx: int
    surname: str
    full_name: str
    age: Optional[int] = None
    trip_date: Optional[date]
    registration_place: str
    url: str
    details: Optional[Dict]


class CiseiRequestHandler:
    URL = "http://www.ciseionline.it/portomondo/ricerca.asp"
    BASE_PERSON_URL = "http://www.ciseionline.it/portomondo/"
    NEXT_PAGE_URL = "http://www.ciseionline.it/portomondo/tabelle.asp?primo="
    MAX_RESULTS_PER_PAGE = 16

    def __init__(self) -> None:
        self.logger = LoggerDB()
        self.session = self._init_session()

    def _init_session(self) -> Session:
        session = Session()
        retries = Retry(connect=10, read=10, redirect=10)

        session.mount("http://", HTTPAdapter(max_retries=retries))
        session.mount("https://", HTTPAdapter(max_retries=retries))
        session.headers.update(
            {
                "User-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0"
            }
        )
        return session

    @retry(wait=wait_fixed(1))
    def get_first_page(self, surname: str) -> BeautifulSoup:
        custom_header = {
            "input_cognome": surname,
            "input_nome": "",
            "input_dest": "al",
        }
        r = self.session.post(self.URL, custom_header)
        r.raise_for_status()
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        return soup

    @retry(wait=wait_fixed(1))
    def get_next_page(self, page: int):
        cookie = self.session.cookies.get_dict()
        cookie_list = list(cookie.items())[0]
        cookie_str = f"{cookie_list[0]}={cookie_list[1]}"
        custom_header = {
            "Cookie": cookie_str,
            "Connection": "keep-alive",
        }
        url = self.NEXT_PAGE_URL + str(page)
        r = self.session.get(url, headers=custom_header)
        r.raise_for_status()
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        return soup

    @retry(wait=wait_fixed(1))
    def get_details_soup(self, details_url: str) -> BeautifulSoup:
        r = self.session.get(details_url)
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        return soup

    @staticmethod
    def remove_alphanumeric(arg: str) -> str:
        return "".join([c for c in arg if c in (ascii_letters)])

    def get_person_info(self, td_list, name):
        idx = td_list[0].text

        age = re.search(r"\d+", td_list[2].text)
        age = age.group(0) if age is not None else None

        full_name = re.findall(r"[A-Z]+", td_list[1].text)
        full_name = (
            " ".join(full_name).replace(name.upper() + " ", "").title()
            if full_name is not None
            else ""
        )

        trip_date = re.findall(r"\d{1,4}", td_list[3].text)
        trip_date = (
            datetime.strptime("-".join(trip_date), "%d-%m-%Y")
            if len(trip_date) != 0
            else None
        )

        registration_place = re.findall(r"\b[A-Z\w+]+", td_list[4].text)
        registration_place = (
            " ".join(registration_place) if registration_place is not None else ""
        )

        details = str(td_list[5].contents[1]).split('"')[1]

        person_info = PersonalInfo(
            idx=idx,
            surname=name,
            full_name=full_name,
            age=age,
            trip_date=trip_date,
            registration_place=registration_place,
            url=urljoin(self.BASE_PERSON_URL, details),
        )

        return person_info

    def get_person_details(self, person: PersonalInfo):
        soup = self.get_details_soup(person.url)
        tr_list = soup.find_all("td")
        details_dict = {}
        for tr in tr_list:
            raw_txt = re.sub(r"\\<[/]?[a-z]\\>", "", tr.text).splitlines()

            for line in raw_txt:
                try:
                    k, v = line.split(":")
                    key = k.strip()
                    value = v.strip()
                    if value not in ["", "nd", "ND", "n.d.", "N.D."]:
                        details_dict[key] = value
                except ValueError:
                    pass

        return details_dict

    def parse_page(self, name: str, soup: BeautifulSoup):
        tr_list = soup.find("div", {"class": "box"}).find("center").find_all("tr")
        for tr in tr_list:
            td_list = tr.find_all("td", {"class": "tdesito"})
            if len(td_list) != 0:
                person_info = self.get_person_info(td_list, name)
                person_details = self.get_person_details(person_info)
                person_info.details = person_details
                sleep(0.5)  # do not overload the server

                self.log_person_info(person_info)

    def next_page_exists(self, soup: BeautifulSoup) -> bool:
        matches = [
            str(x) for x in list(soup.find_all("a", href=re.compile(r".*tabelle.*")))
        ]
        return "Successivi" in f"{matches}"

    def log_person_info(self, person_info: PersonalInfo) -> None:
        print(person_info, "\n")
        self.logger.add_person_info(person_info)


def scrap_cisei():
    crh = CiseiRequestHandler()
    names = get_names_list()

    for name in names:
        soup = crh.get_first_page(name)
        crh.parse_page(name, soup)

        next_page = crh.next_page_exists(soup)
        i = crh.MAX_RESULTS_PER_PAGE
        while next_page:
            soup = crh.get_next_page(page=i)
            crh.parse_page(name, soup)
            next_page = crh.next_page_exists(soup)
            i += crh.MAX_RESULTS_PER_PAGE

        sleep(0.5)  # do not overload the server
