import json
import re

from psstore4ru.core.scraping_routines.meta.variables import SELECTORS


class Scraper:

    def __init__(self, soup):
        self.soup = soup

    @staticmethod
    def __extract_pars_able_data_from_source(soup):
        pinpointed_data = soup.find('script', SELECTORS['products'])
        pinpointed_data_no_opening_tag = str(pinpointed_data).lstrip(SELECTORS['products_script_tag_opening'])
        pinpointed_data_pars_able = pinpointed_data_no_opening_tag.rstrip(SELECTORS['products_script_tag_closing'])

        return pinpointed_data_pars_able

    @staticmethod
    def __extract_nested_payload_from_pars_able_data(pars_able_data):

        return json.loads(pars_able_data)

    @staticmethod
    def __reduce_extracted_payload(dictionary):

        return dictionary[SELECTORS['products_json_root']][SELECTORS['products_json_root_descendant']]

    @staticmethod
    def __extract_hashable_dict_lookup_key(dictionary):
        un_hashable_key = re.search(SELECTORS['category_grid_pattern'], str(dictionary), re.S).group(0)
        hashable_key = un_hashable_key.strip("'")

        return hashable_key

    @staticmethod
    def __retrieve_iterable_dictionary_with_products(dictionary, hashable_key):

        return dictionary[hashable_key]['products']

    @staticmethod
    def extract_cusa_code(dictionary_item):

        return re.search(SELECTORS['cusa_pattern'], dictionary_item['id']).group(1)

    def get_products_dictionary(self):
        pars_able_data = self.__extract_pars_able_data_from_source(self.soup)
        big_payload = self.__extract_nested_payload_from_pars_able_data(pars_able_data)
        reduced_payload = self.__reduce_extracted_payload(big_payload)
        products_dictionary = self.__retrieve_iterable_dictionary_with_products(
            reduced_payload, self.__extract_hashable_dict_lookup_key(reduced_payload)
        )

        return products_dictionary
