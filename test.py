import pygame
import pytmx

# Initialisation de Pygame
pygame.init()

# Charger la carte TMX
tmx_data = pytmx.load_pygame('Assets/assets tiled/mapv2.tmx')

# Déterminer la taille de la fenêtre en fonction de la carte
map_width = tmx_data.width * tmx_data.tilewidth
map_height = tmx_data.height * tmx_data.tileheight
screen = pygame.display.set_mode((map_width, map_height))

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
