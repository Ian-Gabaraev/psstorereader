![PyPI - Python Version](https://img.shields.io/pypi/pyversions/psstore-ru)
![GitHub repo size](https://img.shields.io/github/repo-size/Ian-Gabaraev/psstorereader)
![Libraries.io dependency status for GitHub repo](https://img.shields.io/librariesio/github/Ian-Gabaraev/psstorereader)
![GitHub](https://img.shields.io/github/license/Ian-Gabaraev/psstorereader)


### **Python interface for PlayStation Store Russia**

#### **Basic Usage**

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
    cusa_codes = PSStore().get_f2p_games_links()
    
    for code in cusa_codes:
            game = PS4Game(region_code=code)
            print(game.as_yaml())
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
