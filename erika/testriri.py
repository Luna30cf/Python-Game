import pygame
import pytmx
from joueur import Joueur
from camera import Camera
from interaction import InteractionManager  # Gestionnaire d'interaction
from crystals import CrystalManager  # Gestionnaire des cristaux

# Initialisation de Pygame
pygame.init()

# Définir un facteur de zoom
zoom_factor = 1.5

# Créer la fenêtre d'affichage
map_width = 800  # Modifier en fonction de la taille de votre carte
map_height = 600  # Modifier en fonction de la taille de votre carte
screen = pygame.display.set_mode((map_width, map_height))

# Charger la carte TMX
tmx_data = pytmx.load_pygame('Assets/assets tiled/mapv2.tmx')

# Créer le joueur
joueur = Joueur(map_width // 2, map_height // 2, 5)

# Créer la caméra avec zoom
camera = Camera(map_width, map_height, tmx_data.width * tmx_data.tilewidth, tmx_data.height * tmx_data.tileheight, zoom_factor)

# Initialiser le gestionnaire des interactions
interaction_manager = InteractionManager(joueur)

# Initialiser le gestionnaire des cristaux
crystal_manager = CrystalManager(tmx_data.width * tmx_data.tilewidth, tmx_data.height * tmx_data.tileheight)

# Générer les cristaux aléatoires
crystal_manager.generate_crystals()

# Ajouter les cristaux au gestionnaire d'interaction
for crystal in crystal_manager.crystals:
    interaction_manager.add_object(crystal)

# Boucle principale du jeu
clock = pygame.time.Clock()
running = True
font = pygame.font.Font(None, 36)  # Police pour afficher les messages
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Récupérer les touches
    keys = pygame.key.get_pressed()

    # Basculer le menu d'informations
    if keys[pygame.K_i]:
        interaction_manager.toggle_info_menu()

    # Si le menu d'informations est affiché, ne rien faire d'autre
    if interaction_manager.show_info_menu:
        screen.fill((0, 0, 0))  # Effacer l'écran
        interaction_manager.draw_info_menu(screen, font)  # Dessiner le menu d'informations
        pygame.display.flip()
        clock.tick(60)
        continue

    # Mettre à jour le joueur
    joueur.update(keys)

    # Vérifier les interactions
    interaction_type, rect = interaction_manager.is_near_interactive()
    if interaction_type == "object" and keys[pygame.K_r]:
        interaction_manager.interact(interaction_type, rect)

    if interaction_type == "house_entry" and keys[pygame.K_e]:
        interaction_manager.interact(interaction_type, rect)

    if interaction_type == "house_exit" and keys[pygame.K_s]:
        interaction_manager.interact(interaction_type, rect)

    # Mettre à jour la caméra
    camera.update(joueur)

    # Effacer l'écran
    screen.fill((0, 0, 0))

    # Dessiner la carte
    for layer in tmx_data.layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, tile in layer:
                if tile:
                    tile_image = tmx_data.get_tile_image_by_gid(tile)
                    if tile_image:
                        tile_rect = pygame.Rect(x * tmx_data.tilewidth, y * tmx_data.tileheight, tmx_data.tilewidth, tmx_data.tileheight)
                        tile_object = Tile(tile_rect)
                        zoomed_rect = camera.apply(tile_object)
                        screen.blit(pygame.transform.scale(tile_image, (int(tile_rect.width * zoom_factor), int(tile_rect.height * zoom_factor))), zoomed_rect)

    # Dessiner les cristaux
    crystal_manager.draw_crystals(screen)

    # Dessiner le joueur
    joueur_rect = camera.apply(joueur)
    screen.blit(pygame.transform.scale(joueur.image, (int(joueur.rect.width * zoom_factor), int(joueur.rect.height * zoom_factor))), joueur_rect)

    # Afficher les messages
    interaction_manager.draw_message(screen, font)

    # Mettre à jour l'affichage
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
