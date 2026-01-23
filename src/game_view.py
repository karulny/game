import arcade
from unit_sprite import UnitSprite
from unit import Unit, UnitState
from config import CROSSBOWMEN_SPRITESHEET, UNIT_COST, PLAYER_TEAM
from enemy_ai import EnemyAI
from save_system import SaveSystem


class GameView(arcade.View):
    def __init__(self, tile_map, game_state, game_model, input_controller):
        super().__init__()

        self.game_state = game_state
        self.game_map = game_model
        self.input_controller = input_controller

        self.camera = arcade.camera.Camera2D()
        self.camera_speed = 500
        self.camera_zoom = 1.0

        self.map_width = tile_map.width * tile_map.tile_width * tile_map.scaling
        self.map_height = tile_map.height * tile_map.tile_height * tile_map.scaling

        self.scene = arcade.Scene.from_tilemap(tile_map)

        self.unit_sprites = arcade.SpriteList()
        self.scene.add_sprite_list("Units", sprite_list=self.unit_sprites)

        self.ui_camera = arcade.camera.Camera2D()

        spritesheet = arcade.load_spritesheet(CROSSBOWMEN_SPRITESHEET)
        self.unit_textures = spritesheet.get_texture_grid(
            size=(32, 32),
            columns=4,
            count=7,
            hit_box_algorithm=arcade.hitbox.algo_detailed
        )

        self.enemy_ai = EnemyAI(game_state)
        self.save_system = SaveSystem()

        self.mouse_x = 0
        self.mouse_y = 0

        self.setup()

    def setup(self):
        for unit_model in self.game_state.units:
            sprite = UnitSprite(unit_model, self.unit_textures)
            self.unit_sprites.append(sprite)

    def on_draw(self):
        self.clear()

        self.camera.use()
        self.scene.draw()
        self._draw_unit_stats()

        self.ui_camera.use()
        self._draw_ui()

    def on_update(self, delta_time):
        self._update_camera(delta_time)
        self.game_state.update(delta_time)

        self.enemy_ai.update(delta_time, self.unit_textures, self.unit_sprites)

        self.game_state.units = [u for u in self.game_state.units if u.hp > 0]

        self.unit_sprites.update(delta_time)

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x
        self.mouse_y = y

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        world_x, world_y, world_z = self.camera.unproject((x, y))

        if button == arcade.MOUSE_BUTTON_LEFT:
            self._handle_left_click(world_x, world_y)
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            self._handle_right_click(world_x, world_y)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            from menu_view import PauseMenu
            pause_menu = PauseMenu(self)
            self.window.show_view(pause_menu)
        elif key == arcade.key.F5:
            self.save_system.save_game(
                self.game_state,
                self.camera.position,
                "quicksave"
            )
        elif key == arcade.key.F9:
            self._load_game()

    def _load_game(self):
        save_data = self.save_system.load_game()
        if not save_data:
            return

        self.game_state.money = save_data['money']

        self.game_state.units.clear()
        self.unit_sprites.clear()

        for unit_data in save_data['units_data']:
            unit = Unit(unit_data['x'], unit_data['y'], unit_data['team'])
            unit.hp = unit_data['hp']
            unit.state = UnitState(unit_data['state'])
            self.game_state.units.append(unit)

            sprite = UnitSprite(unit, self.unit_textures)
            self.unit_sprites.append(sprite)

        for i, building_data in enumerate(save_data['buildings_data']):
            if i < len(self.game_state.buildings):
                building = self.game_state.buildings[i]
                building.hp = building_data['hp']
                building.spawn_cooldown = building_data['spawn_cooldown']

        self.camera.position = (save_data['camera_x'], save_data['camera_y'])
        print("Игра загружена!")

    def _handle_left_click(self, x: int, y: int):
        clicked_building = self._get_building_at(x, y)

        if clicked_building and clicked_building.owner == "player":
            self._try_spawn_unit(clicked_building)
            return

        clicked_unit = None

        for unit_model in self.game_state.units:
            dx = x - unit_model.x
            dy = y - unit_model.y
            dist = (dx * dx + dy * dy) ** 0.5

            if dist <= unit_model.radius:
                clicked_unit = unit_model
                break

        if clicked_unit:
            if clicked_unit.team == PLAYER_TEAM:
                for sprite in self.unit_sprites:
                    if sprite.model == clicked_unit:
                        self.input_controller.select_unit(sprite)
                        break
        else:
            if self.input_controller.selected_unit:
                self.input_controller.selected_unit.color = arcade.color.WHITE
                self.input_controller.selected_unit = None
                self.game_state.selected_unit = None

    def _handle_right_click(self, x: int, y: int):
        if not self.input_controller.selected_unit:
            return

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
            selected_model = self.input_controller.selected_unit.model
            selected_model.target_enemy = clicked_enemy
            selected_model.state = UnitState.ATTACK
        else:
            self.input_controller.on_mouse_press(x, y, arcade.MOUSE_BUTTON_RIGHT)

    def _get_building_at(self, x: float, y: float):
        for building in self.game_state.buildings:
            dx = abs(x - building.world_x)
            dy = abs(y - building.world_y)

            if dx < 32 and dy < 32:
                return building
        return None

    def _try_spawn_unit(self, building):
        if not building.can_spawn():
            print("Здание на кулдауне!")
            return

        if not self.game_state.can_afford(UNIT_COST):
            print(f"Недостаточно денег! Нужно: {UNIT_COST}, есть: {self.game_state.money}")
            return

        self.game_state.spend_money(UNIT_COST)

        spawn_x = building.world_x + 40
        spawn_y = building.world_y

        new_unit = Unit(spawn_x, spawn_y, team=PLAYER_TEAM)
        self.game_state.units.append(new_unit)

        sprite = UnitSprite(new_unit, self.unit_textures)
        self.unit_sprites.append(sprite)

        building.start_spawn()

        print(f"Юнит создан! Осталось денег: {self.game_state.money}")

    @staticmethod
    def _draw_health_bar(unit):
        bar_width = 30
        bar_height = 4
        x = unit.x - bar_width / 2
        y = unit.y + unit.radius + 5

        arcade.draw_lrbt_rectangle_filled(
            x, x + bar_width,
               y - bar_height / 2, y + bar_height / 2,
            arcade.color.RED
        )

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

            elif unit.state == UnitState.ATTACK and unit.target_enemy:
                arcade.draw_line(
                    unit.x, unit.y,
                    unit.target_enemy.x, unit.target_enemy.y,
                    arcade.color.RED, 3
                )

            if self.game_state.selected_unit == unit:
                arcade.draw_circle_outline(
                    unit.x, unit.y,
                    unit.attack_range,
                    arcade.color.RED_ORANGE, 2
                )

    def _draw_ui(self):
        arcade.draw_lrbt_rectangle_filled(
            0, 400, self.window.height - 100, self.window.height,
            (0, 0, 0, 200)
        )

        money_text = f"💰 Деньги: ${self.game_state.money}"
        arcade.draw_text(
            money_text,
            10, self.window.height - 30,
            arcade.color.GOLD, 20, bold=True
        )

        player_units = len([u for u in self.game_state.units if u.team == 1])
        enemy_units = len([u for u in self.game_state.units if u.team == 0])

        stats_text = f"👥 Твои: {player_units}  |  🔴 Враги: {enemy_units}"
        arcade.draw_text(
            stats_text,
            10, self.window.height - 55,
            arcade.color.WHITE, 14
        )

        hint_text = "ЛКМ по зданию = спавн (50$) | ESC = меню | F5 = сохранить | F9 = загрузить"
        arcade.draw_text(
            hint_text,
            10, self.window.height - 80,
            arcade.color.LIGHT_GRAY, 11
        )

    def _update_camera(self, delta_time):
        keys = self.window.keyboard
        dx, dy = 0, 0

        if keys[arcade.key.W]: dy += self.camera_speed * delta_time
        if keys[arcade.key.S]: dy -= self.camera_speed * delta_time
        if keys[arcade.key.A]: dx -= self.camera_speed * delta_time
        if keys[arcade.key.D]: dx += self.camera_speed * delta_time

        edge = 20

        if self.mouse_x < edge:
            dx -= self.camera_speed * delta_time
        elif self.mouse_x > self.window.width - edge:
            dx += self.camera_speed * delta_time
        if self.mouse_y < edge:
            dy -= self.camera_speed * delta_time
        elif self.mouse_y > self.window.height - edge:
            dy += self.camera_speed * delta_time

        self.camera.position = (
            self.camera.position[0] + dx,
            self.camera.position[1] + dy
        )

        hw = self.window.width / 2 / self.camera_zoom
        hh = self.window.height / 2 / self.camera_zoom

        self.camera.position = (
            max(hw, min(self.camera.position[0], self.map_width - hw)),
            max(hh, min(self.camera.position[1], self.map_height - hh))
        )

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if scroll_y > 0:
            self.camera_zoom = min(2.0, self.camera_zoom + 0.1)
        else:
            self.camera_zoom = max(0.5, self.camera_zoom - 0.1)

        self.camera.zoom = self.camera_zoom