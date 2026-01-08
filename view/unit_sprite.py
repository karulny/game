import arcade

class UnitSprite(arcade.Sprite):
    def __init__(self, model, textures):
        super().__init__()
        self.model = model
        self.textures = textures
        self.texture = textures[0]
        self.scale = 2.0

    def sync_from_model(self, is_selected=False):
        self.center_x = self.model.x
        self.center_y = self.model.y

        if is_selected:
            self.color = arcade.color.GREEN
        else:
            self.color = arcade.color.WHITE
