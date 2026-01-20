import arcade
from views.unit_sprite import UnitSprite
from models.unit_model import UnitState


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
        """Создаём Sprite для каждой модели"""
        spritesheet = arcade.load_spritesheet(
            "resources/units/crossbowmen.png"
        )

        textures = spritesheet.get_texture_grid(
            size=(32, 32),
            columns=4,
            count=7,
            hit_box_algorithm=arcade.hitbox.algo_detailed
        )


        for unit_model in self.game_state.units:
            sprite = UnitSprite(unit_model, textures)
            self.unit_sprites.append(sprite)

    def on_draw(self):
        self.clear()
        self.scene.draw()

        self._draw_unit_stats()


    def on_update(self, dt):
        # Удаляем мертвых из логики модели
        self.game_state.units = [u for u in self.game_state.units if u.hp > 0]
        
        # Обновляем спрайты (они сами себя удалят, если hp <= 0)
        self.unit_sprites.update()
            
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        """Обработка кликов"""
        if button == arcade.MOUSE_BUTTON_LEFT:
            # ЛКМ - выбор юнита (по кругу радиуса)
            clicked_unit = None

            for unit_model in self.game_state.units:
                dx = x - unit_model.x
                dy = y - unit_model.y
                dist = (dx * dx + dy * dy) ** 0.5

                if dist <= unit_model.radius:
                    clicked_unit = unit_model
                    break

            if clicked_unit:
                # Выбираем только своих юнитов (team 1)
                if clicked_unit.team == 1:
                    # Находим соответствующий спрайт
                    for sprite in self.unit_sprites:
                        if sprite.model == clicked_unit:
                            self.input_controller.select_unit(sprite)
                            break
            else:
                # Клик по пустому месту - сброс выделения
                if self.input_controller.selected_unit:
                    self.input_controller.selected_unit.color = arcade.color.WHITE
                    self.input_controller.selected_unit = None
                    self.game_state.selected_unit = None

        elif button == arcade.MOUSE_BUTTON_RIGHT:
            # ПКМ - команда на движение/атаку
            if self.input_controller.selected_unit:
                # Проверяем, кликнули ли по вражескому юниту
                clicked_enemy = None

                for unit_model in self.game_state.units:
                    if unit_model.team == 1:  # Пропускаем своих
                        continue

                    dx = x - unit_model.x
                    dy = y - unit_model.y
                    dist = (dx * dx + dy * dy) ** 0.5

                    if dist <= unit_model.radius:
                        clicked_enemy = unit_model
                        break

                if clicked_enemy:
                    # Атаковать врага
                    selected_model = self.input_controller.selected_unit.model
                    selected_model.target_enemy = clicked_enemy
                    selected_model.state = UnitState.ATTACK
                    print(f"Атака врага!")
                else:
                    # Двигаться к точке
                    self.input_controller.on_mouse_press(x, y, button)

    def draw_unit(self, unit):
        """Рисуем круг юнита"""
        color = arcade.color.BLUE if unit.team == 0 else arcade.color.GREEN

        # Подсветка если юнит атакует
        if unit.state == UnitState.ATTACK:
            color = arcade.color.ORANGE

        # arcade.draw_circle_filled(unit.x, unit.y, unit.radius, color)

        # Обводка для выбранного
        if self.game_state.selected_unit == unit:
            arcade.draw_circle_outline(
                unit.x, unit.y,
                unit.radius + 3,
                arcade.color.WHITE, 3
            )
    @staticmethod
    def _draw_health_bar(unit):
        """Рисуем HP бар над юнитом"""
        bar_width = 30
        bar_height = 4
        x = unit.x - bar_width / 2
        y = unit.y + unit.radius + 5

        # Фон (красный)
        arcade.draw_lrbt_rectangle_filled(
            x, x + bar_width,
               y - bar_height / 2, y + bar_height / 2,
            arcade.color.RED
        )

        # HP (зелёный)
        hp_percent = unit.hp / 100.0
        arcade.draw_lrbt_rectangle_filled(
            x, x + (bar_width * hp_percent),
               y - bar_height / 2, y + bar_height / 2,
            arcade.color.GREEN
        )

    def _draw_unit_stats(self):
        for unit in self.game_state.units:
            self._draw_health_bar(unit)
            if unit.state == UnitState.MOVE:
                arcade.draw_line(
                    unit.x, unit.y,
                    unit.target_x, unit.target_y,
                    arcade.color.YELLOW, 2
                )

            # Линия атаки
            elif unit.state == UnitState.ATTACK and unit.target_enemy:
                arcade.draw_line(
                    unit.x, unit.y,
                    unit.target_enemy.x, unit.target_enemy.y,
                    arcade.color.RED, 3
                )

            # Круг радиуса атаки для выбранного юнита
            if self.game_state.selected_unit == unit:
                arcade.draw_circle_outline(
                    unit.x, unit.y,
                    unit.attack_range,
                    arcade.color.RED_ORANGE, 2
                )