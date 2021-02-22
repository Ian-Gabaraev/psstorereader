import uuid

import json

import asyncio

from aiohttp import ClientSession
from aiohttp import TCPConnector

from psstore4ru.core.scraping_routines.utils.reusable import Helpers
from psstore4ru.core.scraping_routines.meta.variables import EXTERNAL, HEADERS

from psstore4ru.core.scraping_routines.game_page import PS4Game


async def launch():
    tasks = []

    f = open("links.json", "r")
    content = f.read()
    js = dict(json.loads(content))
    links = list(js.values())[:200]

    async with ClientSession(headers=HEADERS, connector=TCPConnector(ssl=False)) as session:
        for link in links:
            task = asyncio.ensure_future(
                Helpers.get_async_soup(
                        session=session, url=f"{EXTERNAL['product']}{link}"
                )
            )
            tasks.append(task)

        soups = await asyncio.gather(*tasks)

        f = open("games.json", "a")
        f.write('{')

        for index, soup in enumerate(soups):
            string = PS4Game(url=soup[1], soup=soup[0]).as_json()
            f.write(f'"{str(uuid.uuid4())}": {string},')
        f.write('}')

loop = asyncio.get_event_loop()
future = asyncio.ensure_future(launch())
loop.run_until_complete(future)
