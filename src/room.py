from src.door import Door
from src.item import Item

from src import params
import pygame

from src.inventory import Inventory,RoomInventory
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
        self.rarity = data["rarity"] # 0 = common ,  1 = standard , 2 = unusual ,  3 = rare
        self.q = data["q"]
        self.placement_condition = data["placement_condition"]
        
        self.cost = data["cost"]
        self.image_path = f"assets/images/rooms/{data['image']}"

        self.cleaned_name = self.returnNameWithoutUnderscore()

        # Array [Est, Nord, Ouest, Sud] - 0 = pas de porte, 1 = porte
        self.doors = [0, 0, 0, 0]
        self.door_status = list()

        direction_map = {"E": 0, "N": 1, "W": 2, "S": 3}

        for d in data["doors"]:
            if d in direction_map:
                self.doors[direction_map[d]] = 1


        
        
        self.room_rotation = 0

        if(orientation is None):
            turn = 0
            self.room_rotation = 0
        else:
            if(orientation == 0):

                 turn = 3
            else:
                turn = orientation -1
                # pour affichage
        
        

        #print("Orientation start:",orientation," - turs to perform: ",turn,"Final Room rotation: ",self.room_rotation)
        self.door_status = list()
        y_max = params.ROOM_GRID_SIZE_VERTICAL-1 #= 8
        #weights = [1/(3**(y_max-y)),1/(3),1/(3**y)]
        w_unlocked = 1/(3**(y_max-y))
        w_double_lock = 1/(3**y)
        w_single_lock = 1/2*(w_unlocked + w_double_lock)/2
       
        weights = [w_unlocked,w_single_lock,w_double_lock]
    
        #print("w: ", weights)
        # ainsi proportionnel à la profondeur du manoi

        choices = [1, 2, 3]
 
        for d in self.doors:
            
            if d == 1:
                inter_status = random.choices(choices, weights=weights, k=1)[0]
                

                if(y==y_max):
                    inter_status = 1

                if(y==0):
                    inter_status = 3

                self.door_status.append(inter_status)    
            else:
                self.door_status.append(0) # pas de porte disponible donc pas de statuts

       # if(orientation is not None):
            #self.door_status[(orientation+2)%4] = 1 # la porte par laquelle on én génère la chambre a déjà été ouverte...
 

        
        
        for _ in range(turn):
            self.rotate_90_trigo()    
       # print("Door's status is ", self.door_status, " - doors: ",self.doors )
        self.possible_items = data["possible_items"]
        self.def_items = data["items"]
        self.items = {}
        self.actions = {}


        #self.randomObjectsGeneration()
   
        self.generateItems()
        self.inventory = RoomInventory(self.items,self.actions)

        self.items = True

        
        #self.room_inventory = Inventory()


        self.x, self.y = x, y


        

        self.update_image()




    def generateItems(self,add_items=None):

        descriptor = params.ITEMS_DESCRIPTION_DICT
        for key,val in self.possible_items.items():
            
            rarity_item = int(descriptor.get(key)[3])
            
            
            rand_choice =  random.randint(0,rarity_item+1)
            if(rand_choice == 0): #item pas présent dans la salle
                continue

            if val[1] == 0:
                item_q = val[0]
            else:
                item_q = random.randint(0,val[0])


            if key in self.items:
                self.items[key] += item_q
            else:
                self.items[key] = item_q
            

        if add_items is None:
            add_items = self.def_items


        for key,val in add_items.items():

            item_q = val[0]
            if key in self.items:
                self.items[key] += item_q
            else:
                self.items[key] = item_q


        self.sortItems()
        self.possible_items = {}

    def sortItems(self):
        descriptor = params.ITEMS_DESCRIPTION_DICT
        items_out = {}
        for key,val in self.items.items():
            if(descriptor.get(key)[2]=="a"):
                print("Adding action ", key, " to ",self.name)
                self.actions[key] = val
                
                
            if(descriptor.get(key)[2]=="p" or descriptor.get(key)[2]=="t"): #if object is temporary or permanent we keep is as item
                items_out[key] = val


            
        self.items = items_out
        pass
    


    def returnNameWithoutUnderscore(self):
        name = self.name
        out = ""
        for l in name:
            if l == "_":
                out += " "
            else:
                out +=l
        return(out)
    
    
    def update_image(self):
        img = pygame.image.load(self.image_path).convert_alpha()
        scaled_image = pygame.transform.scale(img, (params.ROOM_TILE_SIZE, params.ROOM_TILE_SIZE))


        rot =  90*(self.room_rotation)  # pour affichage
        self.IMAGE = pygame.transform.rotozoom(scaled_image, rot, 1)


        img = pygame.image.load(self.image_path).convert_alpha()
        scaled_image = pygame.transform.scale(img, (params.BIG_TILE, params.BIG_TILE))


        rot =  90*(self.room_rotation)  # pour affichage
        self.BIG_IMAGE = pygame.transform.rotozoom(scaled_image, rot, 1)

    def rotate_90_trigo(self,keepRef=True):
        """
        Fait tourner la pièce de 90° dans le sens trigonométrique :
        - Met à jour les portes [E, N, W, S]
        - Incrémente room_rotation (dans le sens anti-horaire)
        """
        
        # [E, N, W, S] devient [N, W, S, E]
        self.doors = [self.doors[3], self.doors[0], self.doors[1], self.doors[2]]
        self.room_rotation = (self.room_rotation +1)%4
       # print("dada: ",self.door_status)
        self.door_status =[self.door_status[3], self.door_status[0], self.door_status[1], self.door_status[2]]
      
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
        return f"<{self.name} ({self.color}) DStat={self.door_status}>"
    
