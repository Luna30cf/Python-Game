import pygame
import pytmx
import time

# Initialisation de Pygame
pygame.init()

# Chargement de la carte TMX
tmx_data = pytmx.TiledMap('Assets/assets tiled/mapv2.tmx')

# Facteur de zoom
zoom_factor = 0  

# Calculer la taille de la fenêtre avec le facteur de zoom
map_width = int(tmx_data.width * tmx_data.tilewidth * zoom_factor)
map_height = int(tmx_data.height * tmx_data.tileheight * zoom_factor)

# Initialiser la fenêtre d'affichage avec les nouvelles dimensions
screen = pygame.display.set_mode((map_width, map_height))

# Ajouter un petit délai pour garantir l'initialisation complète
time.sleep(1)

# Recharger la carte TMX après l'initialisation de la fenêtre
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
                    # Appliquer le facteur de zoom en multipliant les coordonnées
                    scaled_tile = pygame.transform.scale(tile, 
                        (int(tmx_data.tilewidth * zoom_factor), 
                         int(tmx_data.tileheight * zoom_factor)))
                    screen.blit(
                        scaled_tile,
                        (int(x * tmx_data.tilewidth * zoom_factor), 
                         int(y * tmx_data.tileheight * zoom_factor))
                    )

    # Actualiser l'écran
    pygame.display.flip()

# Quitter Pygame
pygame.quit()
