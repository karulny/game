class GameState:
    def __init__(self):
        self.units = []
        self.selected_unit = None

    def update(self, dt, game_map):
        for unit in self.units:
            unit.update(dt, game_map)