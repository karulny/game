import arcade

from view.unit_sprite import UnitSprite


class GameView(arcade.View):
    def __init__(self, tile_map, game_state, game_model, input_controller):
        super().__init__()

        self.game_state = game_state
        self.game_map = game_model
        self.input_controller = input_controller
        self.camera = arcade.camera.Camera2D()

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

        for unit_model in self.game_state.units:
            sprite = UnitSprite(unit_model, textures)
            self.unit_sprites.append(sprite)

    def on_draw(self):
        self.clear()
        self.scene.draw()

        for unit in self.game_state.units:
            self.draw_unit(unit)
            arcade.draw_line(
                unit.x,
                unit.y,
                unit.target_x,
                unit.target_y,
                arcade.color.YELLOW
            )

    def on_update(self, dt):
        for unit in self.unit_sprites:
            unit.update(dt, self)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        # Проверяем наличие спрайтов в точке клика
        hit_sprites = arcade.get_sprites_at_point((x, y), self.unit_sprites)
        print("pressed")
        if button == arcade.MOUSE_BUTTON_LEFT:
            if hit_sprites:
                # Клик по юниту (выбор или отмена выбора)
                self.input_controller.select_unit(hit_sprites[0])
            elif self.input_controller.selected_unit:
                # Клик по пустому месту ПРИ наличии выбранного юнита — движение
                self.input_controller.on_mouse_pressed(x, y)


    def draw_unit(self, unit):
        color = arcade.color.BLUE if unit.team == 0 else arcade.color.RED

        arcade.draw_circle_filled(
            unit.x,
            unit.y,
            unit.radius,
            color
        )