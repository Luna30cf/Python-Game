import pygame
import pytmx

class Map:
    def __init__(self):
        
        # Charge la carte TMX
        tmx_data = pytmx.load_pygame('Assets/assets tiled/mapv2.tmx')
        
        # Taille de la map
        self.width = self.tmx_data.width * self.tmx_data.tilewidth
        self.height = self.tmx_data.height * self.tmx_data.tileheight
        