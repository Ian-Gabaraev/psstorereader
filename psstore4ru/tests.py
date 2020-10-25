import unittest
import json
from .games import PS4Game
import asyncio
from .enmasse import EnMasse


class Games(unittest.TestCase):

    def test_online_game_support(self):
        """
        Test if "online gaming" flag is processed correctly
        :return:
        """
        targets = [
            'EP0082-CUSA19120_00-0000000000000000',
            'EP4365-CUSA17615_00-WAR40KMECHANICUS',
            'EP4826-CUSA18828_00-0000000000000001',
        ]

        results = [
            dict(json.loads(PS4Game(alias=target).as_json()))['details']['misc']['online']
            for target in targets
        ]

        self.assertEqual(results, [False, False, False])


class AsynchronousMethods(unittest.TestCase):

    async def test_get_f2p_in_bulk_returns_nonempty(self):
        """
        Test if fetching Free To Play games in bulk returns non-empty set
        :return:
        """
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(EnMasse.get_all_f2p_games_links(iterations=3))
        result = await loop.run_until_complete(future)

        self.assertTrue(bool(result))

    async def test_get_tbr_in_bulk_returns_nonempty(self):
        """
        Test if fetching To Be Released games in bulk returns non-empty set
        :return:
        """
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(EnMasse.get_all_soon_tbr_games_links(iterations=3))
        result = loop.run_until_complete(future)

        self.assertTrue(bool(result))

    async def test_get_vr_in_bulk_returns_nonempty(self):
        """
        Test if fetching VR games in bulk returns non-empty set
        :return:
        """
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(EnMasse.get_all_vr_games_links(iterations=3))
        result = loop.run_until_complete(future)

        self.assertTrue(bool(result))

    async def test_get_new_in_bulk_returns_nonempty(self):
        """
        Test if fetching new games in bulk returns non-empty set
        :return:
        """
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(EnMasse.get_all_new_games_links(iterations=3))
        result = loop.run_until_complete(future)

        self.assertTrue(bool(result))

    async def test_get_all_in_bulk_returns_nonempty(self):
        """
        Test if fetching all games in bulk returns non-empty set
        :return:
        """
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(EnMasse.get_all_games_links(iterations=3))
        result = loop.run_until_complete(future)

        self.assertTrue(bool(result))
