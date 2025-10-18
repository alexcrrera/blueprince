from src.inventory import Inventory

from src import params


class Player:
    """
    Représente le joueur.
    - position : (x, y) dans la grille du manoir
    - steps_left : nombre de pas restants
    - inventory : objets et ressources
    """

    def __init__(self, start_pos=(2, 8)):
            
        #lool
        self.position = start_pos
        self.x = self.position[0]
        self.y = self.position[1]
         # valeur par défaut d’après l’énoncé
        self.inventory = Inventory()

  
     

    # Le joueur peut se déplacer n'importe où dans la grille (même en dehors du manoir)
    # TODO: ajouter vérif murs/portes
    def move(self, dx: int, dy: int):
        """Déplace le joueur dans la grille (pour l’instant sans vérif de murs)."""
        x, y = self.position
        self.position = (x + dx, y + dy)
        self.steps_left -= 1  # chaque déplacement coûte 1 pas

    def __repr__(self):
        
        return f"Player pos={self.position} steps={self.steps_left} inv={self.inventory}"
    
    def update(self):
        self.x = self.position[0]
        self.y = self.position[1]
        self.inventory.update()