import arcade

from view.unit_sprite import UnitSprite


class GameView(arcade.View):
    def __init__(self, tile_map, game_state, game_model, input_controller):
        super().__init__()

        self.state = game_state
        self.game_map = game_model
        self.controller = input_controller

        # Сцена
        self.scene = arcade.Scene.from_tilemap(tile_map)

        # Юниты
        self.unit_sprites = arcade.SpriteList()
        self.scene.add_sprite_list("Units", sprite_list=self.unit_sprites)

    def setup(self):
        """
        Создаём Sprite для каждой модели
        """
        spritesheet = arcade.load_spritesheet(
            "resources/units/crossbowmen.png"
        )

        textures = spritesheet.get_texture_grid(
            size=(32, 32),
            columns=7,
            count=7,
            hit_box_algorithm=arcade.hitbox.algo_detailed
        )

        for unit_model in self.state.units:
            sprite = UnitSprite(unit_model, textures)
            self.unit_sprites.append(sprite)

    def on_draw(self):
        self.clear()
        self.scene.draw()

    def on_update(self, dt):
        for unit in self.unit_sprites:
            unit.update(dt, self)

    def on_mouse_press(self, x, y, button, modifiers):
        pass