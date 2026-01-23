import arcade
from unit_sprite import UnitSprite
from unit import Unit, UnitState
from config import CROSSBOWMEN_SPRITESHEET, UNIT_COST, PLAYER_TEAM
from enemy_ai import EnemyAI


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

        # Границы карты
        self.map_width = tile_map.width * tile_map.tile_width * tile_map.scaling
        self.map_height = tile_map.height * tile_map.tile_height * tile_map.scaling

        # Сцена
        self.scene = arcade.Scene.from_tilemap(tile_map)

        # Юниты
        self.unit_sprites = arcade.SpriteList()
        self.scene.add_sprite_list("Units", sprite_list=self.unit_sprites)

        # UI камера (для интерфейса)
        self.ui_camera = arcade.camera.Camera2D()

        # Текстуры для юнитов
        spritesheet = arcade.load_spritesheet(CROSSBOWMEN_SPRITESHEET)
        self.unit_textures = spritesheet.get_texture_grid(
            size=(32, 32),
            columns=4,
            count=7,
            hit_box_algorithm=arcade.hitbox.algo_detailed
        )

        # AI противника (НОВОЕ!)
        self.enemy_ai = EnemyAI(game_state)

        self.setup()

    def setup(self):
        """Создание Sprite для каждой модели"""
        for unit_model in self.game_state.units:
            sprite = UnitSprite(unit_model, self.unit_textures)
            self.unit_sprites.append(sprite)

    def on_draw(self):
        """Отрисовка игры"""
        self.clear()

        # Рисуем игровой мир
        self.camera.use()
        self.scene.draw()
        self._draw_unit_stats()
        self._draw_buildings()

        # Рисуем UI поверх всего
        self.ui_camera.use()
        self._draw_ui()

    def on_update(self, delta_time):
        """Обновление логики игры"""
        self._update_camera(delta_time)
        self.game_state.update(delta_time)

        # Обновляем AI противника (НОВОЕ!)
        self.enemy_ai.update(delta_time, self.unit_textures, self.unit_sprites)

        # Удаляем мертвых
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
        """Обработка ЛКМ - выбор юнита или клик по зданию"""
        # Сначала проверяем клик по зданию
        clicked_building = self._get_building_at(x, y)

        if clicked_building and clicked_building.owner == "player":
            # Попытка спавнить юнита
            self._try_spawn_unit(clicked_building)
            return

        # Если не попали по зданию, проверяем юнитов
        clicked_unit = None

        for unit_model in self.game_state.units:
            dx = x - unit_model.x
            dy = y - unit_model.y
            dist = (dx * dx + dy * dy) ** 0.5

            if dist <= unit_model.radius:
                clicked_unit = unit_model
                break

        if clicked_unit:
            # Выбираем только своих юнитов
            if clicked_unit.team == PLAYER_TEAM:
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
            if unit_model.team == PLAYER_TEAM:
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

    def _get_building_at(self, x: float, y: float):
        """Получить здание в точке клика"""
        for building in self.game_state.buildings:
            # Проверяем попадание в область здания (примерно 32x32 пикселя)
            dx = abs(x - building.world_x)
            dy = abs(y - building.world_y)

            if dx < 32 and dy < 32:
                return building
        return None

    def _try_spawn_unit(self, building):
        """Попытка создать юнита в здании"""
        # Проверяем условия
        if not building.can_spawn():
            print("Здание на кулдауне!")
            return

        if not self.game_state.can_afford(UNIT_COST):
            print(f"Недостаточно денег! Нужно: {UNIT_COST}, есть: {self.game_state.money}")
            return

        # Тратим деньги
        self.game_state.spend_money(UNIT_COST)

        # Создаем юнита рядом со зданием
        spawn_x = building.world_x + 40
        spawn_y = building.world_y

        new_unit = Unit(spawn_x, spawn_y, team=PLAYER_TEAM)
        self.game_state.units.append(new_unit)

        # Создаем спрайт
        sprite = UnitSprite(new_unit, self.unit_textures)
        self.unit_sprites.append(sprite)

        # Запускаем кулдаун здания
        building.start_spawn()

        print(f"Юнит создан! Осталось денег: {self.game_state.money}")

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

    def _draw_buildings(self):
        """Отрисовка зданий с ПОЛУПРОЗРАЧНОЙ ЗАЛИВКОЙ"""
        for building in self.game_state.buildings:
            # Выбираем цвет в зависимости от владельца
            if building.owner == "player":
                outline_color = arcade.color.GREEN
                fill_color = (0, 255, 0, 80)  # Зеленый полупрозрачный
            elif building.owner == "enemy":
                outline_color = arcade.color.RED
                fill_color = (255, 0, 0, 80)  # Красный полупрозрачный
            else:
                outline_color = arcade.color.GRAY
                fill_color = (128, 128, 128, 80)  # Серый полупрозрачный

            # ЗАЛИВКА здания (полупрозрачная)
            arcade.draw_rectangle_filled(
                building.world_x, building.world_y,
                32, 32,
                fill_color
            )

            # ОБВОДКА здания (яркая)
            arcade.draw_rectangle_outline(
                building.world_x, building.world_y,
                32, 32,
                outline_color, 3  # Толще линия
            )

            # Показываем кулдаун
            if building.spawn_cooldown > 0:
                cooldown_text = f"{building.spawn_cooldown:.1f}s"
                arcade.draw_text(
                    cooldown_text,
                    building.world_x - 15, building.world_y + 20,
                    arcade.color.YELLOW, 10, bold=True
                )

    def _draw_ui(self):
        """Отрисовка интерфейса (деньги и статистика)"""
        # Фон панели
        arcade.draw_lrbt_rectangle_filled(
            0, 350, self.window.height - 80, self.window.height,
            (0, 0, 0, 200)  # Полупрозрачный черный
        )

        # Текст денег
        money_text = f"💰 Деньги: ${self.game_state.money}"
        arcade.draw_text(
            money_text,
            10, self.window.height - 30,
            arcade.color.GOLD, 20, bold=True
        )

        # Статистика юнитов рвди смеха смайлы прямо смешные брал
        player_units = len([u for u in self.game_state.units if u.team == 1])
        enemy_units = len([u for u in self.game_state.units if u.team == 0])

        stats_text = f"👥 Твои: {player_units}  |  🔴 Враги: {enemy_units}"
        arcade.draw_text(
            stats_text,
            10, self.window.height - 55,
            arcade.color.WHITE, 14
        )

        # Подсказка
        hint_text = "ЛКМ по 🟩 зданию = спавн юнита (50$)"
        arcade.draw_text(
            hint_text,
            10, self.window.height - 75,
            arcade.color.LIGHT_GRAY, 12
        )

    def _update_camera(self, delta_time):
        """Управление камерой: WASD + края экрана + зум"""
        keys = self.window.keyboard
        dx, dy = 0, 0

        if keys[arcade.key.W]: dy += self.camera_speed * delta_time
        if keys[arcade.key.S]: dy -= self.camera_speed * delta_time
        if keys[arcade.key.A]: dx -= self.camera_speed * delta_time
        if keys[arcade.key.D]: dx += self.camera_speed * delta_time

        # Движение к краям экрана мышью
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

        # Ограничить границами
        hw = self.window.width / 2 / self.camera_zoom
        hh = self.window.height / 2 / self.camera_zoom

        self.camera.position = (
            max(hw, min(self.camera.position[0], self.map_width - hw)),
            max(hh, min(self.camera.position[1], self.map_height - hh))
        )

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        """Зум колесиком"""
        if scroll_y > 0:
            self.camera_zoom = min(2.0, self.camera_zoom + 0.1)
        else:
            self.camera_zoom = max(0.5, self.camera_zoom - 0.1)

        self.camera.zoom = self.camera_zoom
