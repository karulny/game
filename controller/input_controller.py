import arcade


class InputController:
    def __init__(self, game_map, game_state):
        self.game_state = game_state
        self.game_map = game_map
        self.selected_unit = None

    def select_unit(self, unit):
        # Если мы кликнули по тому же самому юниту, который уже выбран
        if self.selected_unit == unit:
            self.selected_unit.color = arcade.color.WHITE  # Возвращаем обычный цвет
            self.selected_unit = None  # Снимаем выделение
            print("Выделение снято")
            return

        # Если выбран другой юнит, сначала сбрасываем цвет у старого
        if self.selected_unit:
            self.selected_unit.color = arcade.color.WHITE

        # Выделяем новый юнит
        self.selected_unit = unit
        if self.selected_unit:
            self.selected_unit.color = arcade.color.LIGHT_GREEN
            print("Юнит выбран")

    def on_mouse_pressed(self, x: int, y: int) -> None:
        if self.selected_unit is not None:
            self.selected_unit.move(x, y)