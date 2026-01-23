"""
Модель карты - логика проходимости и тайлов
"""
import arcade
from building import Building

NAME_OF_IMPASSABLE_LAYER = "Water"
NAME_OF_BUILDING_LAYER = "Buildings"
NAME_OF_TILE_LAYER = "Ground"


class GameMapLoader:
    """Модель карты с сеткой проходимости"""

    def __init__(self, tile_map: arcade.TileMap):
        self.width = int(tile_map.width)
        self.height = int(tile_map.height)
        self.tile_map = tile_map

        # Создаем сетку проходимости (0 - нельзя, 1 - можно, 2 - здание)
        self.grid = [[0 for x in range(self.width)] for y in range(self.height)]
        self.buildings = []

        # Загружаем данные из слоев карты
        self._parse_map_data(tile_map, NAME_OF_TILE_LAYER, 1)
        self._parse_buildings(tile_map)

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

    def _parse_buildings(self, tile_map: arcade.TileMap) -> None:
        """Парсинг зданий из геометрических объектов Tiled"""
        self.buildings = []

        # Общая высота карты в пикселях (нужна для конвертации координат Y)
        map_height_px = tile_map.height * tile_map.tile_height
        scaling = tile_map.scaling

        # Перебираем слои напрямую через внутренний объект tiled_map
        for layer in tile_map.tiled_map.layers:
            # Проверяем, что это слой объектов
                props = layer.properties if layer.properties else {}

                # Ищем слои, где прописан building_type
                if "building_type" in props:
                    b_type = props.get("building_type")
                    owner = props.get("owner", "neutral")

                    print(f"📦 Обработка слоя объектов '{layer.name}': {b_type} ({owner})")

                    for obj in layer.tiled_objects:

                        # Вычисляем центр объекта в мировых координатах
                        obj_x = obj.coordinates.x
                        obj_y = obj.coordinates.y
                        obj_w = obj.size.width
                        obj_h = obj.size.height

                        # Центр X: (Лево + Ширина/2) * масштаб
                        center_x = (obj_x + obj_w / 2) * scaling

                        # Центр Y: (Высота_карты - (Верх + Высота_объекта/2)) * масштаб
                        center_y = (map_height_px - (obj_y + obj_h / 2)) * scaling

                        # Считаем координаты в сетке (grid)
                        grid_x = int(center_x // (tile_map.tile_width * scaling))
                        grid_y = int(center_y // (tile_map.tile_height * scaling))

                        if 0 <= grid_x < self.width and 0 <= grid_y < self.height:
                            # Помечаем в сетке: 2 - это здание
                            self.grid[grid_y][grid_x] = 2

                            building = Building(grid_x, grid_y, b_type, owner)
                            building.world_x = center_x
                            building.world_y = center_y

                            self.buildings.append(building)
                            print(f"   🏠 Найдено здание в сетке: {grid_x}:{grid_y}")

        print(f"✅ Успешно загружено зданий: {len(self.buildings)}")