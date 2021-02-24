![PyPI - Python Version](https://img.shields.io/pypi/pyversions/psstore-ru)
![GitHub repo size](https://img.shields.io/github/repo-size/Ian-Gabaraev/psstorereader)
![GitHub](https://img.shields.io/github/license/Ian-Gabaraev/psstorereader)
![Maintenance](https://img.shields.io/maintenance/yes/2021)

# **Python interface for PlayStation&reg; Store 🌍**

#### **Basic Usage**

![Usa](https://github.com/Ian-Gabaraev/psstorereader/blob/master/psstore4ru/usage/ezgif.com-video-to-gif(1).gif)

##### Get JSON representation of a game by CUSA code

```python
from psstore4ru.core.scraping_routines.game_page import PS4Game

game = PS4Game(region_code="EP0002-CUSA23470_00-CB4STANDARD00001")

print(game.as_json())
```

#### **psstore supports different output formats, namely:**

```python
from psstore4ru.core.scraping_routines.game_page import PS4Game

game = PS4Game(region_code="EP0002-CUSA23470_00-CB4STANDARD00001")

print(game.as_dict())
print(game.as_yaml())
```

#### You decide what category of games you want to scrape
```python
from psstore4ru.core.deprecated import PSStore

def get_all_free_to_play_games():
    """
    A call to method
    PSStore().get_f2p_games_links()
    returns a list of CUSA codes correspondings
    to Free-to-Play games on the PS Store,
    e.g ['EP6261-CUSA23678_00-OSRELSIEEGENSHIN', 'EP8062-CUSA17849_00-0190589937083212', ...]
    """
    cusa_codes = PSStore().get_f2p_games_links()
    
    for code in cusa_codes:
            game = PS4Game(region_code=code)
            print(game.as_yaml())
```

#### You can also scrape off a game's specs using its url instead of CUSA code
```python
from psstore4ru.core.scraping_routines.game_page import PS4Game

game = PS4Game(url="https://store.playstation.com/ru-ru/product/EP0002-CUSA23470_00-CB4STANDARD00001")

print(game.as_dict())
```

#### Synchronous scraping is slow, so psstore utilizes asynchronicity
##### Get CUSA codes from the first 10 pages on PS Store
```python
from psstore4ru.core.asynchronous import PSStore
from psstore4ru.core.scraping_routines.game_page import PS4Gam

async def get_games_as_dict_fast():
    cusa_codes = await PSStore.get_all_games_links(iterations=10)

    for code in cusa_codes:
        game = PS4Game(region_code=code)
        print(game.as_dict())
```
