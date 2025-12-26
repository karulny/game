import arcade

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.tile_map = None
        self.scene = None

    def setup(self):
        # Путь к файлу из resources/
        map_name = "resources/map.tmx"
        # Загружаем карту (включая слои, созданные другом) [cite: 27-28]
        self.tile_map = arcade.load_tilemap(map_name, scaling=1.0)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

    def on_draw(self):
        self.clear()
        # Отрисовка всех слоев карты (земля, препятствия и т.д.)
        self.scene.draw()