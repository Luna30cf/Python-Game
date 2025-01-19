import pygame
import pytmx
import luna.Map as Map

# Initialisation de Pygame
pygame.init()


# Boucle principale du jeu
running = True
while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Effacer l'écran
    screen.fill((0, 0, 0))
    # Afficher les tuiles de la carte avec redimensionnement
    for layer in tmx_data.layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    # Redimensionner la tuile selon le facteur d'échelle
                    tile = pygame.transform.scale(tile, (tmx_data.tilewidth * scale_factor, tmx_data.tileheight * scale_factor))
                    
                    # Dessiner la tuile redimensionnée à l'écran
                    screen.blit(tile, (x * tmx_data.tilewidth * scale_factor, y * tmx_data.tileheight * scale_factor))
    # Actualiser l'écran
    pygame.display.flip()
# Quitter Pygame
pygame.quit()