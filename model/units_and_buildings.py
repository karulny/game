class UnitModel:
    def __init__(self, x, y, name="Крестьянин"):
        self.x = x  # Экранная координата X
        self.y = y  # Экранная координата Y
        self.name = name
        self.hp = 100
        self.selected = False
        self.speed = 2