from bs4 import BeautifulSoup
from psstore4ru.core.scraping_routines.meta.variables import HEADERS
import requests


class Helpers:

    @staticmethod
    def get_soup(link):
        response = requests.get(link, headers=HEADERS)
        source = response.content
        soup = BeautifulSoup(source, features='html.parser')
        return soup

    @staticmethod
    async def get_async_soup(url, session):
        async with session.get(url) as response:
            content = await response.read()
            html = content
            soup = BeautifulSoup(html, features='html.parser')
            return [soup, url]
