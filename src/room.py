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

    def __init__(self, name,room_attributes,x,y,rotation):
        """
        data = dictionnaire venant du JSON
        """
        data =  room_attributes[name]
        self.name = name
        self.color = data["color"]
        self.rarity = data["rarity"]
        self.cost = data["cost"]
        self.image_path = f"assets/images/rooms/{data['image']}"

        # Array [Est, Nord, Ouest, Sud] - 0 = pas de porte, 1 = porte
        self.doors = [0, 0, 0, 0]
        direction_map = {"E": 0, "N": 1, "W": 2, "S": 3}
        for d in data["doors"]:
            if d in direction_map:
                self.doors[direction_map[d]] = 1

        self.door_status = random.randint(0, 2) 
        self.room_rotation = rotation
        # portes ouvertes au premier niveau
        if(y==8): # 1er  niveau
            self.door_status = 0 #ouverte

        # portes fermees a double tour
        if(y==0): #final level
            self.door_status = 2  #porte fermee a double tour

        self.items = [Item(i, "consommable") for i in data["items"]]
        self.x, self.y = x, y
        

    def add_door(self, direction: str, level_lock: int = 0):
        """Ajoute une porte dans une direction donnée."""
        if direction in self.doors:
            self.doors[direction] = Door(level_lock)
        else:
            raise ValueError("Direction invalide (utilise N, S, E ou W).")

    def rotate_90_trigo(self):
        """
        Fait tourner la pièce de 90° dans le sens trigonométrique :
        - Met à jour les portes [E, N, W, S]
        - Incrémente room_rotation (dans le sens anti-horaire)
        """
        # [E, N, W, S] devient [N, W, S, E]
        self.doors = [self.doors[1], self.doors[2], self.doors[3], self.doors[0]]
        self.room_rotation = (self.room_rotation + 1) % 4

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
    
