from config import *

class Biome(pygame.sprite.Sprite):
    def __init__(self, game, x, y, img):
        # save instance of game
        self.game = game

        # coords
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE

        # state flags
        self.gathered = False

        # sprite lists
        self.all_sprites = game.all_sprites

        # textures
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE

        pygame.sprite.Sprite.__init__(self)



