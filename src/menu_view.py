"""
Главное меню игры
"""
import arcade


class MenuView(arcade.View):
    """Представление главного меню"""

    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_show_view(self):
        """Вызывается при переключении на это представление"""
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

    def on_draw(self):
        """Отрисовка меню"""
        self.clear()

        arcade.draw_text(
            "RTS СТРАТЕГИЯ",
            self.window.width / 2,
            self.window.height / 2 + 50,
            arcade.color.WHITE,
            font_size=50,
            anchor_x="center"
        )

        arcade.draw_text(
            "Нажми ENTER, чтобы начать",
            self.window.width / 2,
            self.window.height / 2 - 50,
            arcade.color.GRAY,
            font_size=20,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        """Обработка нажатий клавиш"""
        if key == arcade.key.ENTER:
            self.window.show_view(self.game_view)