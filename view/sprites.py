import math
import arcade


class Unit(arcade.Sprite):
    def __init__(self, x, y, texture_list, scale=2.0):
        super().__init__(texture_list[0], scale=scale)
        self.center_x = x
        self.center_y = y
        self.textures = texture_list
        # Целевые координаты для движения
        self.target_x = x
        self.target_y = y
        self.speed = 150.0

    def move(self, target_x, target_y):
        """Устанавливает новую точку назначения"""
        self.target_x = target_x
        self.target_y = target_y

    def update(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        # Вычисляем вектор до цели
        dist_x = self.target_x - self.center_x
        dist_y = self.target_y - self.center_y
        distance = math.sqrt(dist_x ** 2 + dist_y ** 2)

        # Если мы еще не дошли до цели (с учетом погрешности)
        if distance > 2.0:
            # Нормализуем вектор и умножаем на скорость и время
            self.change_x = (dist_x / distance) * self.speed
            self.change_y = (dist_y / distance) * self.speed

            self.center_x += self.change_x * delta_time
            self.center_y += self.change_y * delta_time
        else:
            # Останавливаемся точно в цели
            self.change_x = 0
            self.change_y = 0
            self.center_x = self.target_x
            self.center_y = self.target_y