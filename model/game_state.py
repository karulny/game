from .units_and_buildings import UnitModel

class GameState:
    def __init__(self):
        self.gold = 400
        self.units = []
        self.add_unit()

    def add_unit(self):
        unit_stats = (400, 300, "crossbowmen")
        self.units.append(UnitModel(*unit_stats))