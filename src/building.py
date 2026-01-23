"""
Модель здания - логика производства юнитов
"""


class Building:
    """Класс для зданий на карте"""

    def __init__(self, grid_x, grid_y, building_type, owner="neutral"):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.type = building_type
        self.owner = owner  # "player", "enemy", "neutral"

        # Производство юнитов
        self.can_spawn_units = True
        self.spawn_cost = 50  # Стоимость юнита
        self.spawn_cooldown = 0.0  # Кулдаун между спавнами
        self.spawn_delay = 2.0  # Задержка в секундах

        # Координаты для визуала (заполним позже)
        self.world_x = 0
        self.world_y = 0

        # HP здания (для будущих фич)
        self.hp = 500
        self.max_hp = 500

    def update(self, delta_time):
        """Обновление кулдауна"""
        if self.spawn_cooldown > 0:
            self.spawn_cooldown -= delta_time

    def can_spawn(self):
        """Проверка, можно ли спавнить юнита"""
        return self.can_spawn_units and self.spawn_cooldown <= 0 and self.hp > 0

    def start_spawn(self):
        """Начать спавн юнита"""
        self.spawn_cooldown = self.spawn_delay

    def take_damage(self, damage):
        """Получить урон (для будущих фич)"""
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0