# Документация RTS Prototype

## Архитектура проекта

Проект следует паттерну **MVC (Model-View-Controller)**:

- **Models** - игровая логика (юниты, здания, карта)
- **Views** - отрисовка и UI
- **Controllers** - обработка ввода

---

## Модули

### 1. `main.py`

**Назначение:** Точка входа в приложение.

```python
def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game = Game(window)
    game.setup()
    arcade.run()
```

---

### 2. `config.py`

**Назначение:** Константы и настройки игры.

**Основные параметры:**
- `SCREEN_WIDTH/HEIGHT` - размер окна
- `UNIT_SPEED` - скорость юнитов
- `STARTING_MONEY` - начальные деньги
- `UNIT_COST` - стоимость юнита

---

### 3. `game.py`

**Назначение:** Управление игровым циклом.

**Класс `Game`:**

```python
class Game:
    def __init__(self, window):
        self.window = window
        
    def setup(self):
        # Загрузка карты, создание состояния игры
        tile_map = arcade.load_tilemap(MAP_PATH)
        game_state = GameState(...)
```

**Методы:**
- `setup()` - инициализация всех компонентов

---

### 4. `game_state.py`

**Назначение:** Центральное хранилище состояния игры.

**Класс `GameState`:**

```python
class GameState:
    def __init__(self, game_map, tile_width, tile_height):
        self.units = []
        self.selected_unit = None
        self.money = STARTING_MONEY
        self.buildings = []
```

**Методы:**
- `update(delta_time)` - обновление юнитов и зданий
- `can_afford(cost)` - проверка денег
- `spend_money(amount)` - трата денег

---

### 5. `game_map.py`

**Назначение:** Загрузка карты и проверка проходимости.

**Класс `GameMapLoader`:**

```python
class GameMapLoader:
    def __init__(self, tile_map):
        self.grid = [[0 for x in range(width)] for y in range(height)]
        # 0 = непроходимо, 1 = проходимо, 2 = здание
```

**Методы:**
- `is_passable(x, y)` - проверка проходимости клетки
- `world_to_grid(x, y)` - конвертация координат
- `_parse_buildings(tile_map)` - загрузка зданий из Tiled

---

### 6. `unit.py`

**Назначение:** Логика поведения юнита (FSM).

**Enum `UnitState`:**
- `IDLE` - ожидание
- `MOVE` - движение к точке
- `ATTACK` - атака врага

**Класс `Unit`:**

```python
class Unit:
    def __init__(self, x, y, team):
        self.x = x
        self.y = y
        self.team = team
        self.state = UnitState.IDLE
        self.hp = 100
```

**Методы:**
- `move_to(x, y)` - приказ на движение
- `update(delta_time)` - главный FSM
- `_update_move()` - логика движения
- `_update_attack()` - логика атаки
- `_search_enemy()` - поиск врагов в радиусе

---

### 7. `building.py`

**Назначение:** Здания на карте.

**Класс `Building`:**

```python
class Building:
    def __init__(self, grid_x, grid_y, building_type, owner):
        self.type = building_type
        self.owner = owner  # "player", "enemy", "neutral"
        self.spawn_cooldown = 0.0
```

**Методы:**
- `can_spawn()` - проверка возможности спавна
- `start_spawn()` - запуск кулдауна
- `update(delta_time)` - обновление кулдауна

---

### 8. `unit_sprite.py`

**Назначение:** Визуальное представление юнита.

**Класс `UnitSprite`:**

```python
class UnitSprite(arcade.Sprite):
    def __init__(self, model, textures):
        self.model = model
        self.textures = textures
```

**Методы:**
- `update(delta_time)` - синхронизация с моделью
- `_animate()` - переключение кадров анимации

---

### 9. `game_view.py`

**Назначение:** Главное игровое окно.

**Класс `GameView`:**

```python
class GameView(arcade.View):
    def __init__(self, tile_map, game_state, ...):
        self.camera = arcade.camera.Camera2D()
        self.scene = arcade.Scene.from_tilemap(tile_map)
```

**Методы:**
- `on_draw()` - отрисовка игры
- `on_update(delta_time)` - обновление логики
- `on_mouse_press()` - обработка кликов
- `on_key_press()` - обработка клавиш (ESC, F5, F9)
- `_try_spawn_unit()` - создание юнита
- `_update_camera()` - движение камеры

---

### 10. `menu_view.py`

**Назначение:** Главное меню и пауза.

**Класс `MenuView`:**

```python
class MenuView(arcade.View):
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            self.window.show_view(self.game_view)
        elif key == arcade.key.ESCAPE:
            arcade.exit()
```

**Класс `PauseMenu`:**
- Показывается при нажатии ESC в игре
- ESC - вернуться в игру
- Q - выход в главное меню

---

### 11. `input_controller.py`

**Назначение:** Обработка пользовательского ввода.

**Класс `InputController`:**

```python
class InputController:
    def select_unit(self, unit_sprite):
        if self.selected_unit:
            self.selected_unit.color = arcade.color.WHITE
        self.selected_unit = unit_sprite
```

**Методы:**
- `select_unit()` - выделение юнита
- `on_mouse_press()` - обработка ПКМ (движение)

---

### 12. `enemy_ai.py`

**Назначение:** AI противника.

**Класс `EnemyAI`:**

```python
class EnemyAI:
    def __init__(self, game_state):
        self.spawn_timer = 0.0
        self.spawn_interval = 5.0
```

**Методы:**
- `update(delta_time)` - обновление AI
- `_try_spawn_enemy_unit()` - создание вражеского юнита
- `_attack_nearest_player_building()` - атака базы игрока

---

### 13. `save_system.py`

**Назначение:** Сохранение/загрузка игры через SQLite.

**Класс `SaveSystem`:**

```python
class SaveSystem:
    def __init__(self):
        self.db_path = "saves/game.db"
        self._init_database()
```

**Методы:**
- `save_game(game_state, camera_pos, save_name)` - сохранить игру
- `load_game(save_id)` - загрузить игру
- `get_all_saves()` - список сохранений
- `delete_save(save_id)` - удалить сохранение

**Структура БД:**

| Поле | Тип | Описание |
|------|-----|----------|
| id | INTEGER | ID сохранения |
| save_name | TEXT | Название |
| money | INTEGER | Деньги |
| units_data | TEXT (JSON) | Юниты |
| buildings_data | TEXT (JSON) | Здания |
| camera_x, camera_y | REAL | Позиция камеры |
| save_date | TIMESTAMP | Дата сохранения |

---

## Игровой цикл

```
main.py
  └─> Game.setup()
       ├─> Загрузка карты (Tiled TMX)
       ├─> Создание GameState
       ├─> Создание GameView
       └─> Показ MenuView

MenuView (ENTER)
  └─> GameView.on_update()
       ├─> GameState.update()
       │    ├─> Unit.update() (FSM)
       │    └─> Building.update()
       ├─> EnemyAI.update()
       └─> UnitSprite.update()
```

---

## FSM (Finite State Machine) юнита

```
IDLE
  ├─> Поиск врагов → ATTACK
  └─> Получен приказ → MOVE

MOVE
  ├─> Достиг цели → IDLE
  ├─> Враг в радиусе → ATTACK
  └─> Непроходимая клетка → IDLE

ATTACK
  ├─> Враг мертв → IDLE
  ├─> Враг далеко → преследование
  └─> В радиусе атаки → наносит урон
```

---

## Система экономики

- **Стартовые деньги:** 200
- **Пассивный доход:** +10$/сек
- **Стоимость юнита:** 50$
- **Механика:** Клик ЛКМ по зданию → трата денег → спавн юнита

---

## Карта (Tiled TMX)

**Слои:**
- `Water` - непроходимая вода
- `Ground` - проходимая земля
- `Objects` - декорации
- **Object Layers** - здания с параметрами:
  - `building_type` - тип здания
  - `owner` - владелец (player/enemy/neutral)

**Парсинг зданий:**
1. Чтение координат объектов
2. Конвертация в мировые координаты
3. Создание объектов `Building`
4. Пометка в сетке проходимости (2 = здание)

---

## Камера

**Управление:**
- WASD - движение
- Края экрана - движение мышью
- Колесико - зум (0.5x - 2.0x)

**Ограничения:**
- Границы карты
- Минимальный/максимальный зум

---

## Сохранения

**Формат JSON в БД:**

```json
{
  "units_data": [
    {"x": 200, "y": 200, "team": 1, "hp": 80, "state": 1}
  ],
  "buildings_data": [
    {"grid_x": 10, "grid_y": 15, "type": "barracks", "hp": 500}
  ]
}
```

**Автосохранение:** Нет (только F5)

**Загрузка:**
- F9 - последнее сохранение
- Восстановление юнитов, зданий, камеры

---

## Расширение проекта

### Добавить новый тип юнита:

1. Создать спрайты в `assets/images/units/`
2. Добавить константы в `config.py`
3. Расширить `Unit.__init__()` параметром `unit_type`

### Добавить новое здание:

1. Нарисовать в Tiled (Object Layer)
2. Задать `building_type` и `owner`
3. Расширить логику в `Building.update()`

### Добавить новую механику:

1. **Ресурсы:** добавить в `GameState`
2. **Туман войны:** изменить `GameView.on_draw()`
3. **Навыки:** расширить `Unit` новыми состояниями FSM

---

## Зависимости

```
arcade==3.0.0       # Игровой движок
pymunk              # Физика (не используется пока)
```

---

## Производительность

- **Оптимизация:** SpriteList для пакетного рендеринга
- **Ограничения:** ~1000 юнитов без просадок FPS
- **Узкое место:** Поиск ближайшего врага (O(n²))

**Улучшения:**
- Spatial hashing для поиска юнитов
- Quadtree для коллизий
- LOD для далеких юнитов

---

## Лицензия

MIT License - свободное использование и модификация.
