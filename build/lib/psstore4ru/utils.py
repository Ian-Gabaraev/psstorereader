from bs4 import BeautifulSoup
import requests


class Helpers:

    @staticmethod
    def get_soup(link):
        response = requests.get(link)
        source = response.content
        soup = BeautifulSoup(source, features='html.parser')
        return soup
