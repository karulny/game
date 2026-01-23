"""
AI противника - автоматический спавн юнитов и управление
"""
import random
from unit import Unit
from config import ENEMY_TEAM, UNIT_COST


class EnemyAI:
    """Простой AI для противника"""

    def __init__(self, game_state):
        self.game_state = game_state
        self.spawn_timer = 0.0
        self.spawn_interval = 5.0  # Спавним юнита каждые 5 секунд

    def update(self, delta_time, unit_textures, unit_sprites):
        """Обновление AI противника"""
        self.spawn_timer += delta_time

        # Пытаемся спавнить юнита
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0.0
            self._try_spawn_enemy_unit(unit_textures, unit_sprites)

    def _try_spawn_enemy_unit(self, unit_textures, unit_sprites):
        """Попытка создать вражеского юнита"""
        # Ищем вражеские здания
        enemy_buildings = [b for b in self.game_state.buildings
                           if b.owner == "enemy"]

        if not enemy_buildings:
            return

        # Выбираем случайное здание
        building = random.choice(enemy_buildings)

        # Проверяем кулдаун
        if not building.can_spawn():
            return

        # У врага всегда есть деньги (упрощенный AI)
        # Можешь добавить экономику врагу позже

        # Создаем юнита слева от здания
        spawn_x = building.world_x - 40
        spawn_y = building.world_y

        new_unit = Unit(spawn_x, spawn_y, team=ENEMY_TEAM)
        self.game_state.units.append(new_unit)

        # Создаем спрайт
        from unit_sprite import UnitSprite
        sprite = UnitSprite(new_unit, unit_textures)
        unit_sprites.append(sprite)

        # Запускаем кулдаун
        building.start_spawn()

        print(
            f"Враг создал юнита! Всего вражеских юнитов: {len([u for u in self.game_state.units if u.team == ENEMY_TEAM])}")

        # Даем юниту приказ атаковать ближайшую базу игрока
        self._attack_nearest_player_building(new_unit)

    def _attack_nearest_player_building(self, unit):
        """Отправить юнита к ближайшему зданию игрока"""
        player_buildings = [b for b in self.game_state.buildings
                            if b.owner == "player"]

        if not player_buildings:
            return

        # Находим ближайшее здание
        closest = min(player_buildings,
                      key=lambda b: ((b.world_x - unit.x) ** 2 + (b.world_y - unit.y) ** 2) ** 0.5)

        # Двигаемся к нему
        unit.move_to(closest.world_x, closest.world_y)