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

        # Списки спрайтов
        self.unit_sprites = None

    def setup(self):
        # Инициализируем сцену из карты
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Инициализируем список юнитов и добавляем его в общую сцену
        # Важно: слой "Units" должен быть создан, чтобы scene.draw() его увидела
        self.unit_sprites = arcade.SpriteList()
        self.scene.add_sprite_list("Units", sprite_list=self.unit_sprites)

        # 1. Загружаем спрайтшит

        spritesheet = arcade.load_spritesheet("resources/units/crossbowmen.png")

        # ИСПРАВЛЕНИЕ: Используем get_texture_grid вместо get_image_grid
        texture_list = spritesheet.get_texture_grid(
            size=(32, 32),
            columns=7,
            count=7
        )

        # 2. Создаем спрайт юнита
        unit = arcade.Sprite()
        # Присваиваем текстуру (теперь это arcade.Texture, а не PIL Image)
        unit.texture = texture_list[0]

        # Координаты
        unit.center_x = 100
        unit.center_y = 100
        unit.scale = 3.0

        # Добавляем спрайт в список
        self.unit_sprites.append(unit)

    def on_draw(self):
        self.clear()

        # scene.draw() отрисует и карту, и юнитов (так как мы их добавили в сцену)
        self.scene.draw()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            # Передаем координаты клика в контроллер
            self.input_controller.on_key_pressed(x, y)

    def on_update(self, delta_time: float) -> bool | None:
        pass