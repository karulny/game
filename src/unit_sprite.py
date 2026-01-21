"""
Спрайт юнита - визуальное представление
"""
import arcade
from unit import UnitState

PLAYER_ID = 1


class UnitSprite(arcade.Sprite):
    """Визуальное представление юнита с анимацией"""

    def __init__(self, model, textures):
        super().__init__()
        self.model = model
        self.textures = textures
        self.texture = textures[0]
        self.scale = 1.0

        # Анимация
        self.current_texture = 0
        self.animation_speed = 0.1
        self.time_since_last_frame = 0

    def sync_from_model(self):
        """Синхронизация визуала с моделью"""
        if self.model.team == PLAYER_ID:
            self.color = arcade.color.LIGHT_GREEN
        else:
            self.color = arcade.color.RED

    def update(self, delta_time):
        """Обновление позиции и анимации"""
        # Синхронизация позиции
        self.center_x = self.model.x
        self.center_y = self.model.y

        # Удаление при смерти
        if self.model.hp <= 0:
            self.remove_from_sprite_lists()

        # Анимация в зависимости от состояния
        if self.model.state == UnitState.MOVE:
            self._animate(delta_time, 0, 3)
        elif self.model.state == UnitState.ATTACK:
            self._animate(delta_time, 4, 6)
        else:
            self.current_texture = 0
            self.texture = self.textures[0]

        self.sync_from_model()

    def _animate(self, delta_time, start_frame, end_frame):
        """Простая анимация по кадрам"""
        self.time_since_last_frame += delta_time

        if self.time_since_last_frame > self.animation_speed:
            self.time_since_last_frame = 0
            self.current_texture += 1

            if self.current_texture > end_frame:
                self.current_texture = start_frame

            self.texture = self.textures[self.current_texture]