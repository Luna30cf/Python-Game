import pygame
import random

class CrystalManager:
    def __init__(self, map_width, map_height, crystal_size=20, total_crystals=4):
        self.crystals = []  # Liste des cristaux (Rect)
        self.map_width = map_width
        self.map_height = map_height
        self.crystal_size = crystal_size
        self.total_crystals = total_crystals

    def generate_crystals(self):
        """Génère des cristaux à des positions aléatoires."""
        for _ in range(self.total_crystals):
            x = random.randint(0, self.map_width - self.crystal_size)
            y = random.randint(0, self.map_height - self.crystal_size)
            crystal_rect = pygame.Rect(x, y, self.crystal_size, self.crystal_size)
            self.crystals.append(crystal_rect)

    def draw_crystals(self, screen):
        """Dessine les cristaux sur l'écran."""
        for crystal in self.crystals:
            # Remplacez cette ligne pour dessiner une image à la place du carré rouge :
            # screen.blit(crystal_image, crystal.topleft)
            pygame.draw.rect(screen, (255, 0, 0), crystal)
