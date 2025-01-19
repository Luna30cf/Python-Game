import pygame
import pytmx
import time
from joueur import Joueur  # Importer la classe Joueur de joueur.py

# Initialisation de Pygame
pygame.init()

# Chargement de la carte TMX
tmx_data = pytmx.TiledMap('Assets/assets tiled/mapv2.tmx')

# Facteur de zoom
zoom_factor = 1.5  # Ajuster selon le niveau de zoom souhaité

# Calculer la taille de la fenêtre avec le facteur de zoom
map_width = int(tmx_data.width * tmx_data.tilewidth * zoom_factor)
map_height = int(tmx_data.height * tmx_data.tileheight * zoom_factor)

# Initialiser la fenêtre d'affichage avec les nouvelles dimensions
screen = pygame.display.set_mode((map_width, map_height))

# Ajouter un petit délai pour garantir l'initialisation complète
time.sleep(1)

# Recharger la carte TMX après l'initialisation de la fenêtre
tmx_data = pytmx.load_pygame('Assets/assets tiled/mapv2.tmx')

# Créer le personnage (joueur)
joueur = Joueur(map_width // 2, map_height // 2, 20)  # Position initiale au centre de la carte

# Boucle principale du jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Récupérer les touches
    keys = pygame.key.get_pressed()

    # Mettre à jour le joueur
    joueur.update(keys)

    # Afficher la carte et le joueur
    screen.fill((0, 0, 0))
    for layer in tmx_data.layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    screen.blit(
                        tile,
                        (x * tmx_data.tilewidth, y * tmx_data.tileheight)
                    )

    # Dessiner le joueur
    joueur.draw(screen)

    # Actualiser l'écran
    pygame.display.flip()

pygame.quit()
