import requests
import re
import json
import yaml
from psstore4ru.core.scraping_routines.meta.variables import EXTERNAL, GAME_SELECTORS
from bs4 import BeautifulSoup


class PS4Game:
    def __init__(self, url: str = None, region_code: str = None):
        """
        :param url: https://store.playstation.com/ru-ru/product/EP0002-CUSA23470_00-CB4STANDARD00001
        :param region_code: EP0002-CUSA23470_00-CB4STANDARD00001
        """
        self.alias = region_code
        self.url = url if url else f"{EXTERNAL['product']}{self.alias}"
        self.soup = None
        self.specs = []

    def __get_title(self) -> str:

        return self.soup.find("h1", GAME_SELECTORS["title"]).text

    def __get_region_code(self):
        if self.alias:
            return self.alias
        else:
            return re.sub(r'.*product/', '', self.url)

    def __get_publisher(self) -> str:
        try:
            publisher = self.soup.find("div", GAME_SELECTORS["publisher"]).text
        except AttributeError:
            return ""
        else:
            return "" if '\n' in publisher else publisher

    def __get_category(self) -> str:
        return "Предзаказ" if self.__get_preorder() else "Обычный"

    def __get_release_date(self) -> str:
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

    def __get_platforms(self) -> str:
        try:
            return self.soup.find("dd", GAME_SELECTORS["platforms"]).text
        except AttributeError:
            return ""

    def __get_rating(self) -> str:
        try:
            return self.soup.find("img", GAME_SELECTORS["rating"])['alt']
        except AttributeError:
            return ""

    def __get_in_game_purchases(self) -> bool:
        match = self.soup.find("span", GAME_SELECTORS["in_game_purchases"])

        return True if match else False

    def __only_single_player_mode(self) -> bool:
        match_single_player = self.soup.find_all(string=GAME_SELECTORS["single_player"])
        match_online_gaming = self.soup.find_all(string=GAME_SELECTORS["online_gaming"])

        return True if (match_single_player and not match_online_gaming) else False

    def __get_online_gaming(self) -> bool:
        online_gaming_supported = (not self.__only_single_player_mode()) or self.__get_ps_plus_required()

        return True if online_gaming_supported else False

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

    def __get_cover_picture(self) -> str:
        try:
            cover_picture_url = self.soup.select(GAME_SELECTORS["cover_picture"])[0]['src']
        except AttributeError:
            return ""
        except IndexError:
            return ""
        else:
            return re.sub(pattern=r'\?.*', repl='', string=cover_picture_url)

    def __get_price(self) -> int:
        try:
            return int(re.sub(r'\D', '', self.soup.find("span", GAME_SELECTORS["price"]).text))
        except AttributeError:
            return 0
        except ValueError:
            return 0

    def __get_original_price(self) -> int:
        try:
            return int(re.sub(r'\D', '', self.soup.find("span", GAME_SELECTORS["original_price"]).text))
        except AttributeError:
            return 0

    def __get_ps_plus(self) -> str:
        try:
            return self.soup.find("div", GAME_SELECTORS["psplus discount"]).text
        except AttributeError:
            return ""

    def __get_description(self) -> str:
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
            "title":          self.__get_title(),
            "link":           self.url,
            "region_code":    self.__get_region_code(),
            "cover":          self.__get_cover_picture(),
            "description":    self.__get_description(),
            "genres":         self.__get_genres(),
            "ages":           self.__get_rating(),
            "publisher":      self.__get_publisher(),
            "release_date":   self.__get_release_date(),
            "final_price":    self.__get_price(),
            "original_price": self.__get_original_price(),
            "audio":          self.__get_voice(),
            "subtitles":      self.__get_subtitles(),
            "misc": {
                "category":          self.__get_category(),
                "supported":         self.__get_platforms(),
                "ps4pro":            self.__get_ps_pro_tuned(),
                "in_game_purchases": self.__get_in_game_purchases(),
                "online":            self.__get_online_gaming(),
                "ps_plus_required":  self.__get_ps_plus_required(),
                "ps_vr_support":     self.__get_ps_vr_support()
            }
        }

    def as_yaml(self) -> str:
        """
        Return game info as YAML
        """
        return yaml.dump([self.__make_payload()], allow_unicode=True)

    def as_xml(self):
        """
        Return game info as XML
        """
        pass

    def as_json(self) -> str:
        """
        Return game info as JSON
        """
        return json.dumps(self.__make_payload(), ensure_ascii=False, indent=4)

    def as_dict(self) -> dict:
        """
        Return game info as <<dict>> object
        """
        return self.__make_payload()
