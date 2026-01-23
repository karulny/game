import arcade


class MenuView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

    def on_draw(self):
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

        arcade.draw_text(
            "ESC - выход",
            self.window.width / 2,
            self.window.height / 2 - 80,
            arcade.color.GRAY,
            font_size=16,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            self.window.show_view(self.game_view)
        elif key == arcade.key.ESCAPE:
            arcade.exit()


class PauseMenu(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_show_view(self):
        arcade.set_background_color((0, 0, 0, 150))

    def on_draw(self):
        self.game_view.on_draw()

        arcade.draw_lbwh_rectangle_filled(
            0, self.window.width,
            self.window.height, 0,
            (0, 0, 0, 180)
        )

        arcade.draw_text(
            "ПАУЗА",
            self.window.width / 2,
            self.window.height / 2 + 80,
            arcade.color.WHITE,
            font_size=50,
            anchor_x="center"
        )

        arcade.draw_text(
            "ESC - продолжить",
            self.window.width / 2,
            self.window.height / 2,
            arcade.color.LIGHT_GRAY,
            font_size=20,
            anchor_x="center"
        )

        arcade.draw_text(
            "Q - выход в меню",
            self.window.width / 2,
            self.window.height / 2 - 40,
            arcade.color.LIGHT_GRAY,
            font_size=20,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.game_view)
        elif key == arcade.key.Q:
            from game import Game
            game = Game(self.window)
            game.setup()