from config import *
import random

class Friend(pygame.sprite.Sprite):
    def __init__(self, game, sprite_class, x, y):
        pygame.sprite.Sprite.__init__(self)

        # AI places of interest
        self.is_player = False
        self.is_enemy = False
        self.is_building = False
        self.is_bonus = True

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
        self.gathered = False

        # sprite lists
        self.all_sprites = game.all_sprites
        self.players = game.player_sprites
        self.blocks = game.block_sprites
        self.buildings = game.building_sprites
        self.enemies = game.enemy_sprites
        self.bonus = game.bonus_sprites

        """
        npc stats
        """
        # sprite_class type
        self.sprite_class = sprite_class
        # xp reward
        self.exp = available_bonus_classes.get(sprite_class)[2]
        # health reward
        self.health = available_bonus_classes.get(sprite_class)[0]
        # power reward
        self.pow = available_bonus_classes.get(sprite_class)[1]

        # load textures
        for i in range(0, 2):
            img = pygame.image.load("sprites/" + sprite_class + "_" + str(i) + ".PNG").convert_alpha()
            self.idle_textures.append(img)
            self.image = self.idle_textures[0]
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

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
        Update animation
        """
        self.movement()

    """
    Gather AUX RANDOM
    """
    def demon_choice(self, player, choice):
        if choice == 'help':
            player.max_health += self.health
            player.health = player.max_health
            player.exp += self.exp
            player.pow += self.pow
            player.current_action_reward = self.exp
            print(
                '\n The grumpy demon gave you an amulet! It makes you feel weird... It seems he really dislikes Necromancers as well...\n')
            print(player.name + ' > Health Stat: ' + str(player.max_health - self.health) + '-->' + str(
                player.max_health))
            print(player.name + ' > Power Stat: ' + str(player.pow - self.pow) + '-->' + str(player.pow))
            print(player.name + ' > Health: ' + str(player.health) + '/' + str(player.max_health))
            print(player.name + ' > Total Exp: ' + str(player.exp))
            print(player.name + ' > Its better to leave him alone now... before he gets even grumpier...')
        elif choice == 'kill':
            player.exp += 1
            player.health -= 25
            player.pow -= 1
            player.current_action_reward += int(self.exp / 10)
            print('\n The grumpy demon cursed you!\n')
            print(player.name + ' > OUTCH!')
            print(player.name + ' > Power Stat: ' + str(player.pow + 1) + '-->' + str(player.pow))
            print(player.name + ' > Health: ' + str(player.health) + '/' + str(player.max_health))
            if player.health <= 0:
                print(player.name + ' > oof!')
                player.die()
            else:
                print(player.name + ' > Its better to leave him alone now... before he gets even grumpier...')

    """
    Gather Rewards or get rekd by a demon
    """
    def gather(self, player):
        self.gathered = True
        if self.sprite_class == 'villager':
            player.max_health += self.health
            player.health = player.max_health
            player.exp += self.exp
            player.pow += self.pow
            player.current_action_reward += self.exp
            print(player.name + ' > Found a Villager girl! She needed some help... She gave gave me some herbs and fruits.')
            print(player.name + ' > Health Stat: ' + str(player.max_health - self.health) + '-->' + str(player.max_health))
            print(player.name + ' > Power Stat: ' + str(player.pow-self.pow) + '-->' + str(player.pow))
            print(player.name + ' > Health: ' + str(player.health) + '/' + str(player.max_health))
            print(player.name + ' > Total Exp: ' + str(player.exp))

        elif self.sprite_class == 'gnome':
            player.max_health += self.health
            player.health = player.max_health
            player.exp += self.exp
            player.pow += self.pow
            player.current_action_reward += self.exp
            print(player.name + ' > Found a tree gnome! He gave me a magic spell.')
            print(player.name + ' > Health Stat: ' + str(player.max_health - self.health) + '-->' + str(player.max_health))
            print(player.name + ' > Power Stat: ' + str(player.pow-self.pow) + '-->' + str(player.pow))
            print(player.name + ' > Health: ' + str(player.health) + '/' + str(player.max_health))
            print(player.name + ' > Total Exp: ' + str(player.exp))

        elif self.sprite_class == 'faery':
            player.max_health += self.health
            player.health = player.max_health
            player.exp += self.exp
            player.pow += self.pow
            player.current_action_reward += self.exp
            print(player.name + ' > Found a Faerie! She looks very cute. She seems to have blessed me? Shes very cheerful...')
            print(player.name + ' > Health Stat: ' + str(player.max_health - self.health) + '-->' + str(player.max_health))
            print(player.name + ' > Power Stat: ' + str(player.pow-self.pow) + '-->' + str(player.pow))
            print(player.name + ' > Health: ' + str(player.health) + '/' + str(player.max_health))
            print(player.name + ' > Total Exp: ' + str(player.exp))

        elif self.sprite_class == 'demon':
            possibilities = ['kill', 'help']
            print(player.name + ' > Found a Demon! He looks very grumpy... Better be careful!')
            print('\n The grumpy Demon stares at you...\n')
            if player.sprite_class == 'priest':
                print('Grumpy Demon > Grrr...')
                choice = random.choices([0, 1], weights=(80, 20), k=1)
                self.demon_choice(player, possibilities[choice[0]])
            elif player.sprite_class == 'wizard':
                print('Grumpy Demon > Hehe...')
                choice = random.choices([0, 1], weights=(20, 80), k=1)
                self.demon_choice(player, possibilities[choice[0]])
            else:
                print('Grumpy Demon > Hmmm...')
                choice = random.choices([0, 1], weights=(50, 50), k=1)
                self.demon_choice(player, possibilities[choice[0]])










