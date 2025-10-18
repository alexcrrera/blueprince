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
        self.position = start_pos
        self.x = self.position[0]
        self.y = self.position[1]
         # valeur par défaut d’après l’énoncé
   
     

        # Valeurs par défaut
        self.steps_left = params.INITIAL_STEPS
        self.inventory = Inventory()

        # Gestion du selector (nouvelle mécanique)
        self.selector_direction = None  # 'N', 'S', 'E', 'W'
        self.selector_visible = False   # affiché ou non

    # Déplacement
    def move(self, dx: int, dy: int):
        """Déplace le joueur dans la grille (sans vérif de murs pour l’instant)."""
        self.x += dx
        self.y += dy
        self.position = (self.x, self.y)
        self.steps_left -= 1
        print(f"🚶 Joueur déplacé en {self.position}")

    # Mise à jour par frame
    def update(self):
        """Met à jour la position et l’inventaire."""
        self.position = (self.x, self.y)
        # Empêche une erreur si inventory n’existe pas encore
        if hasattr(self, "inventory") and self.inventory is not None:
            self.inventory.update()

    def __repr__(self):
        return f"Player pos={self.position} steps={self.steps_left} inv={self.inventory}"
