import arcade
from view.game_view import GameView

def main():
    window = arcade.Window(1920, 1080, "RTS Prototype") # Размеры из config.py
    game_view = GameView()
    game_view.setup()
    window.show_view(game_view)
    arcade.run() # Запуск цикла игры

if __name__ == "__main__":
    main()