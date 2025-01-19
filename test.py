import pygame
import pytmx
import time

# Initialisation de Pygame
pygame.init()

# Calculer la taille de la fenêtre avant de charger la carte
tmx_data = pytmx.TiledMap('Assets/assets tiled/mapv2.tmx')
map_width = tmx_data.width * tmx_data.tilewidth
map_height = tmx_data.height * tmx_data.tileheight

# Initialiser la fenêtre d'affichage avec les dimensions de la carte
screen = pygame.display.set_mode((map_width, map_height))

# Ajouter un petit délai pour garantir l'initialisation complète
time.sleep(1)

# Charger la carte TMX après l'initialisation de la fenêtre
tmx_data = pytmx.load_pygame('Assets/assets tiled/mapv2.tmx')

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
