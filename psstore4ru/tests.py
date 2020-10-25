import unittest
import json
from .games import PS4Game


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
