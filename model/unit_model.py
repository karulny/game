import math
from enum import Enum


class UnitState(Enum):
    IDLE = 0
    MOVE = 1
    ATTACK = 2


class UnitModel:
    def __init__(self, x: float, y: float, team: int):
        self.x = x
        self.y = y
        self.team = team

        # движение
        self.target_x = x
        self.target_y = y
        self.speed = 120
        self.radius = 12

        # состояние
        self.state = UnitState.IDLE

        # бой
        self.hp = 100
        self.damage = 10
        self.attack_range = 40
        self.attack_cooldown = 0.0
        self.attack_delay = 1.0

        self.target_enemy = None

    def move_to(self, x: float, y: float):
        self.target_x = x
        self.target_y = y
        self.state = UnitState.MOVE

    def update(self, delta_time, game_map, units, tile_w, tile_h):
        if self.state == UnitState.MOVE:
            self._update_move(delta_time, game_map, tile_w, tile_h)

        elif self.state == UnitState.ATTACK:
            self._update_attack(delta_time)

        elif self.state == UnitState.IDLE:
            self._search_enemy(units)

    def _update_move(self, delta_time, game_map, tile_w, tile_h):
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = math.hypot(dx, dy)

        if dist < 2:
            self.state = UnitState.IDLE
            return

        dir_x = dx / dist
        dir_y = dy / dist

        next_x = self.x + dir_x * self.speed * delta_time
        next_y = self.y + dir_y * self.speed * delta_time

        grid_x, grid_y = game_map.world_to_grid(next_x, next_y, tile_w, tile_h)
        print(game_map.is_passable(grid_x, grid_y))
        if not game_map.is_passable(grid_x, grid_y):
            self.state = UnitState.IDLE
            return

        self.x = next_x
        self.y = next_y

        self._search_enemy(None)

    def _search_enemy(self, units):
        if not units:
            return

        for u in units:
            if u is self or u.team == self.team or u.hp <= 0:
                continue

            dx = u.x - self.x
            dy = u.y - self.y
            dist = math.hypot(dx, dy)

            if dist <= self.attack_range:
                self.target_enemy = u
                self.state = UnitState.ATTACK
                return

    def _update_attack(self, delta_time):
        if not self.target_enemy or self.target_enemy.hp <= 0:
            self.target_enemy = None
            self.state = UnitState.IDLE
            return

        dx = self.target_enemy.x - self.x
        dy = self.target_enemy.y - self.y
        dist = math.hypot(dx, dy)

        if dist > self.attack_range:
            self.target_enemy = None
            self.state = UnitState.MOVE
            self.move_to(self.target_x, self.target_y)
            return

        self.attack_cooldown -= delta_time
        if self.attack_cooldown <= 0:
            self.target_enemy.hp -= self.damage
            self.attack_cooldown = self.attack_delay
