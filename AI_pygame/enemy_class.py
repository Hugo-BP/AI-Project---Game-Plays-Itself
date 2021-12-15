from config import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, sprite_class, x, y):
        pygame.sprite.Sprite.__init__(self)

        # AI places of interest
        self.is_player = False
        self.is_enemy = True
        self.is_building = False
        self.is_bonus = False

        # save instance of game
        self.game = game
        # coords
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE

        # movement change
        self.x_movement = 0
        self.y_movement = 0

        # frame counter, for fps
        self.frame = 0

        # texture lists
        self.idle_textures = []

        # state flags
        self.dead = False

        # sprite lists
        self.all_sprites = game.all_sprites
        self.players = game.player_sprites
        self.blocks = game.block_sprites
        self.buildings = game.building_sprites
        self.enemies = game.enemy_sprites
        self.bonus = game.bonus_sprites
        self.required_to_win = game.required_to_win

        # attacked by which players?
        self.tagged = []

        """
        npc stats
        """
        # sprite_class type
        self.sprite_class = sprite_class
        # xp reward
        self.exp = available_enemy_classes.get(sprite_class)[2]
        # health
        self.health = available_enemy_classes.get(sprite_class)[0]
        self.max_health = available_enemy_classes.get(sprite_class)[0]
        # power
        self.pow = available_enemy_classes.get(sprite_class)[1]

        # load textures
        for i in range(0, 2):
            img = pygame.image.load("sprites/" + sprite_class + "_" + str(i) + ".PNG").convert_alpha()
            self.idle_textures.append(img)
            self.image = self.idle_textures[0]
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

    """
    clean NPC and free memory
    """
    def die(self):
        if self.sprite_class == 'necromancer':
            print('Necromancer > Curse you all! ARRGGG...!!')
            self.game.required_to_win.remove(self)
            self.required_to_win.remove(self)
            required_to_win_list.remove(self)

            n = 0
            c = 0
            for sprite in self.required_to_win:
                if sprite.sprite_class == 'necromancer':
                    n += 1
                elif sprite.sprite_class == 'evil_castle':
                    c += 1
            print('...There are still ' + str(n) + ' Necromancers on the loose and ' + str(c) + ' Evil Castles full of undead...')

        self.dead = True

        enemy_sprites_list.remove(self)
        all_sprites_list.remove(self)
        self.all_sprites.remove(self)
        self.game.all_sprites.remove(self)
        self.game.enemy_sprites.remove(self)
        self.kill()

    """
    NPC died, grant exp
    """
    def give_exp(self, players):
        print("\n")
        for player in players:
            player.exp += self.exp
            player.current_action_reward += self.exp
            print(player.name + " fought " + str(self.sprite_class) + " and gained " + str(
                self.exp) + " exp. Total exp is " + str(player.exp) + '.')
        print("\n")

    """
    Sprite Position 
    """
    def movement(self):
        """
        ANIMATIONS
        """
        # idle
        self.frame += 1
        if self.frame > 1:
            self.frame = 0
        self.image = self.idle_textures[self.frame]

    """
    Update events, movement, state
    """
    def update(self):
        """
        Update health
        """
        if self.health > 0:
            self.movement()

        elif self.health <= 0:
            self.give_exp(list(dict.fromkeys(self.tagged)))
            self.die()


