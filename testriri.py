import pygame
import pytmx
import time
from joueur import Joueur  # Importer la classe Joueur de joueur.py
from interaction import InteractionManager  # Importer le gestionnaire d'interactions

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

# Initialiser le gestionnaire d'interactions
interaction_manager = InteractionManager(joueur)

# Ajouter des maisons à la liste d'interactions
for obj in tmx_data.objects:
    if obj.type == "maison":
        house_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
        interaction_manager.add_house(house_rect)

# Fonction pour charger une nouvelle carte
def load_new_map(map_name):
    """Charger une nouvelle carte TMX."""
    global tmx_data, interaction_manager
    # Recharger la carte TMX
    tmx_data = pytmx.load_pygame(map_name)

    # Réinitialiser les interactions en fonction de la nouvelle carte
    interaction_manager.houses.clear()  # Vider les maisons actuelles
    for obj in tmx_data.objects:
        if obj.type == "maison":
            house_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
            interaction_manager.add_house(house_rect)
    print(f"Nouvelle carte chargée : {map_name}")

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

    # Vérifier si le joueur est proche d'une maison et peut interagir
    is_near_house, house_rect = interaction_manager.is_near_house()
    if is_near_house and keys[pygame.K_e]:  # Si le joueur appuie sur E
        if interaction_manager.interact(house_rect):  # Effectuer l'interaction
            # Changer de carte ou effectuer d'autres actions
            print("Le joueur a interagi avec la maison et est transféré dans une nouvelle carte.")
            load_new_map("Assets/assets tiled/nouvelle_carte.tmx")  # Remplacer par le nom de la nouvelle carte

    # Afficher la carte et le joueur
    screen.fill((0, 0, 0))  # Effacer l'écran avant de redessiner
    for layer in tmx_data.layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    screen.blit(
                        tile,
                        (x * tmx_data.tilewidth * zoom_factor, y * tmx_data.tileheight * zoom_factor)
                    )

    # Dessiner le joueur
    joueur.draw(screen)

    # Afficher un message si le joueur peut interagir avec une maison
    if is_near_house:
        font = pygame.font.Font(None, 36)
        text = font.render("Appuyez sur E pour entrer", True, (255, 255, 255))
        screen.blit(text, (joueur.rect.x + 20, joueur.rect.y - 30))

    # Actualiser l'écran
    pygame.display.flip()

    # Contrôler le framerate
    clock.tick(60)

# Quitter Pygame
pygame.quit()
