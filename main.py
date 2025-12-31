import arcade
from view.main_menu_view import MainMenuView
from controller.input_controller import InputController
from view.game_view import GameView
from model.game_map import GameMapModel
from model.game_state import GameState

def main():
    window = arcade.Window(title="RTS Prototype", resizable=True) # Размеры из config.py
    # Загрузка карты
    tile_map = arcade.load_tilemap("resources/maps/map.tmx")

    game_model = GameMapModel(tile_map)
    game_state = GameState()
    input_controller = InputController(game_model, game_state)
    # Загружаем все для отрисовки
    game_view = GameView(tile_map, game_state, game_model, input_controller)

    game_view.setup()
    menu_view = MainMenuView(game_view)

    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()