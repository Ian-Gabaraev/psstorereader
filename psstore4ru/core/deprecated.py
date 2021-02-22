from psstore4ru.core.scraping_routines.utils.reusable import Helpers
from psstore4ru.core.scraping_routines.meta.variables import EXTERNAL
from psstore4ru.core.scraping_routines.catalogue_page import Scraper


class PSStore:

    def __init__(self):
        self.links = set()
        self.new_games_links = set()
        self.f2p_games = set()
        self.soon_tbr_games = set()
        self.vr_games = set()

    def __collect_multi_page_links(self, source: str, target: set):
        """
        Collects all the links from all the pages
        :param source: page URL to crawl
        :param target: object to store collected data
        """
        start_page = 1
        soup = Helpers.get_soup(source % start_page)
        products = Scraper(soup).get_products_dictionary()
        links = (Scraper.extract_cusa_code(product) for product in products)

        while links:
            for link in links:
                target.add(link)

            start_page += 1
            soup = Helpers.get_soup(source % start_page)
            products = Scraper(soup).get_products_dictionary()
            links = (Scraper.extract_cusa_code(product) for product in products)

    def get_all_games_links(self):
        self.__collect_multi_page_links(source=EXTERNAL['all'], target=self.links)

        return self.links

    def get_soon_tbr_games_links(self) -> set:
        """
        Retrieve games IDs from "Soon to be released"
        """
        self.__collect_multi_page_links(source=EXTERNAL['soon'], target=self.soon_tbr_games)

        return self.soon_tbr_games

    def get_f2p_games_links(self) -> set:
        """
        Retrieve games IDs from "Free to play"
        """
        self.__collect_multi_page_links(source=EXTERNAL['f2p'], target=self.f2p_games)

        return self.f2p_games

    def get_vr_games_links(self) -> set:
        """
        Retrieve games IDs from "VR"
        """
        self.__collect_multi_page_links(source=EXTERNAL['vr'], target=self.vr_games)

        return self.vr_games

    def get_all_new_games_links(self) -> set:
        """
        Retrieve games IDs from "New"
        """
        self.__collect_multi_page_links(source=EXTERNAL['latest'], target=self.new_games_links)

        return self.new_games_links
