import arcade

from controller.input_controller import InputController
from .sprites import Unit


class GameView(arcade.View):
    def __init__(self, tile_map: arcade.TileMap, game_state, game_model, input_controller: InputController):
        super().__init__()
        self.tile_map = tile_map
        self.scene = None
        self.input_controller = input_controller
        self.game_state = game_state
        self.game_model = game_model

        # Списки спрайтов
        self.unit_sprites = None

    def setup(self):
        # Инициализируем сцену из карты
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.unit_sprites = arcade.SpriteList()
        self.scene.add_sprite_list("Units", sprite_list=self.unit_sprites)
        self.add_crossbowmen()

    def on_draw(self):
        self.clear()

        self.scene.draw()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        # Находим, по кому кликнули
        hit_sprites = arcade.get_sprites_at_point((x, y), self.unit_sprites)

        if button == arcade.MOUSE_BUTTON_LEFT:
            if hit_sprites:
                self.input_controller.select_unit(hit_sprites[0])
            else:
                self.input_controller.on_mouse_pressed(x, y)

    def on_update(self, delta_time: float) -> bool | None:
        self.scene.update(delta_time)

    def add_crossbowmen(self):
        spritesheet = arcade.load_spritesheet("resources/units/crossbowmen.png")

        # ИСПРАВЛЕНИЕ: Используем get_texture_grid вместо get_image_grid
        texture_list = spritesheet.get_texture_grid(
            size=(32, 32),
            columns=7,
            count=7,
            hit_box_algorithm=arcade.hitbox.algo_detailed
        )

        unit = Unit(200, 200, texture_list=texture_list)

        # Добавляем спрайт в список
        self.unit_sprites.append(unit)
