from model.game_state import GameState

class UnitModel:
    def __init__(self, x, y, owner_id, speed=80):
        self.x = x
        self.y = y
        self.speed = speed
        self.target = None
        self.owner_id = owner_id
        self.state = None
        self.target = None

    def set_target(self, x, y):
        self.target = (x, y)

    def update(self, dt, game_state):
        if self.state != "FIGHT":
            enemy = game_state.find_nearest_enemy(self)
            if enemy:
                self.target = enemy
                self.state = "FIGHT"