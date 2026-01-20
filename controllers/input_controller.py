import arcade


class InputController:
    def __init__(self, game_state):
        self.game_state = game_state
        self.selected_unit = None

    def on_mouse_press(self, x, y, button):
        """Обработка клика мыши"""
        if button == arcade.MOUSE_BUTTON_RIGHT:
            # ПКМ - команда на движение
            if self.selected_unit:
                self.selected_unit.model.move_to(x, y)

        elif button == arcade.MOUSE_BUTTON_LEFT:
            # ЛКМ обрабатывается в game_view
            pass

    def select_unit(self, unit_sprite):
        """Выделение/снятие выделения юнита"""
        # Если кликнули по тому же юниту - снимаем выделение
        if self.selected_unit == unit_sprite:
            self.selected_unit.color = arcade.color.WHITE
            self.selected_unit = None
            self.game_state.selected_unit = None
            print("Выделение снято")
            return

        # Сбрасываем цвет у предыдущего юнита
        if self.selected_unit:
            self.selected_unit.color = arcade.color.WHITE

        # Выделяем новый юнит
        self.selected_unit = unit_sprite
        self.game_state.selected_unit = unit_sprite.model

        # Подсвечиваем выбранный юнит
        if unit_sprite.model.team == 1:
            self.selected_unit.color = arcade.color.LIGHT_GREEN

        print(f"Юнит выбран (Team {unit_sprite.model.team})")