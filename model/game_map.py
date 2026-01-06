import arcade
import pathfinding

class GameMapModel:
    def __init__(self, tile_map: arcade.TileMap):
        # карта - затычка
        self.width = int(tile_map.width)
        self.height = int(tile_map.height)
        # шаблон клеток - Затычка т.к пока так
        self.grid = [[0 for _ in range(self.height)] for _ in range(self.width)]


    def load_from_tmx(self, tmx):
        pass

    def get_path(self, start, end):
        pass



        
    
