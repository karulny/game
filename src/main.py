"""
RTS Prototype - Точка входа приложения
"""
import arcade
from game import Game
from config import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE



def main():
    """Инициализация и запуск игры"""
    window = arcade.Window(
        width=SCREEN_WIDTH,
        height=SCREEN_HEIGHT,
        title=SCREEN_TITLE,
        resizable=True,
        fullscreen=True
    )

    game = Game(window)
    game.setup()

    arcade.run()


if __name__ == "__main__":
    main()