import pygame
import pytmx
import time

def get_scaled_tile_image(tmx_data, gid, zoom, cache):
    """
    Récupère l'image pour 'gid' et la met à l'échelle en fonction de 'zoom'.
    Utilise un cache pour éviter de recalculer la transformation trop souvent.
    """
    if (gid, zoom) in cache:
        return cache[(gid, zoom)]
    
    original_image = tmx_data.get_tile_image_by_gid(gid)
    if original_image is None:
        return None
    
    # Dimensions d'une tuile * zoom
    tile_w = int(tmx_data.tilewidth * zoom)
    tile_h = int(tmx_data.tileheight * zoom)
    
    scaled_image = pygame.transform.scale(original_image, (tile_w, tile_h))
    cache[(gid, zoom)] = scaled_image
    return scaled_image

def load_collidable_tiles(tmx_data):
    """
    Parcourt les couches de la map et récupère (x, y) des tuiles 'collides = True'.
    """
    collidables = set()
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                if gid != 0:
                    props = tmx_data.get_tile_properties_by_gid(gid)
                    if props and props.get('collides') is True:
                        collidables.add((x, y))
    return collidables

def main():
    pygame.init()
    
    # Fenêtre 1280×720
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Map Grotte, collisions, orientation + anim, zoom=4, sprite agrandi")
    
    clock = pygame.time.Clock()
    
    # 1) Charger la map Tiled
    tmx_data = pytmx.util_pygame.load_pygame("Assets/assets tiled/grotte.tmx")
    tile_w = tmx_data.tilewidth
    tile_h = tmx_data.tileheight
    
    # 2) Collisions
    collidable_tiles = load_collidable_tiles(tmx_data)
    map_width_in_tiles = tmx_data.width
    map_height_in_tiles = tmx_data.height
    
    # 3) Chargement des frames d’animation par direction
    #    On suppose 4 frames : 0,1,2,3
    character_animations = {
        "down": [
            pygame.image.load("Python-Karl/sprites/down/down_0.png").convert_alpha(),
            pygame.image.load("Python-Karl/sprites/down/down_1.png").convert_alpha(),
            pygame.image.load("Python-Karl/sprites/down/down_2.png").convert_alpha(),
            pygame.image.load("Python-Karl/sprites/down/down_3.png").convert_alpha(),
        ],
        "up": [
            pygame.image.load("Python-Karl/sprites/up/up_0.png").convert_alpha(),
            pygame.image.load("Python-Karl/sprites/up/up_1.png").convert_alpha(),
            pygame.image.load("Python-Karl/sprites/up/up_2.png").convert_alpha(),
            pygame.image.load("Python-Karl/sprites/up/up_3.png").convert_alpha(),
        ],
        "left": [
            pygame.image.load("Python-Karl/sprites/left/left_0.png").convert_alpha(),
            pygame.image.load("Python-Karl/sprites/left/left_1.png").convert_alpha(),
            pygame.image.load("Python-Karl/sprites/left/left_2.png").convert_alpha(),
            pygame.image.load("Python-Karl/sprites/left/left_3.png").convert_alpha(),
        ],
        "right": [
            pygame.image.load("Python-Karl/sprites/right/right_0.png").convert_alpha(),
            pygame.image.load("Python-Karl/sprites/right/right_1.png").convert_alpha(),
            pygame.image.load("Python-Karl/sprites/right/right_2.png").convert_alpha(),
            pygame.image.load("Python-Karl/sprites/right/right_3.png").convert_alpha(),
        ],
    }
    
    # Variable qui stocke la direction actuelle (pour interactions)
    characterLook = "down"
    
    # 4) Position du personnage (en coordonnées tuile, float pour interpolation)
    player_x = 5.0
    player_y = 5.0
    
    # 5) Zoom = 4
    zoom = 4.0
    
    # 6) Facteur supplémentaire pour agrandir le sprite (ex: 2 = deux fois plus grand)
    SPRITE_SCALE = 2
    
    # Cache de tuiles redimensionnées
    scaled_tiles_cache = {}
    
    # 7) Animation de transition tuile par tuile
    #    => 0.1s pour passer d'une tuile à l'autre
    move_duration = 0.1
    
    # Vitesse de l'animation du perso (frames)
    CHARACTER_ANIM_SPEED = 0.3  # 1.0 = normal, 2.0 = plus rapide, 0.5 = plus lent
    
    is_moving = False
    move_start_x = 0.0
    move_start_y = 0.0
    move_target_x = 0.0
    move_target_y = 0.0
    move_start_time = 0
    
    pygame.key.set_repeat(200, 80)  # répète KEYDOWN si on maintient
    
    running = True
    
    while running:
        dt = clock.tick(60) / 1000.0  # dt en secondes
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                # Echap pour quitter
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                # Zoom +/-
                elif event.key in (pygame.K_PLUS, pygame.K_KP_PLUS):
                    zoom += 0.1
                    if zoom > 5.0:
                        zoom = 5.0
                    scaled_tiles_cache.clear()
                elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    zoom -= 0.1
                    if zoom < 0.1:
                        zoom = 0.1
                    scaled_tiles_cache.clear()
        
        # Gestion du déplacement
        # On vérifie si l'anim en cours est terminée
        next_move_possible = False
        if not is_moving:
            next_move_possible = True
        else:
            # On calcule le ratio d'animation
            elapsed = time.time() - move_start_time
            if elapsed >= move_duration:
                # Le déplacement est terminé
                player_x = move_target_x
                player_y = move_target_y
                is_moving = False
                next_move_possible = True
        
        # Si on peut enchaîner un nouveau déplacement
        if next_move_possible:
            direction_x = 0
            direction_y = 0
            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_LEFT]:
                direction_x = -1
                characterLook = "left"
            elif keys[pygame.K_RIGHT]:
                direction_x = 1
                characterLook = "right"
            elif keys[pygame.K_UP]:
                direction_y = -1
                characterLook = "up"
            elif keys[pygame.K_DOWN]:
                direction_y = 1
                characterLook = "down"
            
            if direction_x != 0 or direction_y != 0:
                curr_tile_x = int(round(player_x))
                curr_tile_y = int(round(player_y))
                target_tile_x = curr_tile_x + direction_x
                target_tile_y = curr_tile_y + direction_y
                
                # Vérif limites & collisions
                if 0 <= target_tile_x < map_width_in_tiles and 0 <= target_tile_y < map_height_in_tiles:
                    if (target_tile_x, target_tile_y) not in collidable_tiles:
                        # Lancer l'animation
                        is_moving = True
                        move_start_time = time.time()
                        move_start_x = player_x
                        move_start_y = player_y
                        move_target_x = float(target_tile_x)
                        move_target_y = float(target_tile_y)
        
        # Si on est en cours de déplacement, on interpole la position
        if is_moving:
            elapsed = time.time() - move_start_time
            ratio = min(elapsed / move_duration, 1.0)
            player_x = move_start_x + ratio * (move_target_x - move_start_x)
            player_y = move_start_y + ratio * (move_target_y - move_start_y)
        
        # Caméra centrée sur le perso
        player_px = player_x * tile_w * zoom
        player_py = player_y * tile_h * zoom
        
        camera_x = player_px - SCREEN_WIDTH / 2
        camera_y = player_py - SCREEN_HEIGHT / 2
        
        # -- Dessin --
        screen.fill((0, 0, 0))
        
        # Tuiles
        for layer in tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    if gid != 0:
                        scaled_image = get_scaled_tile_image(tmx_data, gid, zoom, scaled_tiles_cache)
                        if scaled_image:
                            draw_x = x * tile_w * zoom - camera_x
                            draw_y = y * tile_h * zoom - camera_y
                            screen.blit(scaled_image, (draw_x, draw_y))
        
        # -- Animation du perso --
        frames = character_animations[characterLook]
        nb_frames = len(frames)
        
        if is_moving:
            elapsed = time.time() - move_start_time
            ratio = elapsed / move_duration  # 0 -> 1
            # On multiplie ce ratio par la vitesse d'animation
            anim_progress = ratio * CHARACTER_ANIM_SPEED
            
            frame_index = int(anim_progress * nb_frames)
            if frame_index >= nb_frames:
                frame_index = nb_frames - 1
        else:
            # Immobile => frame 0
            frame_index = 0
        
        current_frame = frames[frame_index]
        
        # Zoomer la frame du perso + appliquer SPRITE_SCALE
        base_width = int(tile_w * zoom)
        base_height = int(tile_h * zoom)
        
        scaled_player_w = int(base_width * SPRITE_SCALE)
        scaled_player_h = int(base_height * SPRITE_SCALE)
        
        player_image_scaled = pygame.transform.scale(current_frame, (scaled_player_w, scaled_player_h))
        
        # Position d'affichage
        # Notez que le pivot reste le coin supérieur gauche : le perso semble un peu décalé
        # si on grossit beaucoup. On peut ajuster pour centrer différemment au besoin.
        p_draw_x = player_px - camera_x
        p_draw_y = player_py - camera_y
        
        # Pour centrer le sprite s'il est plus grand, on peut ajuster :
        p_draw_x -= (scaled_player_w - base_width) / 2
        # p_draw_y -= (scaled_player_h - base_height) / 2
        
        screen.blit(player_image_scaled, (p_draw_x, p_draw_y))
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()
