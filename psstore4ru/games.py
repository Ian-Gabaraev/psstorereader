import requests
import re
import json
import yaml
from .variables import SPECS, GAME_SELECTORS, EXTERNAL
from bs4 import BeautifulSoup


class PS4Game:
    def __init__(self, url: str = None, alias: str = None):
        """
        :param url: https://store.playstation.com/ru-ru/product/EP0002-CUSA23470_00-CB4STANDARD00001
        :param alias: EP0002-CUSA23470_00-CB4STANDARD00001
        """
        self.url = url if url else f"{EXTERNAL['product']}{alias}"
        self.languages = SPECS["languages"]
        self.genres = SPECS["genres"]
        self.soup = None
        self.specs = []

    def __get_title(self):
        return self.soup.find("h1", GAME_SELECTORS["title"]).text

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

    def __get_voice(self):
        try:
            return self.soup.find("dd", GAME_SELECTORS["voice"]).text
        except AttributeError:
            return ""

    def __get_subtitles(self):
        try:
            return self.soup.find("dd", GAME_SELECTORS["subtitles"]).text
        except AttributeError:
            return ""

    def __get_genres(self):
        try:
            return self.soup.find("dd", GAME_SELECTORS["genres"]).text
        except AttributeError:
            return ""

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

    def __get_in_game_purchases(self):
        match = self.soup.find("span", GAME_SELECTORS["in_game_purchases"])
        return True if match else False

    def __get_online_gaming(self):
        match = self.soup.find("span", GAME_SELECTORS["online_gaming"])
        return True if match else False

    def __get_ps_plus_required(self):
        match = self.soup.find("span", GAME_SELECTORS["ps_plus_required"])
        return True if match else False

    def __get_ps_pro_support(self):
        match = self.soup.find("span", GAME_SELECTORS["ps_pro_support"])
        return True if match else False

    def __get_preorder(self):
        match = self.soup.find("span", GAME_SELECTORS["preorder"])
        return True if match else False

    def __get_cover_picture(self):
        try:
            cover_picture_url = self.soup.select(GAME_SELECTORS["cover_picture"])[0]['src']
        except AttributeError:
            return ""
        else:
            return re.sub(pattern=r'\?.*', repl='', string=cover_picture_url)

    def __get_price(self):
        try:
            return int(re.sub(r'\D', '', self.soup.find("span", GAME_SELECTORS["price"]).text))
        except AttributeError:
            return 0

    def __get_original_price(self):
        try:
            return int(re.sub(r'\D', '', self.soup.find("span", GAME_SELECTORS["original_price"]).text))
        except AttributeError:
            return 0

    def __get_former_price(self):
        try:
            return int(re.sub(r'\D', '', self.soup.find("span", GAME_SELECTORS["previous price"]).text))
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
        self.__load_page()

        return {
            "title": self.__get_title(),
            "link": self.url,
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
                    "ps4pro": self.__get_ps_pro_support()
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
                    "ps_plus_required": self.__get_ps_plus_required()
                }

            }
        }

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
        Return game info as JSON string
        """
        return json.dumps(self.__make_payload(), ensure_ascii=False, indent=4)


print(PS4Game(alias='EP1121-CUSA19036_00-CLOUDPUNK0000001').as_yaml())
