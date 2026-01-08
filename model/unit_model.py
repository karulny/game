import math

class UnitModel:
    def __init__(self, x, y, speed=80):
        self.x = x
        self.y = y
        self.speed = speed
        self.target = None

    def set_target(self, x, y):
        self.target = (x, y)

    def update(self, dt, game_map):
        if not self.target:
            return

        dx = self.target[0] - self.x
        dy = self.target[1] - self.y
        dist = math.hypot(dx, dy)

        if dist < 2:
            self.target = None
            return

        nx = self.x + (dx / dist) * self.speed * dt
        ny = self.y + (dy / dist) * self.speed * dt

        # простая проверка проходимости
        tile_x = int(nx // 32)
        tile_y = int(ny // 32)

        if game_map.is_passable(tile_x, tile_y):
            self.x = nx
            self.y = ny
