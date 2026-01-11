import arcade

from model.game_map import GameMapModel
from model.game_state import GameState
from model.unit_model import UnitModel

from controller.input_controller import InputController
from view.game_view import GameView


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "RTS Prototype"


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT,
            title=SCREEN_TITLE,
            resizable=True
        )

        self.tile_map = arcade.load_tilemap(
            "resources/maps/map.tmx",
            scaling=1
        )

        self.game_map_model = GameMapModel(self.tile_map)

        self.tile_width = self.tile_map.tile_width * self.tile_map.scaling
        self.tile_height = self.tile_map.tile_height * self.tile_map.scaling

        self.game_state = GameState(
            game_map=self.game_map_model,
            tile_width=self.tile_width,
            tile_height=self.tile_height
        )

        self.game_state.units.append(UnitModel(200, 200, team=1))
        self.game_state.units.append(UnitModel(260, 200, team=0))

        self.input_controller = InputController(self.game_state)
        self.game_view = GameView(
            tile_map=self.tile_map,
            game_state=self.game_state,
            input_controller=self.input_controller,
            game_model=self.game_map_model
        )

    def on_draw(self):
        self.clear()
        self.game_view.on_draw()

    def on_update(self, delta_time):
        self.game_state.update(delta_time)

    def on_mouse_press(self, x, y, button, modifiers):
        self.game_view.on_mouse_press(x, y, button, modifiers)


def main():
    window = GameWindow()
    arcade.run()


if __name__ == "__main__":
    main()
