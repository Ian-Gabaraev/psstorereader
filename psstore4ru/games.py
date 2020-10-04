import requests
import re
import json
from variables import APP_PARAMETERS, EXTERNAL, SPECS, SELECTORS
from bs4 import BeautifulSoup


class PS4Game:
    def __init__(self, url: str = None, alias: str = None):
        self.url = url if url else
        self.languages = SPECS["languages"]
        self.genres = SPECS["genres"]
        self.soup = None
        self.specs = []

    def __get_title(self):
        return self.soup.find("h2", SELECTORS["title"]).text or ""

    def __get_publisher(self):
        publisher = self.soup.find("h5", SELECTORS["publisher"]).text
        return "" if '\n' in publisher else publisher

    def __get_category(self):
        return self.soup.find("span", SELECTORS["category"]).text or ""

    def __get_price(self):
        return int(re.sub(r'\D', '', self.soup.find("h3", SELECTORS["price"]).text)) or 0

    def __get_former_price(self):
        return int(re.sub(r'\D', '', self.soup.find("span", SELECTORS["previous price"]).text)) or 0

    def __get_ps_plus(self):
        return self.soup.find("div", SELECTORS["psplus discount"]).text

    def __get_cover(self):
        cover_picture_url = self.soup.select(SELECTORS["cover"])
        if cover_picture_url:
            self.cover = cover_picture_url[0]['src'] or ""

    def __get_description(self):
        return self.soup.find("div", SELECTORS["description"]).text or ""

    def __load_page(self):
        response = requests.get(self.url.encode("utf-8").decode("utf-8-sig"))
        html = response.content
        self.soup = BeautifulSoup(html, features='html.parser')
        self.specs = list(map(lambda x: x.strip(), self.soup.find("div", SELECTORS["specs"]).text.split('\n')))

    def get_specs(self):

        if self.cover:
            try:
                api_url = re.sub('\/image\?.*', '', self.cover)
                json_data = requests.get(api_url).json()
                self.screenshots = [element["url"] for element in json_data["mediaList"]["screenshots"]]
            except KeyError:
                pass

        try:
            img_tag = soup.find('img', {'class': 'content-rating__rating-img'})
            src_attribute = re.search('/(\d+)\.(png|jpg|svg)', img_tag['src'])
            self.age = int(src_attribute.group(1))
        except Exception:
            pass

        try:
            specs = list(map(lambda x: x.strip(),
                         soup.find("div", SELECTORS["specs"]).text.split('\n')))
            self.lang = set(filter(lambda l: l in self.languages, specs))
            # Game genre
            self.genre = set(filter(lambda g: g in self.genres, specs))
            # Game file size
            try:
                self.size = " ".join(specs[specs.index('Размер файла'):])
            except ValueError:
                pass
        except AttributeError:
            pass

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
                "size": self.size,
                "age limit": self.age,
                "description": self.__get_description(),
                "cover": self.cover,
                "screenshots": self.screenshots,
            }
        }

        if self.lang is not None:
            description['details']['language'] = list(self.lang)
        else:
            description['details']['language'] = self.lang
        if self.genre is not None:
            description['details']['genre'] = list(self.genre)
        else:
            description['details']['genre'] = self.genre
        return json.dumps(description, ensure_ascii=False, indent=4)
