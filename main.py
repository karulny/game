import arcade
import config
from models.game_map import GameMapModel
from models.game_state import GameState
from models.unit_model import UnitModel
from controllers.input_controller import InputController
from views.game_view import GameView


def main():
    # Создаём окно
    window = arcade.Window(
        width=config.SCREEN_WIDTH,
        height=config.SCREEN_HEIGHT,
        title=config.SCREEN_TITLE,
        resizable=True
    )

    # Загружаем карту
    tile_map = arcade.load_tilemap(
        config.MAP_PATH,
        scaling=config.TILE_SCALING
    )

    # Создаём модель карты
    game_map_model = GameMapModel(tile_map)

    tile_width = tile_map.tile_width * tile_map.scaling
    tile_height = tile_map.tile_height * tile_map.scaling

    # Создаём состояние игры
    game_state = GameState(
        game_map=game_map_model,
        tile_width=tile_width,
        tile_height=tile_height
    )

    # Добавляем юнитов
    game_state.units.append(UnitModel(200, 200, team=config.PLAYER_TEAM))
    game_state.units.append(UnitModel(260, 200, team=config.ENEMY_TEAM))

    # Создаём контроллер
    input_controller = InputController(game_state)

    # Создаём игровое представление
    game_view = GameView(
        tile_map=tile_map,
        game_state=game_state,
        input_controller=input_controller,
        game_model=game_map_model
    )

    # Показываем игровое представление
    window.show_view(game_view)

    # Запускаем игру
    arcade.run()


if __name__ == "__main__":
    main()