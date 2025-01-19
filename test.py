import pygame
import pytmx

# Initialisation de Pygame
pygame.init()

# Charger la carte TMX
tmx_data = pytmx.load_pygame('Assets/assets tiled/mapv2.tmx')

# Vérifier la taille de la carte avant d'essayer d'afficher
map_width = tmx_data.width * tmx_data.tilewidth
map_height = tmx_data.height * tmx_data.tileheight

# Si la taille de la carte est valide, initialiser l'écran
if map_width > 0 and map_height > 0:
    screen = pygame.display.set_mode((map_width, map_height))
else:
    print("Erreur: Dimensions de la carte non valides.")
    pygame.quit()
    exit()

# Boucle principale du jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Effacer l'écran
    screen.fill((0, 0, 0))

    # Afficher toutes les tuiles de la carte
    for layer in tmx_data.layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    screen.blit(
                        tile,
                        (x * tmx_data.tilewidth, y * tmx_data.tileheight)
                    )

    # Actualiser l'écran
    pygame.display.flip()

# Quitter Pygame
pygame.quit()
