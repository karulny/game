class GameState:
    """Центральное хранилище состояния игры"""

    def __init__(self, game_map, tile_width, tile_height):
        self.units = []
        self.selected_unit = None
        self.game_map = game_map
        self.tile_width = tile_width
        self.tile_height = tile_height

    def update(self, delta_time):
        """Обновление всех юнитов"""
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