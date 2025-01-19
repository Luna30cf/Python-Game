import pygame
import pytmx


# Initialisation de Pygame
pygame.init()

# Définit la taille de la fenêtre
screen = pygame.display.set_mode((1780, 1000))
# Charge la carte TMX
tmx_data = pytmx.load_pygame('Assets/assets tiled/mapv2.tmx')

# Dimensionne l'image avec un facteur d'échelle par rapport à la fenêtre
scale_factor = 4

# Taille des tuiles redimensionnées
tile_width = tmx_data.tilewidth * scale_factor
tile_height = tmx_data.tileheight * scale_factor

# Initialisation du joueur (un simple rectangle pour cet exemple)
player = pygame.Rect(100, 100, 50, 50)  # x, y, largeur, hauteur
player_speed = 5

# Liste des calques à gérer pour les collisions
collision_layers = [
    "limites", "collines", "lac", "arbres3 et fleurs", "arbres2 et fleurs",
    "arbres et touffes d'herbes", "fleurs", "barrières", "étage", "maison",
    "portes et bancs", "tonneaux1", "tonneaux2", "tonneaux3", "items sur tapis",
    "arbres et décos", "kayou"
]


# Extraire les rectangles de collision pour chaque calque
collisions = []
for layer in tmx_data.layers:
    if layer.name in collision_layers:  # Vérifie si le calque est dans la liste
        for x, y, gid in layer:
            if gid:  # Si une tuile existe à cette position
                rect = pygame.Rect(
                    x * tile_width,
                    y * tile_height,
                    tile_width,
                    tile_height
                )
                collisions.append(rect)
                
# Boucle principale du jeu
running = True
while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Gestion des touches pour déplacer le joueur
    keys = pygame.key.get_pressed()
    new_x, new_y = player.x, player.y

    if keys[pygame.K_LEFT]:
        new_x -= player_speed
    if keys[pygame.K_RIGHT]:
        new_x += player_speed
    if keys[pygame.K_UP]:
        new_y -= player_speed
    if keys[pygame.K_DOWN]:
        new_y += player_speed

    # Création d'un rectangle simulant le déplacement
    new_rect = pygame.Rect(new_x, new_y, player.width, player.height)

    # Vérification des collisions
    collision_detected = False
    for coll_rect in collisions:
        if new_rect.colliderect(coll_rect):
            collision_detected = True
            break

    # Mise à jour de la position si pas de collision
    if not collision_detected:
        player.x = new_x
        player.y = new_y

    # Effacer l'écran
    screen.fill((0, 0, 0))

    # Afficher les tuiles de la carte avec redimensionnement
    for layer in tmx_data.layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    # Redimensionner la tuile selon le facteur d'échelle
                    tile = pygame.transform.scale(tile, (tile_width, tile_height))
                    # Dessiner la tuile redimensionnée à l'écran
                    screen.blit(tile, (x * tile_width, y * tile_height))

    # Dessiner le joueur
    pygame.draw.rect(screen, (255, 0, 0), player)  # Joueur en rouge

    # Actualiser l'écran
    pygame.display.flip()

# Quitter Pygame
pygame.quit()