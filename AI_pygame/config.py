import pygame

# 32x32 pixels
TILE_SIZE = 32

# 16x16 tiles
WINDOW_SIZE = 16

# player movement speed
SPEED = TILE_SIZE / 2

FPS = 4

pygame.display.init()
pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))

TILEMAP = []
MAP_SIZE_X = 0
MAP_SIZE_Y = 0


# textures
# load biome textures
biome_textures = {
    '00': pygame.image.load('biomes/water.PNG').convert_alpha(),
    '01': pygame.image.load('biomes/mountain.PNG').convert_alpha(),
    '02': pygame.image.load('biomes/swamp.PNG').convert_alpha(),
    '03': pygame.image.load('biomes/grass.PNG').convert_alpha(),
    '04': pygame.image.load('biomes/desert.PNG').convert_alpha(),
    '05': pygame.image.load('biomes/forest.PNG').convert_alpha(),
    '06': pygame.image.load('biomes/forest2.PNG').convert_alpha(),
    '07': pygame.image.load('biomes/road.PNG').convert_alpha(),
    '08': pygame.image.load('biomes/coast_n.PNG').convert_alpha(),
    '09': pygame.image.load('biomes/coast_e.PNG').convert_alpha(),
    '10': pygame.image.load('biomes/coast_s.PNG').convert_alpha(),
    '11': pygame.image.load('biomes/coast_w.PNG').convert_alpha(),
    '12': pygame.image.load('biomes/coast_ne.PNG').convert_alpha(),
    '13': pygame.image.load('biomes/coast_se.PNG').convert_alpha(),
    '14': pygame.image.load('biomes/coast_sw.PNG').convert_alpha(),
    '15': pygame.image.load('biomes/coast_nw.PNG').convert_alpha(),
    '16': pygame.image.load('biomes/coast_nwu.PNG').convert_alpha(),
    '17': pygame.image.load('biomes/coast_swu.PNG').convert_alpha(),
    '18': pygame.image.load('biomes/coast_neu.PNG').convert_alpha(),
    '19': pygame.image.load('biomes/coast_seu.PNG').convert_alpha(),
    '20': pygame.image.load('biomes/crops1.PNG').convert_alpha(),
    '21': pygame.image.load('biomes/crops2.PNG').convert_alpha(),
    '22': pygame.image.load('biomes/semidesert.PNG').convert_alpha(),
    '23': pygame.image.load('biomes/dune.PNG').convert_alpha(),
    '24': pygame.image.load('biomes/coast_n_swamp.PNG').convert_alpha(),
    '25': pygame.image.load('biomes/coast_s_swamp.PNG').convert_alpha(),
    '26': pygame.image.load('biomes/coast_e_swamp.PNG').convert_alpha(),
    '27': pygame.image.load('biomes/coast_w_swamp.PNG').convert_alpha(),
    '28': pygame.image.load('biomes/coast_ne_swamp.PNG').convert_alpha(),
    '29': pygame.image.load('biomes/coast_nw_swamp.PNG').convert_alpha(),
    '30': pygame.image.load('biomes/coast_se_swamp.PNG').convert_alpha(),
    '31': pygame.image.load('biomes/coast_sw_swamp.PNG').convert_alpha(),
    '32': pygame.image.load('biomes/coast_nwu_swamp.PNG').convert_alpha(),
    '33': pygame.image.load('biomes/coast_swu_swamp.PNG').convert_alpha(),
    '34': pygame.image.load('biomes/coast_neu_swamp.PNG').convert_alpha(),
    '35': pygame.image.load('biomes/coast_seu_swamp.PNG').convert_alpha(),
    '36': pygame.image.load('biomes/bog.PNG').convert_alpha(),

}

# load building textures
building_textures = {
    'house': pygame.image.load('buildings/house.PNG').convert_alpha(),
    'cave': pygame.image.load('buildings/cave.PNG').convert_alpha(),
    'faery_house': pygame.image.load('buildings/faery_house.PNG').convert_alpha(),
    'castle': pygame.image.load('buildings/castle.PNG').convert_alpha(),
    'evil_castle': pygame.image.load('buildings/evil_castle.PNG').convert_alpha(),
    'bridge': pygame.image.load('buildings/bridge.PNG').convert_alpha(),
    'broken_bridge': pygame.image.load('buildings/broken_bridge.PNG').convert_alpha(),
    'stone_cross': pygame.image.load('buildings/stone_cross.PNG').convert_alpha(),
    'cactus': pygame.image.load('buildings/cactus.PNG').convert_alpha(),
    'necro_house': pygame.image.load('buildings/necro_house.PNG').convert_alpha(),
}

# load building text
building_text = {
    'house': 'a humble village house...',
    'cave': 'this is a spooky looking cave...',
    'stone_cross': 'an eerie stone cross...',
    'faery_house': 'I wonder if the faery is home...',
    'castle': 'a castle worthy of a noble!',
    'evil_castle': 'a castle worthy of an evil lord!',
    'bridge': 'this bridge looks sturdy enough...',
    'broken_bridge': 'this bridge is rotten and broken...',
    'cactus': 'this plant might have some water...',
    'necro_house': 'I guess the zombies had to come from somewhere...',
}

# load building reward
building_reward = {
    'house': 1,
    'cave': 25,
    'stone_cross': 15,
    'faery_house': 50,
    'castle': 25,
    'evil_castle': 666,
    'bridge': 3,
    'broken_bridge': 1,
    'cactus': 1,
    'necro_house': 2,
}


# load building coords - where to spawn buildings
building_coords = {
    'house': [(6, 4), (6, 5), (5, 6), (8, 6), (10, 9), (8, 15), (5, 28), (6, 27), (16, 14), (16, 10), (18, 14),
              (18, 15), (18, 10), (19, 6), (22, 48), (23, 48), (15, 48), (13, 48), (13, 49), (15, 46), (16, 46),
              (19, 49)],
    'cave': [(3, 3), (16, 5), (22, 33), (20, 27), (37, 49), (17, 55)],
    'stone_cross': [(12, 28)],
    'faery_house': [(13, 22), (30, 60)],
    'castle': [(7, 5), (16, 11), (18, 11), (13, 46), (28, 47), (28, 49), (15, 50), (29, 7)],
    'evil_castle': [(35, 7), (45, 5), (42, 11), (41, 19)],
    'bridge': [(10, 12), (11, 12), (28, 24), (29, 24), (30, 24), (16, 49), (17, 49), (18, 49), (20, 49), (21, 49),
               (22, 49), (24, 48), (25, 48), (26, 48), (27, 48), (28, 48), (32, 7), (31, 7), (30, 7), (33, 7)],
    'broken_bridge': [(13, 12), (15, 12), (27, 39), (26, 39), (29, 39), (30, 39), (34, 7)],
    'cactus': [(33, 39), (37, 38), (38, 42), (38, 49), (27, 33), (32, 31), (33, 50), (32, 25), (32, 33), (27, 55),
               (20, 55), (20, 53), (30, 61), (31, 60)],
    "necro_house": [(35, 5), (37, 5), (44, 4), (43, 4), (40, 11), (38, 16), (39, 10), (45, 8), (43, 14)],
}

available_player_classes = {
    # sprite_class : [health, power, line_of_sight]
    'thug': [5, 3, 5],
    'squire': [25, 5, 5],
    'archer': [10, 10, 5],
    'knight': [50, 10, 5],
    'wizard': [20, 25, 6],
    'priest': [15, 2, 5],
}

available_enemy_classes = {
    # sprite_class : [health, power, xp]
    'slime': [10, 1, 5],
    'beast': [50, 10, 15],
    'zombie': [100, 25, 30],
    'ghost': [75, 50, 50],
    'necromancer': [300, 80, 666],
}

enemy_coords = {
    'slime': [(9, 9), (8, 9), (7, 9), (4, 11), (8, 13), (10, 10), (5, 14), (12, 4), (15, 9),
              (18, 9), (9, 16), (9, 18), (9, 20), (9, 22), (12, 33), (14, 34), (17, 35), (15, 40), (17, 41), (12, 38),
              (22, 23), (24, 21), (25, 26), (25, 10), (25, 11), (23, 16), (10, 48), (11, 48), (9, 48), (10, 49),
              (10, 47), (10, 37), (10, 36), (7, 32), (7, 29), (6, 30), (6, 27), (5, 30), (7, 19), (6, 31), (4, 28),
              (5, 28), (5, 27)],
    'beast': [(20, 6), (26, 5), (19, 4), (15, 13), (16, 9), (18, 8), (17, 13),
              (12, 35), (14, 36), (17, 38), (20, 40), (23, 41), (19, 21), (21, 21), (22, 24), (23, 29),
              (33, 43), (37, 39), (38, 44), (39, 49), (27, 30), (33, 33),
              (27, 50), (20, 53), (18, 53), (29, 61), (31, 55)],
    'zombie': [(40, 18), (39, 16), (41, 8), (34, 7), (36, 7), (38, 9), (38, 13), (38, 16), (41, 11), (43, 11), (42, 10),
               (42, 12), (30, 7)],
    'ghost': [(42, 19), (37, 9), (41, 20), (41, 18), (44, 5), (42, 14), (44, 14), (43, 15), (43, 13)],
    'necromancer': [(35, 7), (45, 5), (42, 11), (41, 19)],
}

available_bonus_classes = {
    # sprite_class : [health, power, xp]
    'villager': [5, 1, 5],
    'gnome': [15, 5, 15],
    'faery': [30, 10, 50],
    'demon': [10, 30, 10],
}

bonus_coords = {
    'villager': [(8, 8), (4, 27), (16, 12), (18, 12), (15, 49), (25, 48), (11, 54), (12, 44)],
    'gnome': [(6, 17), (21, 35), (20, 54), (25, 8)],
    'faery': [(14, 21), (31, 61)],
    'demon': [(12, 27)],
}

# create sprite groups
player_sprites_list = pygame.sprite.Group()
bonus_sprites_list = pygame.sprite.Group()
enemy_sprites_list = pygame.sprite.Group()
block_sprites_list = pygame.sprite.Group()
building_sprites_list = pygame.sprite.Group()
biome_sprites_list = pygame.sprite.Group()
required_to_win_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()
