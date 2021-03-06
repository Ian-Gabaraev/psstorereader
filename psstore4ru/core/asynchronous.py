import asyncio
import aiohttp
from psstore4ru.core.scraping_routines.catalogue_page import Scraper
from psstore4ru.core.scraping_routines.utils.reusable import Helpers
from psstore4ru.core.scraping_routines.meta.variables import EXTERNAL


class PSStore:
    """
    Introduces methods for fetching game IDs
    in bulk in asynchronous manner
    """

    @staticmethod
    def pop_empty_results(list_of_objects: list):
        return list(
                filter(
                    lambda nested_list: bool(nested_list), list_of_objects
                )
            )

    @staticmethod
    def soups_to_links(soups: list) -> set:
        results = set()
        for soup_object in soups:
            products = Scraper(soup_object[0]).get_products_dictionary()
            links = (Scraper.extract_cusa_code(product) for product in products)
            for link in links:
                results.add(link)

        return results

    @staticmethod
    async def collect_multi_page_links(source: str, iterations: int):
        """
        Collects all the links from all the pages
        :param source: page URL to crawl
        :param iterations: pages to scan
        """
        tasks = []

        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            for page_number in range(1, iterations+1):
                task = asyncio.ensure_future(
                    Helpers.get_async_soup(session=session, url=source % page_number)
                )
                tasks.append(task)

            responses = await asyncio.gather(*tasks)

            return PSStore.pop_empty_results(responses)

    @staticmethod
    async def get_all_games_links(iterations) -> set:
        """
        Retrieve all games IDs
        """
        raw_data = await PSStore.collect_multi_page_links(
            source=EXTERNAL['all'], iterations=iterations)

        return PSStore.soups_to_links(raw_data)

    @staticmethod
    async def get_all_soon_tbr_games_links(iterations) -> set:
        """
        Retrieve all games IDs from "Soon to be released"
        """
        raw_data = await PSStore.collect_multi_page_links(
            source=EXTERNAL['soon'], iterations=iterations)

        return PSStore.soups_to_links(raw_data)

    @staticmethod
    async def get_all_f2p_games_links(iterations) -> set:
        """
        Retrieve all games IDs from "Free to play"
        """
        raw_data = await PSStore.collect_multi_page_links(
            source=EXTERNAL['f2p'], iterations=iterations)

        return PSStore.soups_to_links(raw_data)

    @staticmethod
    async def get_all_vr_games_links(iterations) -> set:
        """
        Retrieve all games IDs from "VR"
        """
        raw_data = await PSStore.collect_multi_page_links(
            source=EXTERNAL['vr'], iterations=iterations)

        return PSStore.soups_to_links(raw_data)

    @staticmethod
    async def get_all_new_games_links(iterations) -> set:
        """
        Retrieve all games IDs from "New"
        """
        raw_data = await PSStore.collect_multi_page_links(
            source=EXTERNAL['latest'], iterations=iterations)

        return PSStore.soups_to_links(raw_data)
