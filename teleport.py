import pygame
import map as m

class teleporter:
        
    def Teleporter(self, player):
        """
        Vérifie si le joueur doit être téléporté à une nouvelle carte.
        """
        if (int(player.position_x), int(player.position_y)) in [(71, 12), (71, 13), (72, 12), (72, 13)]:
            print("[INFO] Téléportation déclenchée !")
            new_map = m.Map("grotte.tmx", "collidable_layers.json")
            new_position = (19, 29)
            return new_map, new_position

        return None, None
