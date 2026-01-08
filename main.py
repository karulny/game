import arcade

from model.game_map import GameMapModel
from model.game_state import GameState
from model.unit_model import UnitModel

from controller.input_controller import InputController

from view.game_view import GameView
from view.main_menu_view import MainMenuView


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "RTS Prototype"


def main():
    # 1️⃣ Создаём окно
    window = arcade.Window(
        width=SCREEN_WIDTH,
        height=SCREEN_HEIGHT,
        title=SCREEN_TITLE,
        resizable=True
    )

    # 2️⃣ Загружаем карту
    tile_map = arcade.load_tilemap(
        "resources/maps/map.tmx",
        scaling=1
    )

    # 3️⃣ MODEL
    game_map_model = GameMapModel(tile_map)
    game_state = GameState()

    # Создаём юниты (ТОЛЬКО модель)
    game_state.units.append(UnitModel(200, 200))
    game_state.units.append(UnitModel(260, 200))

    # 4️⃣ CONTROLLER
    input_controller = InputController(game_state)

    # 5️⃣ VIEW
    game_view = GameView(
        tile_map=tile_map,
        game_state=game_state,
        game_model=game_map_model,
        input_controller=input_controller
    )

    game_view.setup()

    # (если меню не нужно — можно сразу показать game_view)
    menu_view = MainMenuView(game_view)
    window.show_view(menu_view)

    arcade.run()


if __name__ == "__main__":
    main()
