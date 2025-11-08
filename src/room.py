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

    def __init__(self, name,room_attributes,x,y,orientation=None,data=None):
        """
        data = dictionnaire venant du JSON
        """



        #print("Created: ",name)
        self.data = data
        data =  room_attributes[name]
        self.name = name
        self.color = data["color"]
        self.rarity = data["rarity"] # 0 = common ,  1 = standard , 2 = unusual ,  3 = rare
        self.q = data["q"]
        self.description = data["description"]
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
     


        #self.randomObjectsGeneration()
        self.inventory = RoomInventory({},{},self.data)
        self.generateItems()
        

      
        
        #self.room_inventory = Inventory()


        self.x, self.y = x, y

        y0 = params.ROOM_GRID_SIZE_VERTICAL-1
        if(y ==y0):
            self.updateDoors(-1,1)
        if(y == y0-1):
            self.updateDoors(3,1) # porte du sud forcément ouverte (si pas un mur)



        if(y ==0):
            self.updateDoors(-1,3)
        if(y == 1):
            self.updateDoors(1,3) # porte du sud forcément ouverte (si pas un mur)

        self.update_image()




    def updateDoors(self,door,status):

        for i in range(len(self.door_status)):
            if self.doors[i] == door or door == -1:
                 if(self.door_status[i]!=0):
                    self.door_status[i] = status
    





    def generateItems(self,def_items=None,possible_items=None,action_based=False):
        # si on ne passe pas en argument def_items, alors def_items = self.def_items
        # même chose pour possible_items

        # cela veut dire qu'il suffit de passer en argument def_items={}  si on ne souhaite pas ajouter d'items definitifs
        if possible_items is None:
            possible_items = self.possible_items

        descriptor = params.ITEMS_DESCRIPTION_DICT
        txt = "You found:"
        t0 = txt

        for key,val in possible_items.items():
            
            rarity_item = int(descriptor.get(key)[3])


            if(key == "gold" or key == "keys"):
                print("item ",key)

                if (not self.data.player is None):
                    if(self.data.player.inventory.getItemQ("metal_detector")>0):
                        rarity_item = max(0,rarity_item-1) # on augmente les chances de trouver des items rares
       

            if (not self.data.player is None):
                if(self.data.player.inventory.getItemQ("rabbits_foot")>0):
                    print("Lucky rabbit's foot found - increasing chances of finding items")
                    rarity_item = max(0,rarity_item-1) # on augmente les chances de trouver des items rares - effet cumulé avec metal detector
            
            rand_choice =  random.randint(0,rarity_item+1)
            if(rand_choice == 0): #item pas présent dans la salle
                continue
            
            
            if val[1] == 0:
                item_q = val[0]
            else:
                item_q = random.randint(1,val[0])


            #print("To add item: ",key," x",item_q, "dict: ",{key:item_q})
            self.inventory.addItem(key,item_q)

            item = descriptor.get(key)[0].lower()

            txt +=" " + str(item_q) + " x " + item + "s"
            if not item_q>1:
                txt = txt[:-1] if txt.endswith("s") else txt
            txt +=","


        
        if txt.endswith(","):
            txt = txt[:-1]

        if def_items is None:
            def_items = self.def_items


  
        
        for key,val in def_items.items():

            item_q = val[0]
            self.inventory.addItem(key,item_q)

        if(txt==t0):
            txt = "You found nothing."
        self.sortItems()

        self.possible_items = {}
        return(txt)


        




    def sortItems(self):
        descriptor = params.ITEMS_DESCRIPTION_DICT
        items_out = {}
        for key,val in self.inventory.items.items():
            if(descriptor.get(key)[2]=="a"):
                print("Adding action ", key, " to ",self.name)
                self.inventory.actions[key] = val
                
                
            if(descriptor.get(key)[2]=="p" or descriptor.get(key)[2]=="t"): #if object is temporary or permanent we keep is as item
                items_out[key] = val


            
        self.inventory.items = items_out
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

    def rotate_90_trigo(self):
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
        
      
   

    def __repr__(self):
        # Affiche le nom, la couleur, la rareté et le coût - TEST
        return f"<{self.name} ({self.color}) DStat={self.door_status}>"
    
