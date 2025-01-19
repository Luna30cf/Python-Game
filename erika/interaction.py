import pygame

class InteractionManager:
    def __init__(self, joueur):
        self.joueur = joueur
        self.houses = []  # Liste des maisons interactives
        self.pnj = []  # Liste des villageois
        self.crystals = []  # Liste des cristaux à trouver
        self.crystals_collected = 0  # Compteur des cristaux collectés
        self.total_crystals = 4  # Nombre total de cristaux à collecter
        self.message = ""  # Message affiché à l'écran
        self.message_time = 0  # Temps pendant lequel le message est affiché
        self.current_map = "main"  # Carte actuelle ("main" ou "house")
        self.last_position_main = None  # Sauvegarde de la position dans la carte principale
        self.house_entry_rect = None  # Rectangle représentant l'entrée de la maison
        self.house_exit_rect = None  # Rectangle représentant la sortie de la maison
        self.show_info_menu = False  # Indique si le menu d'informations est affiché

    def set_house_entry(self, rect):
        """Définit la zone d'entrée de la maison."""
        self.house_entry_rect = rect

    def set_house_exit(self, rect):
        """Définit la zone de sortie de la maison."""
        self.house_exit_rect = rect

    def toggle_info_menu(self):
        """Affiche ou masque le menu d'informations."""
        self.show_info_menu = not self.show_info_menu

    def is_near_interactive(self):
        """Vérifie si le joueur est proche d'une maison, d'un villageois ou d'un objet (cristal)."""
        if self.current_map == "main" and self.house_entry_rect:
            if self.joueur.rect.colliderect(self.house_entry_rect.inflate(50, 50)):
                return "house_entry", self.house_entry_rect

        if self.current_map == "house" and self.house_exit_rect:
            if self.joueur.rect.colliderect(self.house_exit_rect.inflate(50, 50)):
                return "house_exit", self.house_exit_rect

        for house in self.houses:
            if self.joueur.rect.colliderect(house.inflate(50, 50)):  # Zone d'interaction autour de la maison
                return "house", house

        for npc in self.pnj:
            if self.joueur.rect.colliderect(npc.inflate(50, 50)):  # Zone d'interaction autour du villageois
                return "npc", npc

        for obj in self.crystals:
            if self.joueur.rect.colliderect(obj.inflate(50, 50)):  # Zone d'interaction autour du cristal
                return "object", obj

        return None, None

    def interact(self, interaction_type, rect):
        """Exécute l'interaction en fonction du type d'objet."""
        if interaction_type == "house_entry" and self.current_map == "main":
            # Entrer dans la maison
            self.last_position_main = self.joueur.rect.topleft  # Sauvegarde de la position actuelle
            self.current_map = "house"
            self.joueur.rect.topleft = (100, 100)  # Position initiale dans la maison
            self.message = "Vous entrez dans la maison."

        elif interaction_type == "house_exit" and self.current_map == "house":
            # Sortir de la maison
            self.current_map = "main"
            if self.last_position_main:
                self.joueur.rect.topleft = self.last_position_main  # Retour à la dernière position
            self.message = "Vous quittez la maison."

        elif interaction_type == "house":
            self.message = "Vous entrez dans la maison."
            return True

        elif interaction_type == "npc":
            self.message = "Vous parlez avec un villageois."
            return True

        elif interaction_type == "object":
            self.crystals.remove(rect)  # Enlever l'objet de la liste après l'avoir collecté
            self.crystals_collected += 1
            self.message = f"Vous avez trouvé {self.crystals_collected}/{self.total_crystals} cristaux !"
            return True

        return False

    def draw_message(self, screen, font, duration=3000):
        """Affiche un message à l'écran pendant un certain temps."""
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

    def draw_info_menu(self, screen, font):
        """Dessine le menu d'informations."""
        if self.show_info_menu:
            # Fond semi-transparent
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))  # Fond noir transparent
            screen.blit(overlay, (0, 0))

            # Texte du menu
            info_text = [
                "Touche E : Entrer dans une maison ou grotte",
                "Touche S : Sortir",
                "Touche R : Ramasser un objet",
                "Appuyer sur I pour fermer ce menu"
            ]
            for i, line in enumerate(info_text):
                text_surface = font.render(line, True, (255, 255, 255))
                screen.blit(text_surface, (50, 50 + i * 40))
