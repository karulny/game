# controller/input_controller.py

class InputController:
    def __init__(self, game_state):
        self.state = game_state

    # def select_unit(self, unit_model):
    #     # если кликнули по тому же — снимаем выделение
    #     if self.state.selected_unit == unit_model:
    #         self.state.selected_unit = None
    #     else:
    #         self.state.selected_unit = unit_model

    def move_selected_unit(self, x, y):
        if self.state.selected_unit:
            self.state.selected_unit.set_target(x, y)
