FOLDERS:

biomes - has all biome textures
buildings - has all building textures
sprites - has all agent textures
model - has pytorch AI saved models

.PY FILES

AI:
pytorch_ai - Run this file to start up the AI and game. This is where the AI stuff is at.  
The AI calls game_session continuously. Press the Q key to stop. 

GAME:
game_session_class - This is where the game initialization stuff is at. Render Textures, Start/End, Render/Update Sprites/Biomes, etc.
biome_class - handles biomes
building_class - handles buildings and gathering their rewards
wall_class - handles collisions with mountains and water
player_class - handles player agents, has most of the methods that involve interaction with other classes
bonus_class - handles bonus agents and gathering their rewards
enemy_class - handles enemy agents and gaining experience
camera_class - handles control of the game window. Game window size is limited, map size is not. Use arrow keys to see the rest of the map

map_rendering - handles assigning biome textures on layer 0. 
config - handles pygame settings, loads textures NPC's buildings and data, handles various class data



.TXT FILES

biome_matrix.txt - where the layer 0 of the map is drawn.
scores.txt - where AI game scores are saved. 
ReadMe.txt - you are here, dummy

HOW TO:
- add NPC's or buildings ---> go to config.py, go to respective coord dictionary, add x,y coord in the key of your choice
- add Player ---> theres 3 players by default, change it in game_session.py new_game()
- change biomes ---> change the values in the biome_matrix.txt file according to the available values in conf.py



