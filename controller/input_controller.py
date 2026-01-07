import arcade

class InputController:
    def __init__(self, game_map, game_state):

        self.game_state = game_state
        self.game_map = game_map
        self.selected_unit = None

    def on_mouse_pressed(self, x: int, y: int) -> None:
        if self.selected_unit is not None:
            self.selected_unit.move(x, y)

    def select_unit(self, unit):
        if self.selected_unit:
            self.selected_unit.color = arcade.color.WHITE

        self.selected_unit = unit

        if self.selected_unit:
            self.selected_unit.color = arcade.color.LIGHT_GREEN