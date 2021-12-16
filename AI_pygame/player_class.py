from config import *
import random


class Player(pygame.sprite.Sprite):
    def __init__(self, game, sprite_class, x, y, name):
        pygame.sprite.Sprite.__init__(self)
        # AI
        self.individual_score = 0
        self.current_action_reward = 0
        self.direction = ''
        self.is_healer = False
        self.is_fighting = False
        """
        self.is_blockedL = False
        self.is_blockedR = False
        self.is_blockedU = False
        self.is_blockedD = False
        """

        # places of interest MAX = 50
        self.places_of_interest = []
        self.is_player = True
        self.is_enemy = False
        self.is_building = False
        self.is_bonus = False

        # save instance of game
        self.game = game

        # initial coords - use rect.x to get current coords
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE

        # movement change
        self.x_movement = 0
        self.y_movement = 0

        # frame counter, for fps
        self.frame = 0

        # texture lists
        self.idle_textures = []
        self.movement_textures = []
        self.attack_textures = []

        # movement flags
        self.walking_down = False
        self.walking_right = True

        # state flags, also used in AI
        self.is_alive = True
        self.final_level = False  # final level

        # sprite lists
        self.all_sprites = game.all_sprites
        self.players = game.player_sprites
        self.blocks = game.block_sprites
        self.buildings = game.building_sprites
        self.enemies = game.enemy_sprites
        self.bonus = game.bonus_sprites


        """
        player stats
        """
        # player name
        self.name = name
        # sprite_class type
        self.sprite_class = sprite_class
        # xp starts at 0
        self.exp = 0
        # health
        self.health = available_player_classes.get(sprite_class)[0]
        self.max_health = available_player_classes.get(sprite_class)[0]
        # power
        self.pow = available_player_classes.get(sprite_class)[1]
        # how far the AI agent can see
        self.view_range = available_player_classes.get(sprite_class)[2]

        # load textures
        for i in range(0, 2):
            img = pygame.image.load("sprites/" + sprite_class + "_" + str(i) + ".PNG").convert_alpha()
            self.idle_textures.append(img)
            self.image = self.idle_textures[0]
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

    """
    Invisible Wall Collisions and Building Collisions - mountains and water
    Enemy NPC collisions and Combat
    Friend NPC collisions and Gathering
    """

    def collisions(self, direction):
        self.is_fighting = False

        biomes_blocked = pygame.sprite.spritecollide(self, self.blocks, False)
        building = pygame.sprite.spritecollide(self, self.buildings, False)
        bonus = pygame.sprite.spritecollide(self, self.bonus, False)
        enemies = pygame.sprite.spritecollide(self, self.enemies, False)
        players = pygame.sprite.spritecollide(self, self.players, False)

        if self.sprite_class == 'priest':
            if players:
                for player in players:
                    if player != self and player.health < player.max_health:
                        player.health += self.pow * 2
                        self.exp += 1
                        # reward healing
                        self.current_action_reward += self.pow * 2
                        print(self.name + " healed " + str(player.name) + ' --> ' + str(player.health) + "/" + str(
                            player.max_health))

        if bonus:
            if not bonus[0].gathered:
                bonus[0].gather(self)

        if building:
            if not building[0].gathered:
                print(self.name + ' > ' + building[0].text)
                building[0].gather(self)

        if biomes_blocked:
            # punish trying to swim or climb mountains
            self.current_action_reward -= 2
            for blocked in biomes_blocked:
                if direction == 'x':
                    # right
                    if self.x_movement > 0:
                        #self.is_blockedR = True
                        self.rect.x = blocked.rect.left - self.rect.width
                        print(self.name + ' > ' + blocked.text)
                    # left
                    elif self.x_movement < 0:
                        #self.is_blockedL = True
                        self.rect.x = blocked.rect.right
                        print(self.name + ' > ' + blocked.text)

                elif direction == 'y':
                    # down
                    if self.y_movement > 0:
                        #self.is_blockedD = True
                        self.rect.y = blocked.rect.top - self.rect.height
                        print(self.name + ' > ' + blocked.text)
                    # up
                    elif self.y_movement < 0:
                        #self.is_blockedU = True
                        self.rect.y = blocked.rect.bottom
                        print(self.name + ' > ' + blocked.text)
                self.x_movement = 0
                self.y_movement = 0

        if enemies:
            self.is_fighting = True
            if direction == 'x':
                if self.x_movement > 0:
                    self.rect.x = enemies[0].rect.left - self.rect.width
                elif self.x_movement < 0:
                    self.rect.x = enemies[0].rect.right

            elif direction == 'y':
                if self.y_movement > 0:
                    self.rect.y = enemies[0].rect.top - self.rect.height
                elif self.y_movement < 0:
                    self.rect.y = enemies[0].rect.bottom
            self.x_movement = 0
            self.y_movement = 0

            for enemy in enemies:
                enemy.tagged.append(self)
                # attack
                enemy.health -= self.pow
                self.current_action_reward += 2
                print(enemy.sprite_class + " > " + str(enemy.health) + "/" + str(enemy.max_health))
                # defend
                if not enemy.dead:
                    self.health -= enemy.pow
                    print(self.name + " > " + str(self.health) + "/" + str(self.max_health))


    def update_interests(self):
        self.places_of_interest.clear()
        self.places_of_interest = []

        # coordinates are in factors of TILE_SIZE, range is not.
        # the following code has values of : player coords = (224,192) max_range = 32
        max_range = self.view_range * TILE_SIZE
        x = self.rect.x
        y = self.rect.y

        for sprite in self.buildings:
            if (x + max_range) >= sprite.x >= (x - max_range) and (
                    y + max_range) >= sprite.y >= (y - max_range) and not sprite.gathered:
                self.places_of_interest.append(sprite)

        for sprite in self.bonus:
            if (x + max_range) >= sprite.x >= (x - max_range) and (
                    y + max_range) >= sprite.y >= (y - max_range) and not sprite.gathered:
                self.places_of_interest.append(sprite)

        for sprite in self.enemies:
            if (x + max_range) >= sprite.x >= (x - max_range) and (
                    y + max_range) >= sprite.y >= (y - max_range):
                self.places_of_interest.append(sprite)

        for sprite in self.players:
            if sprite != self and (x + max_range) >= sprite.x >= (x - max_range) and (
                    y + max_range) >= sprite.y >= (y - max_range):
                self.places_of_interest.append(sprite)

        """
        self.is_blockedR = False
        self.is_blockedL = False
        self.is_blockedU = False
        self.is_blockedD = False
        for block in self.blocks:
            if x + TILE_SIZE == block.x and (block.y == y or block.y == y+SPEED or block.y == y-SPEED):
                self.is_blockedL = True

            if x - TILE_SIZE == block.x and (block.y == y or block.y == y+SPEED or block.y == y-SPEED):
                self.is_blockedR = True

            if (block.x == x or block.x == x+SPEED or block.x == x-SPEED) and block.y == y + TILE_SIZE:
                self.is_blockedD = True

            if (block.x == x or block.x == x+SPEED or block.x == x-SPEED) and block.y == y - TILE_SIZE:
                self.is_blockedU = True
        """
        # print(self.name + ' found: ' + sprite.sprite_class + '(' + str(round(sprite.x/TILE_SIZE)) + ' : ' + str(round(sprite.y/TILE_SIZE)) + ')')

    def check_boundaries(self, pt):
        if pt in self.game.boundaries:
            return True


    def update_movement_textures_and_collisions(self):
        # update x plane
        self.rect.x += self.x_movement
        # x plane collision checks
        self.collisions('x')
        # update y plane
        self.rect.y += self.y_movement
        # y plane collision checks
        self.collisions('y')

        """
        ANIMATIONS
        """
        # moving left
        if self.x_movement < 0:
            if self.walking_right:
                for i in range(0, 2):
                    self.idle_textures[i] = pygame.transform.flip(self.idle_textures[i], True, False)
                self.walking_right = False

            self.frame += 1
            if self.frame > 1:
                self.frame = 0
            self.image = self.idle_textures[self.frame]

        # moving right
        elif self.x_movement > 0:
            if not self.walking_right:
                for i in range(0, 2):
                    self.idle_textures[i] = pygame.transform.flip(self.idle_textures[i], True, False)
                self.walking_right = True

            self.frame += 1
            if self.frame > 1:
                self.frame = 0
            self.image = self.idle_textures[self.frame]

        # moving up
        elif self.y_movement < 0:
            self.frame += 1
            if self.frame > 1:
                self.frame = 0
            self.image = self.idle_textures[self.frame]

        # moving down
        elif self.y_movement > 0:
            self.frame += 1
            if self.frame > 1:
                self.frame = 0
            self.image = self.idle_textures[self.frame]

        # reset movement values after theyre used for calculating collisions, position, and updating textures
        self.y_movement = 0
        self.x_movement = 0

        # DEFAULT ANIMATION
        self.frame += 1
        if self.frame > 1:
            self.frame = 0
        self.image = self.idle_textures[self.frame]

    # Player keyboard controls
    def player_movement(self, direction):
        self.direction = direction
        if direction == 0:  # A left
            self.x_movement -= SPEED
            self.y_movement = 0
           # if self.is_blockedR or self.is_blockedU or self.is_blockedD:
           #     self.is_blockedR = False
           #     self.is_blockedU = False
           #     self.is_blockedD = False
        elif direction == 1:  # D right
            self.x_movement += SPEED
            self.y_movement = 0
          #  if self.is_blockedL or self.is_blockedU or self.is_blockedD:
           #     self.is_blockedL = False
           #     self.is_blockedU = False
            #    self.is_blockedD = False
        elif direction == 2:  # W up
            self.y_movement -= SPEED
            self.x_movement = 0
           # if self.is_blockedL or self.is_blockedR or self.is_blockedD:
            #    self.is_blockedL = False
            #    self.is_blockedR = False
            #    self.is_blockedD = False
        elif direction == 3:  # S down
            self.y_movement += SPEED
            self.x_movement = 0
           # if self.is_blockedL or self.is_blockedR or self.is_blockedU:
            #    self.is_blockedL = False
             #   self.is_blockedR = False
             #   self.is_blockedU = False


    """
    clean Player and free memory
    """

    def die(self):
        self.is_alive = False
        self.current_action_reward -= int((self.exp + 1) * 0.75)
        print('Oh no! ' + self.name + ' died!')

        player_sprites_list.remove(self)
        all_sprites_list.remove(self)
        self.all_sprites.remove(self)
        self.players.remove(self)
        self.game.all_sprites.remove(self)
        self.game.player_sprites.remove(self)
        self.kill()

    """
    Level up
    """

    def level_up(self):
        level_up = False
        new_class = ''
        if self.sprite_class == 'thug' and self.exp >= 75:
            possibilities = ['squire', 'archer']
            choice = random.choices([0, 1], weights=(55, 45), k=1)
            new_class = possibilities[choice[0]]
            level_up = True

        elif self.sprite_class == 'squire' and self.exp >= 250:
            possibilities = ['knight', 'wizard', 'priest']
            choice = random.choices([0, 1, 2], weights=(80, 5, 15), k=1)
            new_class = possibilities[choice[0]]
            level_up = True

        elif self.sprite_class == 'archer' and self.exp >= 250:
            possibilities = ['knight', 'wizard', 'priest']
            choice = random.choices([0, 1, 2], weights=(30, 50, 20), k=1)
            new_class = possibilities[choice[0]]
            if possibilities[choice[0]] == 'priest':
                self.is_healer = True
            level_up = True

        elif self.exp >= 500 and not self.final_level:
            self.pow = int(self.pow * 1.25)
            self.max_health = int(self.max_health * 1.25)
            self.health = self.max_health
            self.final_level = True
            print(self.name + ' leveled up! You are now an arch-' + self.sprite_class + '.')

        if level_up:
            # load new textures
            self.idle_textures = []
            for i in range(0, 2):
                img = pygame.image.load("sprites/" + new_class + "_" + str(i) + ".PNG").convert_alpha()
                self.idle_textures.append(img)
            self.walking_down = False
            self.walking_right = True

            # max health
            self.max_health += available_player_classes.get(new_class)[0]
            self.health = self.max_health

            # power
            self.pow += available_player_classes.get(new_class)[1]
            self.sprite_class = new_class

            print(self.name + ' leveled up! You are now a ' + self.sprite_class + '.')

    """
    Update events, movement, state
    """

    def update(self):
        # make sure reward is reset
        self.current_action_reward = 0

        # check if enough exp to level up
        self.level_up()

        # check if new interests
        self.update_interests()

        # keep updating player while alive - move, collision vs enemy bonus or treasure, animations
        if self.health > 0:
            self.update_movement_textures_and_collisions()  # this also updates the state variables called by AI


        # if player dies then cleanup
        elif self.health <= 0:
            self.die()

        # update total score
        self.individual_score += self.current_action_reward



