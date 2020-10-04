import requests
import re
import json
from variables import SPECS, GAME_SELECTORS, EXTERNAL
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
        return self.soup.find("h2", GAME_SELECTORS["title"]).text or ""

    def __get_publisher(self):
        publisher = self.soup.find("h5", GAME_SELECTORS["publisher"]).text
        return "" if '\n' in publisher else publisher

    def __get_category(self):
        return self.soup.find("span", GAME_SELECTORS["category"]).text or ""

    def __get_price(self):
        return int(re.sub(r'\D', '', self.soup.find("h3", GAME_SELECTORS["price"]).text)) or 0

    def __get_former_price(self):
        return int(re.sub(r'\D', '', self.soup.find("span", GAME_SELECTORS["previous price"]).text)) or 0

    def __get_ps_plus(self):
        return self.soup.find("div", GAME_SELECTORS["psplus discount"]).text

    def __get_cover(self):
        cover_picture_url = self.soup.select(GAME_SELECTORS["cover"])
        return cover_picture_url[0]['src'] or ""

    def __get_description(self):
        return self.soup.find("div", GAME_SELECTORS["description"]).text or ""

    def __get_language(self):
        return list(set(filter(lambda l: l in self.languages, self.specs))) or []

    def __get_genre(self):
        return list(set(filter(lambda g: g in self.genres, self.specs))) or []

    def __get_size(self):
        return " ".join(self.specs[self.specs.index('Размер файла'):]) or None

    def __get_age(self):
        img_tag = self.soup.find('img', {'class': 'content-rating__rating-img'})
        src_attribute = re.search(r'/(\d+)\.(png|jpg|svg)', img_tag['src'])
        return int(src_attribute.group(1)) or 0

    def __get_screenshots(self):
        if self.__get_cover():
            api_url = re.sub(r'\/image\?.*', '', self.__get_cover())
            json_data = requests.get(api_url).json()
            return [element["url"] for element in json_data["mediaList"]["screenshots"]] or []

    def __load_page(self):
        response = requests.get(self.url.encode("utf-8").decode("utf-8-sig"))
        html = response.content
        self.soup = BeautifulSoup(html, features='html.parser')
        self.specs = list(map(lambda x: x.strip(), self.soup.find("div", GAME_SELECTORS["specs"]).text.split('\n')))

    # Retrieve results in JSON
    def as_json(self):
        self.__load_page()

        description = {
            "title": self.__get_title(),
            "link": self.url,
            "details": {
                "publisher": self.__get_publisher(),
                "category": self.__get_category(),
                "price": self.__get_price(),
                "previous price": self.__get_former_price(),
                "on sale": True if self.__get_former_price() else False,
                "PS Plus discount": self.__get_ps_plus(),
                "size": self.__get_size(),
                "age limit": self.__get_age(),
                "description": self.__get_description(),
                "cover": self.__get_cover(),
                "language": self.__get_language(),
                "genre": self.__get_genre(),
                "screenshots": self.__get_screenshots(),
            }
        }

        return json.dumps(description, ensure_ascii=False, indent=4)


print(PS4Game(alias='EP0002-CUSA23470_00-CB4STANDARD00001').as_json())