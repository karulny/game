import arcade

class InputController:
    def __init__(self, game_state):
        self.game_state = game_state
        self.selected_unit = None

    def on_mouse_press(self, x, y, button):
        print("pressed")
        if button == arcade.MOUSE_BUTTON_RIGHT:
            print("right")
            for unit in self.game_state.units:
                unit.move_to(x, y)

    def move_selected_unit(self, x, y):
        if self.game_state.selected_unit:
            self.game_state.selected_unit.set_target(x, y)

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
