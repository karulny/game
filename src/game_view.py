import arcade
from unit_sprite import UnitSprite
from unit import UnitState
from config import CROSSBOWMEN_SPRITESHEET


class GameView(arcade.View):
    """Главное игровое представление"""

    def __init__(self, tile_map, game_state, game_model, input_controller):
        super().__init__()

        self.game_state = game_state
        self.game_map = game_model
        self.input_controller = input_controller
        # Камера
        self.camera = arcade.camera.Camera2D()
        self.camera_speed = 500
        self.camera_zoom = 1.0

        # Границы карты для создания 'мертвой зоны камеры'
        self.map_width = tile_map.width * tile_map.tile_width * tile_map.scaling
        self.map_height = tile_map.height * tile_map.tile_height * tile_map.scaling

        # Сцена
        self.scene = arcade.Scene.from_tilemap(tile_map)

        # Юниты
        self.unit_sprites = arcade.SpriteList()
        self.scene.add_sprite_list("Units", sprite_list=self.unit_sprites)
        self.setup()

    def setup(self):
        """Создание Sprite для каждой модели"""
        spritesheet = arcade.load_spritesheet(CROSSBOWMEN_SPRITESHEET)

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
        """Отрисовка игры"""
        self.clear()
        self.camera.use()
        self.scene.draw()
        self._draw_unit_stats()

    def on_update(self, delta_time):
        """Обновление логики игры"""
        self._update_camera(delta_time)
        # Удаляем мертвых из логики модели
        self.game_state.update(delta_time)
        self.game_state.units = [u for u in self.game_state.units if u.hp > 0]

        # Обновляем спрайты
        self.unit_sprites.update(delta_time)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        """Обработка кликов мыши"""
        world_x, world_y, world_z = self.camera.unproject((x, y))
        if button == arcade.MOUSE_BUTTON_LEFT:
            self._handle_left_click(world_x, world_y)
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            self._handle_right_click(world_x, world_y)

    def _handle_left_click(self, x: int, y: int):
        """Обработка ЛКМ - выбор юнита"""
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

    def _handle_right_click(self, x: int, y: int):
        """Обработка ПКМ - команда на движение/атаку"""
        if not self.input_controller.selected_unit:
            return

        # Проверяем клик по вражескому юниту
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
            print("Атака врага!")
        else:
            # Двигаться к точке
            self.input_controller.on_mouse_press(x, y, arcade.MOUSE_BUTTON_RIGHT)

    # Тут статик метод не из-за нейронки, а из-за того что pycharm ругался
    @staticmethod
    def _draw_health_bar(unit):
        """Рисует HP бар над юнитом"""
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
        """Отрисовка статистики юнитов"""
        for unit in self.game_state.units:
            self._draw_health_bar(unit)

            # Линия движения
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

    def _update_camera(self, delta_time):
        """Управление камерой: WASD + края экрана + зум"""

        # Движение WASD
        keys = self.window.keyboard
        dx, dy = 0, 0

        if keys[arcade.key.W]: dy += self.camera_speed * delta_time
        if keys[arcade.key.S]: dy -= self.camera_speed * delta_time
        if keys[arcade.key.A]: dx -= self.camera_speed * delta_time
        if keys[arcade.key.D]: dx += self.camera_speed * delta_time

        # Движение к краям экрана мышью (просто ради удобства пользователя (такая же штука есть в HOI4
        mouse_x, mouse_y = self.window.mouse["x"], self.window.mouse["y"]
        edge = 20


        if mouse_x < edge:
            dx -= self.camera_speed * delta_time
        elif mouse_x > self.window.width - edge:
            dx += self.camera_speed * delta_time
        if mouse_y < edge:
            dy -= self.camera_speed * delta_time
        elif mouse_y > self.window.height - edge:
            dy += self.camera_speed * delta_time

        # Применить движение камеры
        self.camera.position = (
            self.camera.position[0] + dx,
            self.camera.position[1] + dy
        )

        # Ограничить границами(пока что только для fullscreen)
        hw = self.window.width / 2 / self.camera_zoom
        hh = self.window.height / 2 / self.camera_zoom

        self.camera.position = (
            max(hw, min(self.camera.position[0], self.map_width - hw)),
            max(hh, min(self.camera.position[1], self.map_height - hh))
        )

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        """Зум колесиком"""
        # сделано тк модельки юнитов малы, а саму штуку реализовать очень просто было
        if scroll_y > 0:
            self.camera_zoom = min(2.0, self.camera_zoom + 0.1)
        else:
            self.camera_zoom = max(0.5, self.camera_zoom - 0.1)

        self.camera.zoom = self.camera_zoom