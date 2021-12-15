from config import *

def camera_events(game, key_states):
    # CAMERA CONTROLS WITH ARROW KEYS
    if key_states[pygame.K_LEFT]:
        for sprite in game.all_sprites:
            sprite.rect.x += TILE_SIZE
    if key_states[pygame.K_RIGHT]:
        for sprite in game.all_sprites:
            sprite.rect.x -= TILE_SIZE
    if key_states[pygame.K_UP]:
        for sprite in game.all_sprites:
            sprite.rect.y += TILE_SIZE
    if key_states[pygame.K_DOWN]:
        for sprite in game.all_sprites:
            sprite.rect.y -= TILE_SIZE


