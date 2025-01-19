import pygame
import pytmx
from joueur import Joueur  # Assurez-vous que la classe Joueur est correctement importée
from camera import Camera  # Assurez-vous que la classe Camera est correctement importée

# Classe Tile pour encapsuler les objets avec un attribut 'rect'
class Tile:
    def __init__(self, rect):
        self.rect = rect

# Initialisation de Pygame
pygame.init()

# Définir un facteur de zoom (par exemple 1.5 pour agrandir la carte)
zoom_factor = 1.5

# Créer la fenêtre d'affichage avant de charger la carte
map_width = 800  # Modifier en fonction de la taille de votre carte
map_height = 600  # Modifier en fonction de la taille de votre carte

screen = pygame.display.set_mode((map_width, map_height))

# Chargement de la carte TMX après l'initialisation de la fenêtre
tmx_data = pytmx.load_pygame('Assets/assets tiled/mapv2.tmx')

# Créer le joueur
joueur = Joueur(map_width // 2, map_height // 2, 5)  # Position initiale au centre de la carte

# Créer la caméra avec zoom
camera = Camera(map_width, map_height, tmx_data.width * tmx_data.tilewidth, tmx_data.height * tmx_data.tileheight, zoom_factor)

# Boucle principale du jeu
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Récupérer les touches
    keys = pygame.key.get_pressed()

    # Mettre à jour le joueur
    joueur.update(keys)

    # Mettre à jour la caméra en fonction du joueur
    camera.update(joueur)

    # Afficher la carte et le joueur
    screen.fill((0, 0, 0))  # Effacer l'écran avant de redessiner

    # Dessiner la carte avec zoom
    for layer in tmx_data.layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, tile in layer:
                if tile:
                    # Obtenir l'image du tile en fonction de son GID
                    tile_image = tmx_data.get_tile_image_by_gid(tile)

                    if tile_image:
                        # Calculer la position du tile
                        tile_rect = pygame.Rect(x * tmx_data.tilewidth, y * tmx_data.tileheight, tmx_data.tilewidth, tmx_data.tileheight)

                        # Créer un objet Tile avec le rect et l'utiliser dans apply
                        tile_object = Tile(tile_rect)
                        zoomed_rect = camera.apply(tile_object)  # Maintenant, vous passez un objet avec un attribut 'rect'
                        screen.blit(pygame.transform.scale(tile_image, (int(tile_rect.width * zoom_factor), int(tile_rect.height * zoom_factor))), zoomed_rect)

    # Dessiner le joueur avec zoom et caméra appliqués
    joueur_rect = camera.apply(joueur)  # Appliquer le zoom et la caméra au joueur
    screen.blit(pygame.transform.scale(joueur.image, (int(joueur.rect.width * zoom_factor), int(joueur.rect.height * zoom_factor))), joueur_rect)

    # Actualiser l'écran
    pygame.display.flip()

    # Contrôler le framerate
    clock.tick(60)

# Quitter Pygame
pygame.quit()
