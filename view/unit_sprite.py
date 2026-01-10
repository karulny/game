import arcade

PLAYER_ID = 1

class UnitSprite(arcade.Sprite):
    def __init__(self, model, textures):
        super().__init__()
        self.model = model
        self.textures = textures
        self.texture = textures[0]
        self.scale = 2.0

    def sync_from_model(self, ):
        if self.model.owner_id == PLAYER_ID:
            self.color = arcade.color.WHITE
        else:
            self.color = arcade.color.RED