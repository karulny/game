import arcade

from controller.input_controller import InputController


class GameView(arcade.View):
    def __init__(self, tile_map: arcade.TileMap, game_state, game_model, input_controller: InputController):
        super().__init__()
        self.tile_map = tile_map
        self.scene = None
        self.input_controller = input_controller
        self.game_state = game_state
        self.game_model = game_model
        self.unit_sprites = arcade.SpriteList()

    def setup(self):

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.unit_sprites.clear()
        for unit_data in self.game_state.units:
            sprite = arcade.Sprite("resources/units/crossbowmen.png", scale=1.0)
            sprite.center_x = unit_data.x
            sprite.center_y = unit_data.y

            sprite.owner = unit_data
            self.unit_sprites.append(sprite)

    def on_draw(self):
        self.clear()
        # Отрисовка всех слоев карты (земля, препятствия и т.д.)
        self.scene.draw()
        self.unit_sprites.draw()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> bool | None:
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.input_controller.on_key_pressed(x, y)