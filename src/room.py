from src.door import Door
from src.item import Item

from src import params



import random



class Room:
    """
    Représente une pièce du manoir.
    Chaque pièce a :
    - un nom
    - une couleur (bleue, verte, rouge...)
    - un coût en gemmes
    - une rareté (0 à 3)
    - des portes (nord, sud, est, ouest)
    """

    def __init__(self, name: str, color: str,x,y, rarity: int = 0, cost: int = 0,src="E"):
        self.x = x
        self.y = y
        #self.icon_dir  = params.DICT_ROOM_DIRECTORIES.get(name)
        self.name = name # nom de la pièce (a"Chambre", "Cuisine", etc.)
        self.color = color # couleur ("bleue", "verte", "rouge", etc.) -> TODO Gerer proba tirage + effet au joueur
        self.rarity = rarity # rareté (0 à 3)
        self.cost = cost # coût en gemmes
        self.objects = [] # liste d'objets dans la pièce (Item)
        # TODO: Attribut image vers l'image de la pièce

        # Dictionnaire de portes : None au départ
        self.doors = {"N": None, "S": None, "E": None, "W": None}
        

    def add_door(self, direction: str, level_lock: int = 0):
        """Ajoute une porte dans une direction donnée."""
        if direction in self.doors:
            self.doors[direction] = Door(level_lock)
        else:
            raise ValueError("Direction invalide (utilise N, S, E ou W).")

    def connect(self, direction: str, other_room):
        """Connecte cette pièce à une autre dans une direction donnée."""

        # si roomA est connectée à l’Est (E), alors roomB sera connectée à l’Ouest (W)
        opposite = {"N": "S", "S": "N", "E": "W", "W": "E"} # Dictionnaire des directions opposées
        
        # Si la direction choisie par le joueur n'est pas possible
        if direction not in self.doors:
            raise ValueError("Direction invalide.")
        
        # Verif si les portes des deux pieces n'existent pas encore
        if self.doors[direction] is None:
            self.add_door(direction)
        if other_room.doors[opposite[direction]] is None:
            other_room.add_door(opposite[direction])
        
        # Connecte les deux pièces
        self.doors[direction].connected_room = other_room
        other_room.doors[opposite[direction]].connected_room = self
        # roomA.doors["E"].connected_room == roomB
        # roomB.doors["W"].connected_room == roomA
    
    def generate_objects_for_room(room):
        """Ajoute des objets à une pièce selon sa couleur et sa rareté."""
        chance = random.random()

        # Simple test d'ajout d'objets selon la couleur
        # TODO: Regarder comment gérer la rareté
        if room.color == "bleue":
            if chance < 0.3:
                room.add_object(Item("gemme", "consommable"))
        elif room.color == "verte":
            if chance < 0.5:
                room.add_object(Item("clé", "consommable"))
            elif chance < 0.7:
                room.add_object(Item("pelle", "permanent"))
        elif room.color == "jaune":
            room.add_object(Item("or", "consommable"))
        elif room.color == "rouge":
            # Pièce dangereuse: retirent des pas, etc. (non implémenté)
            pass

    def __repr__(self):
        # Affiche le nom, la couleur, la rareté et le coût - TEST
        return f"<Room {self.name} ({self.color}) r={self.rarity} c={self.cost}>"
    
