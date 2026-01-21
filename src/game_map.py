"""
Модель карты - логика проходимости и тайлов
"""
import arcade

NAME_OF_IMPASSABLE_LAYER = "Water"
NAME_OF_OBJECT_LAYER = "Objects"
NAME_OF_TILE_LAYER = "Ground"


class GameMapModel:
    """Модель карты с сеткой проходимости"""

    def __init__(self, tile_map: arcade.TileMap):
        self.width = int(tile_map.width)
        self.height = int(tile_map.height)

        # Создаем сетку проходимости (0 - нельзя, 1 - можно, 2 - здание)
        self.grid = [[0 for x in range(self.width)] for y in range(self.height)]

        # Загружаем данные из слоев карты
        self._parse_map_data(tile_map, NAME_OF_TILE_LAYER, 1)
        self._parse_map_data(tile_map, NAME_OF_OBJECT_LAYER, 2)

    def _parse_map_data(self, tile_map: arcade.TileMap, layer_name: str, value: int) -> None:
        """Парсинг слоя и заполнение сетки"""
        layer = tile_map.sprite_lists.get(layer_name)

        if layer:
            for item in layer:
                grid_x = int(item.center_x // (tile_map.tile_width * tile_map.scaling))
                grid_y = int(item.center_y // (tile_map.tile_height * tile_map.scaling))

                if 0 <= grid_x < self.width and 0 <= grid_y < self.height:
                    self.grid[grid_y][grid_x] = value

    def is_passable(self, x: int, y: int) -> bool:
        """Проверка проходимости клетки"""
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return False
        return self.grid[y][x] == 1

    def world_to_grid(self, world_x: float, world_y: float, tile_width: int, tile_height: int):
        """Конвертация мировых координат в координаты сетки"""
        grid_x = int(world_x // tile_width)
        grid_y = int(world_y // tile_height)
        return grid_x, grid_y