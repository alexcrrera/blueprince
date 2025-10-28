from src.door import Door
from src.item import Item

from src import params
import pygame


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

    def __init__(self, name,room_attributes,x,y,orientation=None):
        """
        data = dictionnaire venant du JSON
        """

        #print("Created: ",name)
        data =  room_attributes[name]
        self.name = name
        self.color = data["color"]
        self.rarity = data["rarity"]
        self.q = data["q"]
        self.placement_condition = data["placement_condition"]
        # 0 = common
        # 1 = standard
        # 2 = unusual
        # 3 = rare
        self.cost = data["cost"]
        self.image_path = f"assets/images/rooms/{data['image']}"

        # Array [Est, Nord, Ouest, Sud] - 0 = pas de porte, 1 = porte
        self.doors = [0, 0, 0, 0]
        direction_map = {"E": 0, "N": 1, "W": 2, "S": 3}
        for d in data["doors"]:
            if d in direction_map:
                self.doors[direction_map[d]] = 1

        self.door_status = random.randint(0, 2) 
        
        self.room_rotation = 0

        if(orientation is None):
            turn = 0
            self.room_rotation = 0
        else:
            if(orientation == 0):
                   # pour affichage
                 turn = 3
            else:
                turn = orientation -1
                # pour affichage
        
        
        for _ in range(turn):
            self.rotate_90_trigo()

        #print("Orientation start:",orientation," - turs to perform: ",turn,"Final Room rotation: ",self.room_rotation)
            

        # portes ouvertes au premier niveau
        if(y==8): # 1er  niveau
            self.door_status = 0 #ouverte

        # portes fermees a double tour
        if(y==0): #final level
            self.door_status = 2  #porte fermee a double tour

        self.items = [Item(i, "consommable") for i in data["items"]]
        self.x, self.y = x, y
        self.update_image()
        
         
       
    def update_image(self):
        img = pygame.image.load(self.image_path).convert_alpha()
        scaled_image = pygame.transform.scale(img, (params.ROOM_TILE_SIZE, params.ROOM_TILE_SIZE))


        rot =  90*(self.room_rotation)  # pour affichage
        self.IMAGE = pygame.transform.rotozoom(scaled_image, rot, 1)

    def rotate_90_trigo(self,keepRef=True):
        """
        Fait tourner la pièce de 90° dans le sens trigonométrique :
        - Met à jour les portes [E, N, W, S]
        - Incrémente room_rotation (dans le sens anti-horaire)
        """
        
        
        # [E, N, W, S] devient [N, W, S, E]
        self.doors = [self.doors[3], self.doors[0], self.doors[1], self.doors[2]]
        self.room_rotation = (self.room_rotation +1)%4
        
      
        self.update_image()
        
      
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
    
