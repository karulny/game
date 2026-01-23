from config import STARTING_MONEY, MONEY_PER_SECOND


class GameState:
    """Центральное хранилище состояния игры"""

    def __init__(self, game_map, tile_width, tile_height):
        self.units = []
        self.selected_unit = None
        self.game_map = game_map
        self.tile_width = tile_width
        self.tile_height = tile_height

        # Экономика (НОВОЕ!)
        self.money = STARTING_MONEY
        self.money_timer = 0.0

        # Здания (НОВОЕ!)
        self.buildings = []

    def update(self, delta_time):
        """Обновление всех юнитов и зданий"""
        # Обновляем юнитов
        for unit in self.units[:]:
            if unit.hp <= 0:
                self.units.remove(unit)
                continue

            unit.update(
                delta_time,
                self.game_map,
                self.units,
                self.tile_width,
                self.tile_height
            )

        # Обновляем здания
        for building in self.buildings:
            building.update(delta_time)

        # Пассивный доход денег
        self.money_timer += delta_time
        if self.money_timer >= 1.0:  # Каждую секунду
            self.money += MONEY_PER_SECOND
            self.money_timer = 0.0

    def can_afford(self, cost):
        """Проверка, хватает ли денег"""
        return self.money >= cost

    def spend_money(self, amount):
        """Потратить деньги"""
        if self.can_afford(amount):
            self.money -= amount
            return True
        return False