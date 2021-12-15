from config import *
import random

class Building(pygame.sprite.Sprite):
    def __init__(self, game, x, y, img, sprite_class, text, exp):

        # AI places of interest
        self.is_player = False
        self.is_enemy = False
        self.is_building = True
        self.is_bonus = False

        # save instance of game
        self.game = game
        # coords
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE

        # state flags
        self.gathered = False

        # sprite lists
        self.all_sprites = game.all_sprites
        self.required_to_win = game.required_to_win

        # Building type and player text when gathering
        self.sprite_class = sprite_class
        self.text = text
        self.exp = exp

        # textures
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE

        pygame.sprite.Sprite.__init__(self)

    """
    Return text when gathering
    """
    def get_text(self):
        if not self.gathered:
            return self.text
        else:
            self.text = 'There is nothing here anymore'

    """
    Gather AUX RANDOM
    """
    def cave_choice(self, player, choice):
        self.gathered = True
        if choice == 'lost':
            print('\n ' + player.name + ' found nothing...\n')
            player.exp += int(self.exp / 10)
            player.health -= 1
            player.current_action_reward += int(self.exp / 10)
            print(player.name + ' > Health: ' + str(player.health) + '/' + str(player.max_health))
            print(player.name + ' > Total Exp: ' + str(player.exp))
            print(player.name + ' > Its better to leave before I get hurt...')

        elif choice == 'treasure':
            print('\n ' + player.name + ' found an ancient ring, made to rule them all...\n')
            player.max_health += 25
            player.health = player.max_health
            player.exp += self.exp
            player.pow += 5
            player.current_action_reward += self.exp
            print('\n This ring looks enchanted... I wonder what will happen if I wear it...\n')
            print(player.name + ' > Health Stat: ' + str(player.max_health - 25) + '-->' + str(player.max_health))
            print(player.name + ' > Power Stat: ' + str(player.pow - 5) + '-->' + str(player.pow))
            print(player.name + ' > Health: ' + str(player.health) + '/' + str(player.max_health))
            print(player.name + ' > Total Exp: ' + str(player.exp))
            print(player.name + ' > Its better to leave before I get lost...')

        elif choice == 'attacked':
            print('\n ' + player.name + ' got attacked by monsters!\n')
            player.exp += self.exp * 2
            player.health = 1
            player.current_action_reward += self.exp * 2
            print(player.name + ' > OUTCH!')
            print(player.name + ' > Health: ' + str(player.health) + '/' + str(player.max_health))
            print(player.name + ' > Its better to leave before I get hurt AND lost!')

    """
    Gather Rewards
    """
    def gather(self, player):
        self.gathered = True
        if self.sprite_class == 'house':
            player.exp += self.exp
            player.health = player.max_health
            player.current_action_reward += self.exp
            print('\n ' + player.name + ' was healed by friendly villagers.\n')
            print(player.name + ' > Health: ' + str(player.health) + '/' + str(player.max_health))
       
        elif self.sprite_class == 'necro_house':
            player.exp += self.exp
            player.health = player.max_health
            player.current_action_reward += self.exp
            print('\n ' + player.name + ' found some abandoned supplies. The zombies wont need any healing...\n')
            print(player.name + ' > Health: ' + str(player.health) + '/' + str(player.max_health))

        elif self.sprite_class == 'castle':
            player.health -= 1
            print(player.name + ' > Health: ' + str(player.health) + '/' + str(player.max_health))

            player.exp += self.exp
            player.pow += 1
            player.max_health += 5
            player.current_action_reward += self.exp
            print('\n ' + player.name + ' was trained by veteran knights.\n')
            print(player.name + ' > Health Stat: ' + str(player.max_health - 5) + '-->' + str(player.max_health))
            print(player.name + ' > Power Stat: ' + str(player.pow - 1) + '-->' + str(player.pow))
            print(player.name + ' > Health: ' + str(player.health) + '/' + str(player.max_health))
            print(player.name + ' > Total Exp: ' + str(player.exp))

        elif self.sprite_class == 'evil_castle':
            self.game.required_to_win.remove(self)
            self.required_to_win.remove(self)
            required_to_win_list.remove(self)

            player.health -= 10
            print(player.name + ' > Health: ' + str(player.health) + '/' + str(player.max_health))

            player.exp += self.exp
            player.pow += 1
            player.max_health += 5
            player.current_action_reward += self.exp
            print('\n ' + player.name + ' fights off a horde of undead.\n')
            print(player.name + ' > Health Stat: ' + str(player.max_health - 5) + '-->' + str(player.max_health))
            print(player.name + ' > Power Stat: ' + str(player.pow - 1) + '-->' + str(player.pow))
            print(player.name + ' > Health: ' + str(player.health) + '/' + str(player.max_health))
            print(player.name + ' > Total Exp: ' + str(player.exp))
            if self.sprite_class == 'evil_castle':
                print(' The castle lays in ruins.')
                n = 0
                c = 0
                for sprite in self.required_to_win:
                    if sprite.sprite_class == 'necromancer':
                        n += 1
                    elif sprite.sprite_class == 'evil_castle':
                        c += 1
                print('...There are still ' + str(n) + ' Necromancers on the loose and ' + str(
                    c) + ' Evil Castles full of undead...')

        elif self.sprite_class == 'faery_house':
            player.health = player.max_health
            player.exp += self.exp
            player.current_action_reward += self.exp
            print('\n ' + player.name + ' rested at the faery house.\n')
            print(player.name + ' > Health: ' + str(player.health) + '/' + str(player.max_health))
            print(player.name + ' > Total Exp: ' + str(player.exp))

        elif self.sprite_class == 'stone_cross':
            player.exp += self.exp
            player.health = player.max_health
            player.current_action_reward += self.exp
            print('\n ' + player.name + ' found an ancient Milestone!\n')
            print(player.name + ' > Health: ' + str(player.health) + '/' + str(player.max_health))
            print(player.name + ' > Total Exp: ' + str(player.exp))

        elif self.sprite_class == 'cave':
            possibilities = ['lost', 'treasure', 'attacked']
            print('\n ' + player.name + ' found a cave!\n')
            choice = random.choices([0, 1, 2], weights=(50, 30, 20), k=1)
            self.cave_choice(player, possibilities[choice[0]])

        elif self.sprite_class == 'cactus':
            player.exp += self.exp
            player.health += 1
            player.current_action_reward += self.exp
            print('\n ' + player.name + ' drank some cactus water.\n')
            print(player.name + ' > Health: ' + str(player.health) + '/' + str(player.max_health))
            print(player.name + ' > Total Exp: ' + str(player.exp))

        else:
            player.exp += self.exp
            player.current_action_reward += self.exp
