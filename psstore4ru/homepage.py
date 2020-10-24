import threading
import json
import sys
from utils import Helpers
from variables import EXTERNAL, SELECTORS, PATTERNS


class PS4StoreRussia:

    def __init__(self):
        self.store_homepage = EXTERNAL["store_homepage"]
        self.new_games_homepage = EXTERNAL["new_games_homepage"]
        self.links = set()
        self.discounts = EXTERNAL["discounts"]
        self.tops = EXTERNAL["top sellers home"]
        self.f2p = EXTERNAL["ftp home"]
        self.soon = EXTERNAL["soon home"]
        self.discount_games = set()
        self.new_games_links = set()
        self.threads = []
        self.ps_plus_games = []
        self.top_sellers = set()
        self.f2p_games = set()
        self.soon_tbr_games = set()

    def __get_soon_tbr_last_page_number(self):
        soup = Helpers.get_soup(self.soon)
        end = soup.find('a', SELECTORS["lp new games"])
        try:
            result = PATTERNS["lp top sellers"].search(end['href'])
        except TypeError:
            return False
        else:
            return int(result[1])

    def __get_free_to_play_last_page_number(self):
        soup = Helpers.get_soup(self.f2p)
        end = soup.find('a', SELECTORS["lp new games"])
        result = PATTERNS["lp top sellers"].search(end['href'])
        return int(result[1])

    def __get_top_sellers_catalogue_last_page_number(self):
        soup = Helpers.get_soup(self.tops)
        end = soup.find('a', SELECTORS["lp new games"])
        result = PATTERNS["lp top sellers"].search(end['href'])
        return int(result[1])

    def __get_discounts_catalogue_last_page_number(self):
        soup = Helpers.get_soup(self.discounts)
        end = soup.find('a', SELECTORS["lp new games"])
        result = PATTERNS["lp discounts"].search(end['href'])
        return int(result[1])

    def __collect_multipage_links(self, source: str, target: set):
        start_page = 1
        soup = Helpers.get_soup(source % start_page)
        links = (link for link in soup.find_all('a', SELECTORS["collect ng"]))

        while links:
            for link in links:
                target.add(json.loads(link['data-telemetry-meta'])['id'])

            start_page += 1
            soup = Helpers.get_soup(EXTERNAL["latest"] % start_page)
            links = soup.find_all('a', SELECTORS["collect ng"])

    def __collect_top_sellers_links(self):
        for i in range(1, self.__get_top_sellers_catalogue_last_page_number() + 1):
            soup = Helpers.get_soup(EXTERNAL["top sellers"] % i)
            for link in soup.find_all('a', SELECTORS["collect ng"]):
                self.top_sellers.add(EXTERNAL["host"] + link['href'])

    def __collect_discounts_links(self):
        for i in range(1, self.__get_discounts_catalogue_last_page_number() + 1):
            soup = Helpers.get_soup(EXTERNAL["discounts homepage"] % i)
            for link in soup.find_all('a', SELECTORS["collect ng"]):
                self.discount_games.add(EXTERNAL["host"] + link['href'])

    def get_all_discounts_links(self):
        self.__collect_discounts_links()
        return self.discount_games

    def __get_full_catalogue_last_page_number(self):
        soup = Helpers.get_soup(self.store_homepage)
        end = soup.find('a', SELECTORS["lp full"])
        result = PATTERNS["lp full"].search(end['href'])
        return int(result[1])

    def __get_new_games_last_page_number(self):
        soup = Helpers.get_soup(self.new_games_homepage)
        end = soup.find('a', SELECTORS["lp new games"])
        result = PATTERNS["lp new games"].search(end['href'])
        return int(result[1])

    def __collect_all_catalogue_links(self, number):
        soup = Helpers.get_soup(EXTERNAL["all"] % number)
        for link in soup.find_all('a', SELECTORS["collect full"]):
            self.links.add(EXTERNAL["host"] + link['href'])

    def __run_threads(self):
        for i in range(1, self.__get_full_catalogue_last_page_number() + 1):
            worker = threading.Thread(target=self.__collect_all_catalogue_links, args=(i,))
            self.threads.append(worker)
        for thread in self.threads:
            thread.start()
        for thread in self.threads:
            thread.join()

    def get_ps_plus_deals(self):
        soup = Helpers.get_soup(EXTERNAL["ps plus"])
        divs = soup.find_all('div', SELECTORS["ps plus container"])
        for container in divs:
            self.ps_plus_games.append(EXTERNAL["host"] +
                                      container.find('a', SELECTORS["ps plus link"])['href'])
        return self.ps_plus_games

    def get_all_links(self):
        self.__run_threads()
        return self.links

    def get_top_sellers(self):
        self.__collect_top_sellers_links()
        return self.top_sellers

    def get_soon_tbr_games(self) -> set:
        """
        Retrieve games IDs from "Soon to be released"
        """
        self.__collect_multipage_links(source=EXTERNAL['soon'], target=self.soon_tbr_games)

        return self.soon_tbr_games

    def get_f2p_games_links(self) -> set:
        """
        Retrieve games IDs from "Free to play"
        """
        self.__collect_multipage_links(source=EXTERNAL['f2p'], target=self.f2p_games)

        return self.f2p_games

    def get_all_new_games_links(self) -> set:
        """
        Retrieve games IDs from "New"
        """
        self.__collect_multipage_links(source=EXTERNAL['latest'], target=self.new_games_links)

        return self.new_games_links


print(
    PS4StoreRussia().get_soon_tbr_games()
)
