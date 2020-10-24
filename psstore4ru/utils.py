from bs4 import BeautifulSoup
from variables import HEADERS
import requests


class Helpers:

    @staticmethod
    def get_soup(link):
        response = requests.get(link, headers=HEADERS)
        source = response.content
        soup = BeautifulSoup(source, features='html.parser')
        return soup


async def get_async_soup(url, session):
    async with session.get(url) as response:
        return await response.read()
