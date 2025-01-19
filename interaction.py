# à completer 
# interactions.py
import pygame

class InteractionManager:
    def __init__(self, joueur):
        self.joueur = joueur
        self.houses = []  # Liste des maisons

    def add_house(self, house_rect):
        """Ajoute une maison à la liste des maisons interactives."""
        self.houses.append(house_rect)

    def is_near_house(self):
        """Vérifie si le joueur est proche d'une maison."""
        for house in self.houses:
            if self.joueur.rect.colliderect(house.inflate(50, 50)):  # Zone d'interaction autour de la maison
                return True, house
        return False, None

    def interact(self, house_rect):
        """Exécute l'interaction avec la maison."""
        # Ici, on peut mettre la logique pour changer de carte ou autre
        print("Interaction avec la maison !")
        return True  # Par exemple, cela pourrait retourner un booléen pour dire si l'interaction a réussi
