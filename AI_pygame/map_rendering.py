from wall_class import *
from building_class import *
from biome_class import *


# loads matrix with map data
def load_tilemap():
    # reset config globals from previous AI runs
    globals()['TILEMAP'] = []
    globals()['MAP_SIZE_X'] = 0
    globals()['MAP_SIZE_Y'] = 0

    with open('biome_matrix.txt', 'r') as f:
        data = f.readlines()

    for raw_line in data:
        split_line = raw_line.strip().split(",")
        TILEMAP.append(split_line)

    globals()['MAP_SIZE_X'] = len(TILEMAP[0])
    globals()['MAP_SIZE_Y'] = len(TILEMAP)

    print('X ' + str(MAP_SIZE_X))
    print('Y ' + str(MAP_SIZE_Y))


def map_renderer(game):
    # reset config sprite groups from previous AI runs
    game.all_sprites.empty()
    game.player_sprites.empty()
    game.bonus_sprites.empty()
    game.enemy_sprites.empty()
    game.block_sprites.empty()
    game.building_sprites.empty()
    game.biome_sprites.empty()
    game.required_to_win.empty()

    # draw biomes
    for row in range(MAP_SIZE_Y):
        # loop through each column
        for column in range(MAP_SIZE_X):
            # draw biome
            biome = Biome(game, column, row, biome_textures.get(TILEMAP[row][column]))
            game.biome_sprites.add(biome)

            # draw invisible walls on top of water and mountains
            if TILEMAP[row][column] == '00':
                wall = Wall(game, column, row, "I dont feel like going for a swim...")
                game.block_sprites.add(wall)
                game.boundaries.append((wall.x, wall.y))
            elif TILEMAP[row][column] == '01' or TILEMAP[row][column] == '23' or TILEMAP[row][column] == '36':
                wall = Wall(game, column, row, "I dont think I can climb that...")
                game.block_sprites.add(wall)
                game.boundaries.append((wall.x, wall.y))

    # draw buildings
    for key in building_coords:
        buildings = building_coords.get(key)
        for loc in buildings:
            building = Building(game, loc[0], loc[1], building_textures.get(key), key, building_text.get(key), building_reward.get(key))
            game.building_sprites.add(building)
            if building.sprite_class == "evil_castle":
                game.required_to_win.add(building)

    game.all_sprites.add(game.biome_sprites)
    game.all_sprites.add(game.building_sprites)
    game.all_sprites.add(game.block_sprites)

