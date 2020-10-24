import threading
import json
from utils import Helpers
from variables import EXTERNAL, SELECTORS, PATTERNS


class PS4StoreRussia:

    def __init__(self):
        self.links = set()
        self.new_games_links = set()
        self.f2p_games = set()
        self.soon_tbr_games = set()
        self.vr_games = set()
        self.threads = []

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

    def get_all_links(self):
        self.__run_threads()
        return self.links

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

    def get_vr_games_links(self) -> set:
        """
        Retrieve games IDs from "VR"
        """
        self.__collect_multipage_links(source=EXTERNAL['vr'], target=self.vr_games)

        return self.vr_games

    def get_all_new_games_links(self) -> set:
        """
        Retrieve games IDs from "New"
        """
        self.__collect_multipage_links(source=EXTERNAL['latest'], target=self.new_games_links)

        return self.new_games_links


print(
    PS4StoreRussia().get_vr_games_links()
)
