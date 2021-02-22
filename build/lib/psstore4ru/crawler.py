import requests
import uuid
import re
import json
import yaml
from .utils import get_async_soup
from .variables import GAME_SELECTORS, EXTERNAL
from bs4 import BeautifulSoup
import asyncio
from aiohttp import ClientSession
from aiohttp import TCPConnector
from .variables import HEADERS


class PS4Game:
    def __init__(self, url: str = None, region_code: str = None, soup=None):
        """
        :param url: https://store.playstation.com/ru-ru/product/EP0002-CUSA23470_00-CB4STANDARD00001
        :param region_code: EP0002-CUSA23470_00-CB4STANDARD00001
        """
        self.url = url
        self.region_code = region_code
        self.soup = soup
        self.specs = []

    def __get_title(self):
        try:
            title = self.soup.find("h1", GAME_SELECTORS["title"]).text
        except AttributeError:
            return ""
        else:
            return title

    def __get_region_code(self):
        if self.region_code:
            return self.region_code
        else:
            return re.sub(pattern=r".*product/", string=self.url, repl="")

    def __get_publisher(self):
        try:
            publisher = self.soup.find("div", GAME_SELECTORS["publisher"]).text
        except AttributeError:
            return ""
        else:
            return "" if '\n' in publisher else publisher

    def __get_category(self):
        return "Предзаказ" if self.__get_preorder() else "Обычный"

    def __get_release_date(self):
        try:
            return self.soup.find("dd", GAME_SELECTORS["release"]).text
        except AttributeError:
            return ""

    def __get_voice(self) -> list:
        try:
            voices = self.soup.find("dd", GAME_SELECTORS["voice"]).text
        except AttributeError:
            return []
        else:
            return [
                voice.lstrip() for voice in voices.split(',')
            ]

    def __get_subtitles(self) -> list:
        try:
            subtitles = self.soup.find("dd", GAME_SELECTORS["subtitles"]).text
        except AttributeError:
            return []
        else:
            return [
                subtitle.lstrip() for subtitle in subtitles.split(',')
            ]

    def __get_genres(self) -> list:
        try:
            genres = self.soup.find("dd", GAME_SELECTORS["genres"]).text
        except AttributeError:
            return []
        else:
            return [
                genre.lstrip() for genre in genres.split(',')
            ]

    def __get_platforms(self):
        try:
            return self.soup.find("dd", GAME_SELECTORS["platforms"]).text
        except AttributeError:
            return ""

    def __get_rating(self):
        try:
            return self.soup.find("img", GAME_SELECTORS["rating"])['alt']
        except AttributeError:
            return ""
        except TypeError:
            return ""

    def __get_in_game_purchases(self) -> bool:
        match = self.soup.find("span", GAME_SELECTORS["in_game_purchases"])

        return True if match else False

    def __get_online_gaming(self) -> bool:
        match = self.soup.find("span", GAME_SELECTORS["online_gaming"])

        return True if (match or self.__get_ps_plus_required()) else False

    def __get_ps_plus_required(self) -> bool:
        match = self.soup.find("span", GAME_SELECTORS["ps_plus_required"])

        return True if match else False

    def __get_ps_pro_tuned(self) -> bool:
        match = self.soup.find("span", GAME_SELECTORS["ps_pro_tuned"])

        return True if match else False

    def __get_ps_vr_support(self) -> bool:
        match = self.soup.find("span", GAME_SELECTORS["ps_vr_support"])

        return True if match else False

    def __get_preorder(self) -> bool:
        match = self.soup.find("button", GAME_SELECTORS["preorder"])

        return True if match else False

    def __get_cover_picture(self):
        try:
            cover_picture_url = self.soup.select(GAME_SELECTORS["cover_picture"])[0]['src']
        except AttributeError:
            return ""
        except IndexError:
            return ""
        else:
            return re.sub(pattern=r'\?.*', repl='', string=cover_picture_url)

    def __get_price(self):
        try:
            return int(re.sub(r'\D', '', self.soup.find("span", GAME_SELECTORS["price"]).text))
        except AttributeError:
            return 0
        except ValueError:
            return 0

    def __get_original_price(self):
        try:
            return int(re.sub(r'\D', '', self.soup.find("span", GAME_SELECTORS["original_price"]).text))
        except AttributeError:
            return 0

    def __get_ps_plus(self):
        try:
            return self.soup.find("div", GAME_SELECTORS["psplus discount"]).text
        except AttributeError:
            return ""

    def __get_description(self):
        try:
            return self.soup.find("p", GAME_SELECTORS["description"]).text
        except AttributeError:
            return ""

    def __load_page(self):
        response = requests.get(self.url.encode("utf-8").decode("utf-8-sig"))
        html = response.content
        self.soup = BeautifulSoup(html, features='html.parser')

    def __make_payload(self):
        """
        Returns a dict of game specs
        """
        if not self.soup:
            self.__load_page()

        return {
            "title": self.__get_title(),
            "uri": self.url,
            "region_code": self.__get_region_code(),
            "cover": self.__get_cover_picture(),
            "details": {
                "about": {
                    "description": self.__get_description(),
                    "genres": self.__get_genres(),
                    "ages": self.__get_rating(),
                    "publisher": self.__get_publisher(),
                    "release_date": self.__get_release_date(),
                    "category": self.__get_category(),
                },
                "platforms": {
                    "supported": self.__get_platforms(),
                    "ps4pro": self.__get_ps_pro_tuned()
                },
                "pricing": {
                    "final_price": self.__get_price(),
                    "original_price": self.__get_original_price()
                },
                "language": {
                    "audio": self.__get_voice(),
                    "subtitles": self.__get_subtitles()
                },
                "misc": {
                    "in_game_purchases": self.__get_in_game_purchases(),
                    "online": self.__get_online_gaming(),
                    "ps_plus_required": self.__get_ps_plus_required(),
                    "ps_vr_support": self.__get_ps_vr_support()
                }
            }
        }

    def as_dict(self):
        """
        Return game info as python
        <dict> object
        """
        return self.__make_payload()

    def as_yaml(self):
        """
        Return game info as YAML
        """
        return yaml.dump([self.__make_payload()], allow_unicode=True)

    def as_xml(self):
        """
        Return game info as XML
        """
        pass

    def as_json(self):
        """
        Return game info as JSON
        """
        return json.dumps(self.__make_payload(), ensure_ascii=False, indent=4)


async def launch():
    tasks = []

    f = open("links.json", "r")
    content = f.read()
    js = dict(json.loads(content))
    links = list(js.values())[:200]

    async with ClientSession(headers=HEADERS, connector=TCPConnector(ssl=False)) as session:
        for link in links:
            task = asyncio.ensure_future(
                get_async_soup(
                        session=session, url=f"{EXTERNAL['product']}{link}"
                )
            )
            tasks.append(task)

        soups = await asyncio.gather(*tasks)

        f = open("games.json", "a")
        f.write('{')

        for index, soup in enumerate(soups):
            string = PS4Game(url=soup[1], soup=soup[0]).as_json()
            f.write(f'"{str(uuid.uuid4())}": {string},')
        f.write('}')

loop = asyncio.get_event_loop()
future = asyncio.ensure_future(launch())
loop.run_until_complete(future)
