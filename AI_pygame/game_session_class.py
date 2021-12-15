from AI_pygame.camera_class import camera_events
from enemy_class import *
from bonus_class import *
from player_class import *
from map_rendering import *
from config import *
import sys

class GameSession:
    def __init__(self, number_of_players):
        pygame.init()
        pygame.display.init()
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode((WINDOW_SIZE * TILE_SIZE, WINDOW_SIZE * TILE_SIZE))
        self.running = True
        self.number_of_players = number_of_players
        # for AI:
        self.total_score = 0  # reward = experience gained
        self.total_time = 0  # used for time limit to get certain amount of reward
        self.performance_quit = False
        self.AI_mode = True

        self.all_sprites = all_sprites_list
        self.player_sprites = player_sprites_list
        self.bonus_sprites = bonus_sprites_list
        self.enemy_sprites = enemy_sprites_list
        self.block_sprites = block_sprites_list
        self.building_sprites = building_sprites_list
        self.biome_sprites = biome_sprites_list
        self.required_to_win = required_to_win_list

    def new_game(self):
        print('Starting New Game Session...')
        render_environment(self)
        render_npc(self)

        print('Initializing game...')

        for i in range(self.number_of_players):
            name = 'Player ' + str(i + 1)
            self.player_sprites.add(Player(self, 'thug', 7, 6, name))
            print('Created ' + name)
        self.all_sprites.add(self.player_sprites)

        print('Game goal: Kill and Gather: ')
        for sprite in self.required_to_win:
            print(sprite.sprite_class)

        print('\n\n\n\n'
              '\nThe evil necromancers are creating an army of undead...'
              '\n...and unleashed monsters upon all our villages!'
              '\nThey hide in a far away land, long decayed from being ruled by evil undead. '
              '\nThe journey is full of dangers. You must help us!'
              '\nThe bridge to the east was broken... You need to travel south through the plains.'
              '\nBeware of crossroads... Thats where Daemons roam...'
              '\nYou will eventually reach a port city. They will have means of traveling east.'
              '\nBeat the desert, reach East Village. Knights will help you prepare...'
              '\nThey are holding back the hoards from the Swamplands, but not for much longer...'
              '\nYou are the only one capable of reaching that cursed island... May the faery blessings be with you...'
              '\nPut an end to these evil schemes...'
              '\n...before its too late!\n')

        print('\nWelcome to our Village, travelers!\n')
        players = []
        for player in self.player_sprites:
            players.append(player)
        return players

    def update(self):
        # update all sprites (call a_sprite.update() ) collision, movement, frame, individual_score, etc
        self.all_sprites.update()

        # update game total score
        self.total_score = 0
        for player in self.player_sprites:
            self.total_score += player.individual_score

    def event(self):
        # CAMERA MOVEMENT - ARROW KEYS
        key_states = pygame.key.get_pressed()
        camera_events(self, key_states)

        # OTHER EVENTS
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                #  quit
                if event.key == ord('q'):
                    print('\nShutting down game...\n')
                    self.running = False
                    sys.exit()

            if event.type == pygame.QUIT:
                # end the game
                self.running = False
                self.end_game()
                break


    def draw(self):
        # layer 0 - Biomes
        self.biome_sprites.draw(self.surface)
        # layer 1 - Buildings
        self.building_sprites.draw(self.surface)
        # layer 2 - NPCs
        self.enemy_sprites.draw(self.surface)
        self.bonus_sprites.draw(self.surface)
        # layer 3 - Players
        self.player_sprites.draw(self.surface)
        # layer 4 - Score and Time
        label = pygame.font.SysFont("monospace", 15).render('Total Score: ' + str(self.total_score), True, (255, 255, 0))
        self.surface.blit(label, (1, 0))
        label = pygame.font.SysFont("monospace", 15).render('Total Time: ' + str(int(self.total_time)), True, (255, 255, 0))
        self.surface.blit(label, (1, 15))

        # game clock and update display
        self.clock.tick(FPS)
        pygame.display.update()

    def end_game(self):
        scores = open("scores.txt", "a")
        scores.write(str(self.total_score) + " " + str(int(self.total_time)) + '\n')
        scores.close()

        # reset config sprite groups
        self.all_sprites.empty()
        self.player_sprites.empty()
        self.bonus_sprites.empty()
        self.enemy_sprites.empty()
        self.block_sprites.empty()
        self.building_sprites.empty()
        self.biome_sprites.empty()
        self.required_to_win.empty()

        # reset config globals
        globals()['TILEMAP'] = []
        globals()['MAP_SIZE_X'] = 0
        globals()['MAP_SIZE_Y'] = 0

        self.running = False
        pygame.quit()
        print('\n\nGame Over.\n\n')

    def performance(self):
        maximum_playtime = 300  # +/- 5 minutes
        minimum_playtime = 10   #
        # if playtime is over minimum and one of the other conditions is met:
        if self.total_score < 0:
            self.performance_quit = True
        if self.total_time > minimum_playtime and \
                ((self.total_time * 1.5 > self.total_score) or
                 (self.total_time > maximum_playtime) or
                 (self.total_time > maximum_playtime / 2 > self.total_score)):
            self.performance_quit = True

    def run_game(self):
        # while self.running:
        self.event()
        self.update()
        self.draw()
        self.performance()
        self.total_time += 0.28

        if not self.player_sprites and self.running:
            print('Oh no! Everyone died! The world is doomed...')

            self.total_score -= 250
            self.end_game()

        if not self.required_to_win and self.running:
            print('All the Necromancers are slain! Their castles lay in ruins! Their armies shall remain beaten!'
                  '\n You have saved the villages! Hurrah!')

            self.total_score += 1000
            self.end_game()

        if self.performance_quit and self.running and self.AI_mode:
            print('Time has run out!')

            if self.total_score < 0:
                self.total_score -= 100
            else:
                self.total_score -= 10

            self.end_game()



def render_environment(game):
    load_tilemap()
    map_renderer(game)
    print('Rendered Environmnet')


def render_npc(game):
    # npc setup (sprite_class, x, y)
    for enemy_type in enemy_coords:
        all_coords = enemy_coords.get(enemy_type)
        for coord in all_coords:
            enemy = Enemy(game, enemy_type, coord[0], coord[1])
            game.enemy_sprites.add(enemy)
            if enemy_type == 'necromancer':
                game.required_to_win.add(enemy)

    for bonus_type in bonus_coords:
        all_coords = bonus_coords.get(bonus_type)
        for coord in all_coords:
            game.bonus_sprites.add(Friend(game, bonus_type, coord[0], coord[1]))

    game.all_sprites.add(game.enemy_sprites)
    game.all_sprites.add(game.bonus_sprites)
    print('Created NPCs')
