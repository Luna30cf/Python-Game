import pygame
import pytmx
import time

def get_scaled_tile_image(tmx_data, gid, zoom, cache):
    """
    Récupère l'image pour 'gid' (une tuile) et la redimensionne selon 'zoom'.
    On utilise 'cache' pour éviter de recalculer constamment le scale.
    """
    if (gid, zoom) in cache:
        return cache[(gid, zoom)]
    
    original_image = tmx_data.get_tile_image_by_gid(gid)
    if original_image is None:
        return None
    
    tile_w = int(tmx_data.tilewidth * zoom)
    tile_h = int(tmx_data.tileheight * zoom)
    
    scaled_image = pygame.transform.scale(original_image, (tile_w, tile_h))
    cache[(gid, zoom)] = scaled_image
    return scaled_image

def load_collidable_layers(tmx_data):
    """
    Parcourt tous les calques de la map. 
    Si un calque a un nom dans 'collidable_layer_names',
    on ajoute toutes ses tuiles (x,y) à l'ensemble 'collidables'.
    """
    collidable_layer_names = {
        "limites",
        "collines",
        "lac",
        "arbres3 et fleurs",
        "arbres2 et fleurs",
        "arbres et touffes d'herbes",
        "fleurs",
        "barrières",
        "étage",
        "maison",
        "portes et bancs",
        "tonneaux1",
        "tonneaux2",
        "tonneaux3",
        "items sur tapis",
        "arbres et décos",
        "kayou",
    }
    
    collidables = set()
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            if layer.name in collidable_layer_names:
                for x, y, gid in layer:
                    if gid != 0:
                        collidables.add((x, y-1))
    return collidables

def find_valid_spawn(collidable_tiles, map_w, map_h, preferred_x=5, preferred_y=5):
    """
    Tente d'utiliser (preferred_x, preferred_y) comme spawn.
    Si c'est hors de la map ou bloquant, on cherche la première tuile libre.
    Retourne (spawn_x, spawn_y) en float.
    """
    if (0 <= preferred_x < map_w
        and 0 <= preferred_y < map_h
        and (preferred_x, preferred_y) not in collidable_tiles):
        return float(preferred_x), float(preferred_y)
    
    for ty in range(map_h):
        for tx in range(map_w):
            if (tx, ty) not in collidable_tiles:
                return float(tx), float(ty)
    return 0.0, 0.0

def main():
    pygame.init()
    
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Map Tiled : collisions togglable (noclip) + zoom + anim")
    
    clock = pygame.time.Clock()
    
    # === 1) Charger la map Tiled ===
    tmx_data = pytmx.util_pygame.load_pygame("Assets/assets tiled/mapv2.tmx")
    tile_w = tmx_data.tilewidth
    tile_h = tmx_data.tileheight
    
    # === 2) Tuiles bloquantes selon les calques nommés ===
    collidable_tiles = load_collidable_layers(tmx_data)
    map_width_in_tiles = tmx_data.width
    map_height_in_tiles = tmx_data.height
    
    print("[DEBUG] Nombre total de tuiles bloquantes =", len(collidable_tiles))
    
    # === 3) Déterminer un spawn valide ===
    spawn_x, spawn_y = find_valid_spawn(
        collidable_tiles,
        map_width_in_tiles,
        map_height_in_tiles,
        preferred_x=5,
        preferred_y=5
    )
    print(f"[DEBUG] Spawn validé : ({spawn_x},{spawn_y})")
    
    # === 4) Initialiser la position du perso ===
    player_x = spawn_x
    player_y = spawn_y
    
    # === 5) Zoom de la map et agrandissement du perso ===
    zoom = 4.0
    SPRITE_SCALE = 2
    
    scaled_tiles_cache = {}
    
    # === 6) Animation de déplacement (paramètres) ===
    move_duration = 0.1         # 0.1s par tuile
    CHARACTER_ANIM_SPEED = 0.3  # vitesse de frames
    
    # Variables de mouvement
    is_moving = False
    move_start_x = 0.0
    move_start_y = 0.0
    move_target_x = 0.0
    move_target_y = 0.0
    move_start_time = 0
    
    # === 7) Charger les sprites d’animation par direction ===
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
    
    # Direction initiale
    characterLook = "down"
    
    # === 8) Activer ou désactiver les collisions ===
    collision_enabled = True  # Par défaut, collisions actives
    
    # Pour répéter les KEYDOWN si on maintient la flèche
    pygame.key.set_repeat(200, 80)
    
    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
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
                
                # === Touche pour toggler collisions ===
                elif event.key == pygame.K_c:
                    collision_enabled = not collision_enabled
                    print(f"[DEBUG] Collisions {'activées' if collision_enabled else 'désactivées'}")
        
        # Fin d'un déplacement
        if is_moving:
            elapsed = time.time() - move_start_time
            if elapsed >= move_duration:
                player_x = move_target_x
                player_y = move_target_y
                is_moving = False
        
        # Nouveau déplacement si possible
        if not is_moving:
            keys = pygame.key.get_pressed()
            direction_x = 0
            direction_y = 0
            
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
                
                # Vérifier qu'on ne sort pas de la map
                if 0 <= target_tile_x < map_width_in_tiles and 0 <= target_tile_y < map_height_in_tiles:
                    
                    # Si collisions actives, on check le blocage
                    if collision_enabled and (target_tile_x, target_tile_y) in collidable_tiles:
                        print(f"[DEBUG] Tuile bloquante: ({target_tile_x},{target_tile_y}). Annulé.")
                    else:
                        print(f"[DEBUG] Déplacement validé: {curr_tile_x},{curr_tile_y} -> {target_tile_x},{target_tile_y}")
                        is_moving = True
                        move_start_time = time.time()
                        move_start_x = player_x
                        move_start_y = player_y
                        move_target_x = float(target_tile_x)
                        move_target_y = float(target_tile_y)
                else:
                    print(f"[DEBUG] Hors map: {target_tile_x},{target_tile_y}")
        
        # Interpolation si on bouge
        if is_moving:
            elapsed = time.time() - move_start_time
            ratio = min(elapsed / move_duration, 1.0)
            player_x = move_start_x + ratio * (move_target_x - move_start_x)
            player_y = move_start_y + ratio * (move_target_y - move_start_y)
        
        # Caméra centrée
        player_px = player_x * tile_w * zoom
        player_py = player_y * tile_h * zoom
        
        camera_x = player_px - SCREEN_WIDTH / 2
        camera_y = player_py - SCREEN_HEIGHT / 2
        
        # Dessin
        screen.fill((0, 0, 0))
        
        # Map
        for layer in tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    if gid != 0:
                        tile_img = get_scaled_tile_image(tmx_data, gid, zoom, scaled_tiles_cache)
                        if tile_img:
                            draw_x = x * tile_w * zoom - camera_x
                            draw_y = y * tile_h * zoom - camera_y
                            screen.blit(tile_img, (draw_x, draw_y))
        
        # Animation du perso
        frames = character_animations[characterLook]
        nb_frames = len(frames)
        
        if is_moving:
            elapsed = time.time() - move_start_time
            ratio = elapsed / move_duration
            anim_progress = ratio * CHARACTER_ANIM_SPEED
            frame_index = int(anim_progress * nb_frames)
            if frame_index >= nb_frames:
                frame_index = nb_frames - 1
        else:
            frame_index = 0
        
        current_frame = frames[frame_index]
        
        # Taille du perso
        base_w = int(tile_w * zoom)
        base_h = int(tile_h * zoom)
        scaled_player_w = int(base_w * SPRITE_SCALE)
        scaled_player_h = int(base_h * SPRITE_SCALE)
        
        player_image_scaled = pygame.transform.scale(current_frame, (scaled_player_w, scaled_player_h))
        
        p_draw_x = player_px - camera_x
        p_draw_y = player_py - camera_y
        
        # Centrage si agrandi
        p_draw_x -= (scaled_player_w - base_w) / 2
        # p_draw_y -= (scaled_player_h - base_h) / 2
        
        screen.blit(player_image_scaled, (p_draw_x, p_draw_y))
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()
