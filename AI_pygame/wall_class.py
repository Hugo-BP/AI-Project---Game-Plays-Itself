from config import *

class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y, text):
        # save instance of game
        self.game = game

        # coords
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE

        # state flags
        self.gathered = False

        # sprite lists
        self.all_sprites = game.all_sprites

        # Player text when collision
        self.text = text

        # textures
        self.image = pygame.image.load("buildings/invisible_wall.PNG").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        pygame.sprite.Sprite.__init__(self)












