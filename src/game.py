"""
Главный игровой класс - управление игровым циклом и переключением view
"""
import arcade
from config import MAP_PATH, TILE_SCALING, PLAYER_TEAM, ENEMY_TEAM
from game_state import GameState
from game_map import GameMapLoader
from unit import Unit
from input_controller import InputController
from game_view import GameView
from menu_view import MenuView


class Game:
    """Центральный класс управления игрой"""

    def __init__(self, window: arcade.Window):
        self.window = window
        self.game_view = None
        self.menu_view = None

    def setup(self):
        """Инициализация всех компонентов игры"""
        # Загрузка карты
        tile_map = arcade.load_tilemap(
            MAP_PATH,
            scaling=TILE_SCALING
        )

        # Создание модели карты
        game_map_model = GameMapLoader(tile_map)

        # Размеры тайлов
        tile_width = tile_map.tile_width * tile_map.scaling
        tile_height = tile_map.tile_height * tile_map.scaling

        # Создание состояния игры
        game_state = GameState(
            game_map=game_map_model,
            tile_width=tile_width,
            tile_height=tile_height
        )

        # Добавляем здания из карты в состояние игры
        game_state.buildings = game_map_model.buildings

        # Добавление начальных юнитов (меньше, чтобы игрок сам их спавнил)
        game_state.units.append(Unit(200, 200, team=PLAYER_TEAM))
        game_state.units.append(Unit(260, 200, team=ENEMY_TEAM))

        # Создание контроллера
        input_controller = InputController(game_state)

        # Создание представлений
        self.game_view = GameView(
            tile_map=tile_map,
            game_state=game_state,
            input_controller=input_controller,
            game_model=game_map_model
        )

        self.menu_view = MenuView(self.game_view)

        # Показываем меню
        self.window.show_view(self.menu_view)