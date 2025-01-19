import pygame
import pytmx
from joueur import Joueur
from interaction import InteractionManager

pygame.init()

# Charger la carte TMX
tmx_data = pytmx.load_pygame('Assets/assets tiled/mapv2.tmx')

# Dimensions de la carte
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Game")

# Créer le joueur
joueur = Joueur(400, 300, 5)

# Initialiser les interactions
interaction_manager = InteractionManager(joueur)

# Ajouter les objets interactifs
for obj in tmx_data.objects:
    rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
    if obj.type == "maison":
        interaction_manager.add_house(rect)
    elif obj.type == "pnj":
        interaction_manager.add_npc(rect)
    elif obj.type == "objet":
        interaction_manager.add_object(rect)

# Boucle principale
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    joueur.update(keys)

    interaction_type, interactive_rect = interaction_manager.is_near_interactive()
    if interaction_type == "house" and keys[pygame.K_e]:
        interaction_manager.interact("house", interactive_rect)
    elif interaction_type == "npc" and keys[pygame.K_p]:
        interaction_manager.interact("npc", interactive_rect)
    elif interaction_type == "object" and keys[pygame.K_r]:
        interaction_manager.interact("object", interactive_rect)

    if interaction_type == "house":
        interaction_manager.message = "Presse E pour entrer"
    elif interaction_type == "npc":
        interaction_manager.message = "Presse P pour parler"
    elif interaction_type == "object":
        interaction_manager.message = "Presse R pour ramasser"

    # Affichage
    screen.fill((0, 0, 0))
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    screen.blit(tile, (x * tmx_data.tilewidth, y * tmx_data.tileheight))

    joueur.draw(screen)
    font = pygame.font.Font(None, 36)
    interaction_manager.draw_message(screen, font)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
