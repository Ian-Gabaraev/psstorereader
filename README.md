### **Python interface for PlayStation4 Store Russia**

#### **Basic Usage**

```python
from psstore4ru.games import PS4Game
game = PS4Game(alias="EP0002-CUSA23470_00-CB4STANDARD00001")

print(game.as_json())
```

#### **psstore4 supports different output formats, namely:**
```python
from psstore4ru.games import PS4Game
game = PS4Game(alias="EP0002-CUSA23470_00-CB4STANDARD00001")

print(game.as_json())
print(game.as_yaml())
```