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

        # Движение
        self.target_x = x
        self.target_y = y
        self.speed = 120
        self.radius = 12

        # Состояние
        self.state = UnitState.IDLE

        # Бой
        self.hp = 100
        self.max_hp = 100
        self.damage = 10
        self.attack_range = 60
        self.attack_cooldown = 0.0
        self.attack_delay = 1.0

        self.aggro_range = 100
        self.target_enemy = None

    def move_to(self, x: float, y: float):
        """Команда на движение"""
        self.target_x = x
        self.target_y = y
        self.state = UnitState.MOVE
        self.target_enemy = None  # Сброс цели атаки

    def update(self, delta_time, game_map, units, tile_w, tile_h):
        """Главный апдейт FSM"""
        if self.state == UnitState.MOVE:
            self._update_move(delta_time, game_map, units, tile_w, tile_h)

        elif self.state == UnitState.ATTACK:
            self._update_attack(delta_time, units)

        elif self.state == UnitState.IDLE:
            self._search_enemy(units)

    def _update_move(self, delta_time, game_map, units, tile_w, tile_h):
        """Движение к цели"""
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = math.hypot(dx, dy)

        # Достигли цели
        if dist < 2:
            self.state = UnitState.IDLE
            return

        # Движение
        dir_x = dx / dist
        dir_y = dy / dist

        next_x = self.x + dir_x * self.speed * delta_time
        next_y = self.y + dir_y * self.speed * delta_time

        # Проверка проходимости
        grid_x, grid_y = game_map.world_to_grid(next_x, next_y, tile_w, tile_h)

        if not game_map.is_passable(grid_x, grid_y):
            self.state = UnitState.IDLE
            return

        self.x = next_x
        self.y = next_y

        # Поиск врагов во время движения
        self._search_enemy(units)

    def _search_enemy(self, units):
        """Поиск ближайшего врага в радиусе агро"""
        if not units:
            return

        closest_enemy = None
        closest_dist = self.aggro_range

        for u in units:
            if u is self or u.team == self.team or u.hp <= 0:
                continue

            dx = u.x - self.x
            dy = u.y - self.y
            dist = math.hypot(dx, dy)

            if dist < closest_dist:
                closest_enemy = u
                closest_dist = dist

        if closest_enemy:
            self.target_enemy = closest_enemy
            self.state = UnitState.ATTACK

    def _update_attack(self, delta_time, units):
        """Атака цели"""
        # Цель умерла или исчезла
        if not self.target_enemy or self.target_enemy.hp <= 0:
            self.target_enemy = None
            self.state = UnitState.IDLE
            return

        dx = self.target_enemy.x - self.x
        dy = self.target_enemy.y - self.y
        dist = math.hypot(dx, dy)

        # Цель вне радиуса атаки - преследуем
        if dist > self.attack_range:
            # Двигаемся к врагу
            self.target_x = self.target_enemy.x
            self.target_y = self.target_enemy.y

            # Небольшое движение в сторону врага
            dir_x = dx / dist
            dir_y = dy / dist
            self.x += dir_x * self.speed * delta_time
            self.y += dir_y * self.speed * delta_time
            return

        # Атакуем
        self.attack_cooldown -= delta_time

        if self.attack_cooldown <= 0:
            # Наносим урон
            self.target_enemy.hp -= self.damage
            self.attack_cooldown = self.attack_delay

            print(f"Team {self.team} атакует! Урон: {self.damage}, HP врага: {self.target_enemy.hp}")

            # Если враг умер
            if self.target_enemy.hp <= 0:
                print(f"Team {self.target_enemy.team} юнит уничтожен!")