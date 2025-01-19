import pygame

class Camera:
    def __init__(self, width, height, world_width, world_height, zoom_factor=1.0):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.world_width = world_width
        self.world_height = world_height
        self.zoom_factor = zoom_factor

    def apply(self, entity):
        """Applique l'effet de la caméra à un objet (joueur ou autre)."""
        # Applique un zoom et applique la position de la caméra
        zoomed_rect = pygame.Rect(
            (entity.rect.x - self.camera.x) * self.zoom_factor,
            (entity.rect.y - self.camera.y) * self.zoom_factor,
            entity.rect.width * self.zoom_factor,
            entity.rect.height * self.zoom_factor
        )
        return zoomed_rect

    def update(self, target):
        """Met à jour la position de la caméra pour suivre le joueur."""
        # Calculer la position de la caméra pour centrer sur le joueur
        x = -target.rect.centerx + int(self.width / 2)
        y = -target.rect.centery + int(self.height / 2)

        # Empêcher la caméra de sortir des bords de la carte
        x = min(0, x)  # Limite à gauche
        y = min(0, y)  # Limite en haut
        x = max(-(self.world_width - self.width), x)  # Limite à droite
        y = max(-(self.world_height - self.height), y)  # Limite en bas

        self.camera = pygame.Rect(x, y, self.width, self.height)

    def scale(self, surface):
        """Applique le zoom sur une surface."""
        return pygame.transform.scale(surface, (int(surface.get_width() * self.zoom_factor), int(surface.get_height() * self.zoom_factor)))
