import unittest
import json
from .games import PS4Game
import asyncio
from .enmasse import EnMasse


class Games(unittest.TestCase):

    def test_online_game_support_no_online(self):
        """
        Test if "online gaming" flag is processed correctly
        for games without online mode
        """
        targets = [
            'EP0082-CUSA19120_00-0000000000000000',  # DRAGON QUEST XI S
            'EP4365-CUSA17615_00-WAR40KMECHANICUS',
            'EP4826-CUSA18828_00-0000000000000001',
            'EP3111-CUSA19519_00-JANDUSOFT0000001',
            'EP3877-CUSA20588_00-FLYINGBASEGAME00',  # Flying Soldiers
            'EP0082-CUSA24813_00-BALANWWE00000001',  # Balan Wonderworld
        ]

        results = [
            dict(json.loads(PS4Game(alias=target).as_json()))['details']['misc']['online']
            for target in targets
        ]

        self.assertEqual(results, [False for _ in range(len(targets))])

    def test_online_game_support_online_supported(self):
        """
        Test if "online gaming" flag is processed correctly
        for games with online mode
        """
        targets = [
            'EP0700-CUSA05392_00-DIGIMONWORLDNE0A',  # Digimon World: Next Order
            'EP1464-CUSA07669_00-PSCP110000000000',  # Fortnite
            'EP9001-CUSA02168_00-GTSPORT000000000',  # Gran Turismo Sport
            'EP4947-CUSA15055_00-CONCEPTION1EU000',  # Conception PLUS
            'EP1001-CUSA19467_00-00000PGATOUR2K21',  # PGA TOUR 2K21
            'EP4384-CUSA04038_00-MAHJONGCARN0PS4E',  # Mahjong Carnival
            'EP0102-CUSA04284_00-RE5HDPS400000000',  # Resident Evil 5
            'EP0102-CUSA07340_00-DDDAFULLGAME0000',  # Dragon's Dogma: Dark Arisen
        ]

        results = [
            dict(json.loads(PS4Game(alias=target).as_json()))['details']['misc']['online']
            for target in targets
        ]

        self.assertEqual(results, [True for _ in range(len(targets))])


class AsynchronousMethods(unittest.TestCase):

    async def test_get_f2p_in_bulk_returns_nonempty(self):
        """
        Test if fetching Free To Play games in bulk returns non-empty set:
        """
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(EnMasse.get_all_f2p_games_links(iterations=3))
        result = loop.run_until_complete(future)

        self.assertTrue(bool(result))

    async def test_get_tbr_in_bulk_returns_nonempty(self):
        """
        Test if fetching To Be Released games in bulk returns non-empty set
        """
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(EnMasse.get_all_soon_tbr_games_links(iterations=3))
        result = loop.run_until_complete(future)

        self.assertTrue(bool(result))

    async def test_get_vr_in_bulk_returns_nonempty(self):
        """
        Test if fetching VR games in bulk returns non-empty set
        """
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(EnMasse.get_all_vr_games_links(iterations=3))
        result = loop.run_until_complete(future)

        self.assertTrue(bool(result))

    async def test_get_new_in_bulk_returns_nonempty(self):
        """
        Test if fetching new games in bulk returns non-empty set
        """
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(EnMasse.get_all_new_games_links(iterations=3))
        result = loop.run_until_complete(future)

        self.assertTrue(bool(result))

    async def test_get_all_in_bulk_returns_nonempty(self):
        """
        Test if fetching all games in bulk returns non-empty set
        """
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(EnMasse.get_all_games_links(iterations=3))
        result = loop.run_until_complete(future)

        self.assertTrue(bool(result))
