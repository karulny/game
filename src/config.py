"""
Конфигурация игры - все константы и настройки
"""
import os

# Базовая директория проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Пути к ресурсам
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")
MAPS_DIR = os.path.join(ASSETS_DIR, "maps")

# Настройки окна
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "RTS Prototype"

# Карта
MAP_PATH = os.path.join(MAPS_DIR, "map.tmx")
TILE_SCALING = 1

# Юниты
UNIT_SPEED = 120
UNIT_RADIUS = 12
UNIT_HP = 100
UNIT_DAMAGE = 10
UNIT_ATTACK_RANGE = 60
UNIT_ATTACK_DELAY = 1.0
UNIT_AGGRO_RANGE = 100

# Команды
PLAYER_TEAM = 1
ENEMY_TEAM = 0

# Пути к спрайтам
CROSSBOWMEN_SPRITESHEET = os.path.join(IMAGES_DIR, "units", "crossbowmen.png")
SPRITE_SIZE = 32
SPRITE_SCALE = 2.0

# Анимация
ANIMATION_SPEED = 0.1
WALK_FRAMES = (0, 3)
ATTACK_FRAMES = (4, 6)

# Экономика
STARTING_MONEY = 200
UNIT_COST = 50
MONEY_PER_SECOND = 10  # Пассивный доход