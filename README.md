### **Python interface for PlayStation4 Store Russia**

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

print(game.as_json())
print(game.as_yaml())
```

#### Syncronous scraping is slow, so psstore utilizes asynchronicity
##### Get CUSA codes from the first 10 pages on PS Store
```python
from psstore4ru.core.asynchronous import PSStore
from psstore4ru.core.scraping_routines.game_page import PS4Game

async def get_games_as_dict_fast():
    cusa_codes = await PSStore.get_all_games_links(iterations=10)

    for code in cusa_codes:
        game = PS4Game(region_code=code)
        print(game.as_dict())
```
