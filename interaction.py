# à completer 
# interactions.py
import pygame

class InteractionManager:
    def __init__(self, joueur):
        self.joueur = joueur
        self.houses = []  # Liste des maisons interactives
        self.pnj = []  # Listevillageois
        self.crystals = []  # Liste des cristaux a trouegr
        self.crystals_collected = 0  # Compteur des cristaux collectés
        self.total_crystals = 4  # Nombre total de cristaux à collecter
        self.message = ""  # Message affiché à l'écran
        self.message_time = 0  # Temps pendant lequel le message est affiché

    def add_house(self, house_rect):
        self.houses.append(house_rect)

    def add_npc(self, npc_rect):
        self.pnj.append(npc_rect)

    def add_object(self, object_rect):
        self.crystals.append(object_rect)

    def is_near_interactive(self):
        """Vérifie si le joueur est proche d'une maison, d'un villageois ou d'un objet."""
        for house in self.houses:
            if self.joueur.rect.colliderect(house.inflate(50, 50)):
                return "house", house

        for npc in self.pnj:
            if self.joueur.rect.colliderect(npc.inflate(50, 50)):
                return "npc", npc

        for obj in self.crystals:
            if self.joueur.rect.colliderect(obj.inflate(50, 50)):
                return "object", obj

        return None, None

    def interact(self, interaction_type, rect):
        if interaction_type == "house":
            self.message = "Vous entrez dans la maison."
            return True
        elif interaction_type == "npc":
            self.message = "Vous parlez avec un villageois."
            return True
        elif interaction_type == "object":
            self.crystals.remove(rect)
            self.crystals_collected += 1
            self.message = f"Vous avez trouvé {self.crystals_collected}/{self.total_crystals} cristaux !"
            return True
        return False

    def draw_message(self, screen, font, duration=3000):
        if self.message:
            now = pygame.time.get_ticks()
            if self.message_time == 0:
                self.message_time = now

            if now - self.message_time < duration:
                text_surface = font.render(self.message, True, (255, 255, 255))
                screen.blit(text_surface, (10, 10))
            else:
                self.message = ""
                self.message_time = 0
