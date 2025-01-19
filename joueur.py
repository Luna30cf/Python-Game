import pygame

class Joueur:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

        # Charger la feuille de sprites
        self.sprite_sheet = pygame.image.load("Assets/joueur/walk and idle.png").convert_alpha()

        # Vérifier les dimensions de la feuille de sprites
        print(f"Sprite sheet dimensions: {self.sprite_sheet.get_width()}x{self.sprite_sheet.get_height()}")

        # Paramètres de la feuille de sprites
        self.sprite_width = 32  # Taille de découpe
        self.sprite_height = 32 
        self.scaled_width = 8  # Taille redimensionnée
        self.scaled_height = 8  

        # Découper les animations pour chaque direction
        self.animations = {
            "down": self.load_animation(0),   # Ligne pour bas
            "left": self.load_animation(1),   # Ligne pour gauche
            "right": self.load_animation(1),  # Ligne pour droite (même que pour gauche)
            "up": self.load_animation(0)     # Ligne pour haut (même que pour bas)
        }

        # Animation actuelle par défaut : bas
        self.current_animation = self.animations["down"]
        self.current_frame = 0
        self.animation_speed = 0.1
        self.last_update = pygame.time.get_ticks()

        # Initialisation de l'image et du rectangle pour le joueur
        self.image = self.current_animation[self.current_frame]
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def load_animation(self, row):
        """Découpe et redimensionne les frames d'une ligne spécifique dans la feuille de sprites."""
        frames = []
        frames_per_row = 24  # 24 frames par ligne (192 / 8 = 24)
        for i in range(frames_per_row):
            frame = self.sprite_sheet.subsurface(
                pygame.Rect(i * 8, row * 8, 8, 8)
            )
            resized_frame = pygame.transform.scale(frame, (self.scaled_width, self.scaled_height))  # Nouvelle taille (8x8)
            frames.append(resized_frame)
        return frames

    def update(self, keys):
        """Met à jour la position et l'animation du joueur."""
        dx, dy = 0, 0
        direction = None
        if keys[pygame.K_LEFT]:
            dx = -self.speed
            direction = "left"
        if keys[pygame.K_RIGHT]:
            dx = self.speed
            direction = "right"
        if keys[pygame.K_UP]:
            dy = -self.speed
            direction = "up"
        if keys[pygame.K_DOWN]:
            dy = self.speed
            direction = "down"

        # Mettre à jour la position du joueur
        self.x += dx
        self.y += dy

        # Mettre à jour l'animation
        if direction:
            self.current_animation = self.animations[direction]
            self.animate()

        # Mettre à jour la position du rectangle du joueur
        self.rect.center = (self.x, self.y)

    def animate(self):
        """Gère le changement des frames de l'animation."""
        now = pygame.time.get_ticks()
        if now - self.last_update > 100:  # Temps entre les frames (100ms ici)
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.current_animation)
            self.image = self.current_animation[self.current_frame]

    def draw(self, screen):
        """Dessine le joueur à l'écran."""
        screen.blit(self.image, self.rect.topleft)
