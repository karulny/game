class InputController:
    def __init__(self, game_map, game_state):

        self.game_state = game_state
        self.game_map = game_map

    @staticmethod
    def on_key_pressed(x, y):
        print(x, y)