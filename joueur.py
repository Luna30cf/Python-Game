import pygame

class Joueur:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

        # Charger la feuille de sprites
        self.sprite_sheet = pygame.image.load("Assets/joueur/walk and idle.png").convert_alpha()

        # Paramètres de la feuille de sprites
        self.sprite_width = 32
        self.sprite_height = 32
        self.scaled_width = 32
        self.scaled_height = 32

        # Découper les animations pour chaque direction
        self.animations = {
            "down": self.load_animation(0),
            "left": self.load_animation(1),
            "right": self.load_animation(2),
            "up": self.load_animation(3)
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
        for i in range(3):  # Nombre de frames par ligne
            frame = self.sprite_sheet.subsurface(
                pygame.Rect(i * self.sprite_width, row * self.sprite_height, self.sprite_width, self.sprite_height)
            )
            resized_frame = pygame.transform.scale(frame, (self.scaled_width, self.scaled_height))
            frames.append(resized_frame)
        return frames

    def update(self, keys):
        """Met à jour la position et l'animation du joueur."""
        dx, dy = 0, 0
        direction = None

        # Déplacer le joueur selon les touches
        if keys[pygame.K_UP]:
            dy = -self.speed
            direction = "up"
        elif keys[pygame.K_DOWN]:
            dy = self.speed
            direction = "down"
        elif keys[pygame.K_LEFT]:
            dx = -self.speed
            direction = "left"
        elif keys[pygame.K_RIGHT]:
            dx = self.speed
            direction = "right"

        self.x += dx
        self.y += dy

        # Mettre à jour l'animation
        if direction:
            self.current_animation = self.animations[direction]
            self.animate()

        # Mettre à jour la position du rectangle
        self.rect.center = (self.x, self.y)

    def animate(self):
        """Gère le changement des frames de l'animation."""
        now = pygame.time.get_ticks()
        if now - self.last_update > 100:  # Temps entre les frames
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.current_animation)
            self.image = self.current_animation[self.current_frame]

    def draw(self, screen):
        """Dessine le joueur à l'écran."""
        screen.blit(self.image, self.rect.topleft)
