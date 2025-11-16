from src import params
import pygame

from src.inventory import Inventory,RoomInventory
import random



class Room:
    """
    Représente une pièce du manoir.

    Une pièce possède :
        - un nom
        - une couleur (bleue, verte, rouge, etc.)
        - un coût en gemmes
        - une rareté (0 à 3)
        - une quantité disponible (q)
        - une description textuelle
        - une condition de placement
        - une liste de portes (E, N, W, S)
        - des statuts de portes (ouverte, verrouillée simple, double verrou)
        - une liste d’objets générables (définitifs ou aléatoires)
        - un inventaire interne (RoomInventory)
    """

    def __init__(self, name,room_attributes,x,y,orientation=None,data=None):
        """
        Initialise une instance de Room à partir des attributs JSON.

        Args:
            name (str): Nom de la pièce.
            room_attributes (dict): Dictionnaire JSON décrivant toutes les pièces.
            x (int): Position X dans la grille du manoir.
            y (int): Position Y dans la grille du manoir.
            orientation (int or None): Orientation d’entrée (0–3) permettant
                                       une rotation automatique de la salle.
            data: Référence vers l’objet HandleData global.
        """

        self.data = data

        # Chargement des données pour cette pièce
        data =  room_attributes[name] # récupère les données de la chambre
        self.name = name #nom
        self.color = data["color"] #couleur
        self.rarity = data["rarity"]        # rareté: 0=common, 1=standard, 2=unusual, 3=rare
        self.description = data["description"] #description textuelle
        self.placement_condition = data["placement_condition"] #condition de placement
        self.cost = data["cost"] # coût en gemmes de la chambre
        self.image_path = f"assets/images/rooms/{data['image']}" # directory de l'image jpg

        self.cleaned_name = self.returnNameWithoutUnderscore() # Nom lisible sans underscore



        # Définition des portes dans l'ordre [E, N, W, S]
        self.doors = [0, 0, 0, 0]
        self.door_status = []  # Contiendra les statuts associés aux portes

        direction_map = {"E": 0, "N": 1, "W": 2, "S": 3}

        for d in data["doors"]:
            if d in direction_map:
                self.doors[direction_map[d]] = 1





        # Rotation de la pièce
        self.room_rotation = 0

        if orientation is None: # si aucune orienation fournie, alors on ne réalise aucune rotation
            turn = 0
        else:
            if orientation == 0: # si orientation = 0, alors il faut réaliser 270º de rotation pour la chambre. En effet, à l'initialisation, l'image 
                # et les portes sont initialisé "vers le NORD", alors que dans notre système, le "0" est l'"EST".
                turn = 3 #  3 tours = 270º
            else:
                turn = orientation - 1 # pour remettre à "0" . Initialisé "vers le NORD" = 1 -> on fait -1 pour avoir "vers l'EST" = 0 rotation






        # Définition des poids probabilistes pour les niveaux de porte selon la profondeur
        y_max = params.ROOM_GRID_SIZE_VERTICAL-1 

        w_unlocked = 1/(3**(y_max-y)) #poid telle qu'aux premières rangées la probabilité de trouver des chambres débloquées est importante
        w_double_lock = 1/(3**y) # poid telle que au fond du manoir le poid pour les portes bloquées à double tour est minimal mais maximal au dernière rangée
        w_single_lock = 1/2*(w_unlocked + w_double_lock)/2 # le "bloqué à un tour" est la moyenne des deux autres probabilités divisée par deux. 
       
        weights = [w_unlocked,w_single_lock,w_double_lock]
        choices = [1, 2, 3] #choix possibles: 1: débloquée, 2: bloquée à un tour, 3: bloquée à deux tours

        # Génération du statut des portes selon rareté et profondeur
        for d in self.doors:
            if d == 1: # s'il y a une porte
                inter_status = random.choices(choices, weights=weights, k=1)[0] # choix aléatoire entre les 3 choix possible
                self.door_status.append(inter_status)
            else:
                # Pas de porte: statut 0 (mur)
                self.door_status.append(0)




        # Position dans la grille
        self.x, self.y = x, y

        # Application de la rotation initiale (si orientation fournie)
        for _ in range(turn):
            self.rotate90Trigo()

        # Objets possibles et objets définis par défaut dans la pièce
        self.possible_items = data["possible_items"]
        self.def_items = data["items"] # items forcément présents

        # Inventaire propre à la pièce
        self.inventory = RoomInventory({},{},self.data)

        # Génération des objets dans la pièce
        self.generateItems(possible_items=self.possible_items, def_items=self.def_items)

        

        # Mise à jour des portes selon la ligne (haut/bas du manoir) - Conditions aux limites
        self.doorHandleEdgeConditions()

        # Génération des images affichables (small + big)
        self.updateImage()



    def doorHandleEdgeConditions(self):
        """Assure que les conditions aux limites sont bien respectées

        Cette méthode n'est utilisée qu'au début de la génération de la chambre. Une fois placée dans le manoir, elle ne sera plus utilisée.
        
        """
        y= self.y 

        # Mise à jour des portes selon la ligne (haut/bas du manoir)
        y0 = params.ROOM_GRID_SIZE_VERTICAL-1 # y0 tel que nous nous trouvons à la première rangée du Manoir (Entrance Hall)
        
        if(y ==y0): # si dans première rangée
            self.updateDoors(-1,1) # toutes les portes sont ouvertes

        if(y == y0-1): #si deuxième rangées
            self.updateDoors(3,1) # toutes les portes menant au SUD sont ouvertes 

        if(y ==0): # si dans dernière rangée
            self.updateDoors(-1,3) # toutes les portes sont bloquées à deux tours
        if(y == 1): # si dans avant-dernière rangée
            self.updateDoors(1,3) # toutes les portes menant au NORD sont bloquées


    def updateDoors(self,door_to_modify,status):
        """
        Met à jour le statut des portes.

        Args:
            door_to_modify (int): Direction à modifier (0=E, 1=N...), ou -1 pour toutes.
            status (int): Nouveau statut de la porte (1 = ouverte, 2 = verrouillée, 3 = double verrou).
        """
        for i in range(len(self.door_status)):

            if self.doors[i] == door_to_modify or door_to_modify == -1: 
                if(self.door_status[i]!=0): # s'il y a une porte alors on change le statut
                    self.door_status[i] = status




    def generateItems(self,def_items=None,possible_items=None,box_generation=False):
        """
        Génère les objets dans la pièce selon :
            - les objets définis par défaut dans le JSON des Rooms dans le champ "items"
            - les objets possibles, soumis à une probabilité basée sur la rareté
            - les effets globaux (veranda, maid chamber, métal détecteur, etc.) qui modifient les probabilités des tirages

        Args:
            def_items (dict): Objets forcément présents.
            possible_items (dict): Objets possibles.
            action_based (bool): Indique si la génération provient d’une action (creuser/coffre).
            box_generation (bool): Indique s'il s'agit d'une génération d'items provenant d'une "box" (trunk/coffre, colis,  digging spot...) | box = groupe d'items

        """


        descriptor = params.ITEMS_DESCRIPTION_DICT
        txt = "You found:"
        t0 = txt

        # Parcours des objets potentiels
        for item,val in possible_items.items():
            
            rarity_item = int(descriptor.get(item)[3]) #recupère la rareté de l'objet associée

            # Effet Veranda : meilleures chances de gemmes dans les pièces vertes
            if self.color == "green" and self.data.veranda_effect :
                if item == "gems":
                    rarity_item = max(0,rarity_item-1)

            # Effet Maid’s Chamber : baisse générale des chances
            if self.data.maid_chamber_effect:
                rarity_item +=1

            # Détecteur de métal : gold/keys plus faciles
            if(item == "gold" or item == "keys"):
                if (not self.data.player is None):
                    if(self.data.player.inventory.getItemQ("metal_detector")>0):
                        rarity_item = max(0,rarity_item-1)
       
            # Patte de lapin : augmentation générale des chances- peut compenser effet Maid's Chamber
            if (not self.data.player is None):
                if(self.data.player.inventory.getItemQ("rabbits_foot")>0):
                    rarity_item = max(0,rarity_item-1)

            # Tirage pour savoir si l’objet apparaît
           
            # plus la rareté augmente, plus la probilité d'apparaître réduit
        
            proba = 1 / (1 + rarity_item * 0.5) # rarity 1: proba de 67%, 2: 50%, 3: 40$. Évite jeu trop compliqué 
            if random.random() > proba:  #objet non choisit - random.random entre [0,1]
                continue       


            # Détermination de la quantité


            # les objets par chambre dans le Room.json sont définis tq: "item": [q,mode] -> mode = 0: quant. objets dispos=q, mode = 1: quant. objets dispos entre 1,q]
            if val[1] == 0:  # mode 0
                item_q = val[0] 
            else: #mode 1
                item_q = random.randint(1,val[0]) # quantité aléatoire entre 1 et q passé en argument dans le JSON.

            self.inventory.addItem(item,item_q) # ajoute l'item à l'inventaire de la pièce

            if(box_generation): # on affiche de l'info uniquement dans ce cas précis
                item = descriptor.get(item)[0].lower() #récupère texte associé à l'objet - pour UI
                txt +=" " + str(item_q) + " x " + item + "s" # formate text et ajoute s
                if not item_q>1: #  si quantité non sup à 1
                    txt = txt[:-1] if txt.endswith("s") else txt # on enlève le "s"
                txt +="," #virgule pour séparer si plusieurs items générés


        
        

        # Gestion des objets focément présents
        if def_items is None: #si aucun paramètre alors on prent par défaut self.def_items: ceci est le cas lors de la gé
            def_items = self.def_items

        for item,val in def_items.items():
            item_q = val[0]
            self.inventory.addItem(item,item_q)



        self.sortItems() # sépare les objets en deux catégories: temporel et "action" - utile uniquement lors de l'affichage UI

        if(box_generation):
            if txt.endswith(","): #enlève virgule inutile à la fin de la str
                txt = txt[:-1]
            
            if(txt==t0): # si le texte initial n'a pas été mis à jour alors cela veut dire qu'aucun objet n'a été ajouté - on a rien trouvé
                self.data.updateDebugText("You found nothing.")

            else:
                self.data.updateDebugText(txt)


        

    def sortItems(self):
        """
        Trie les objets générés dans la pièce selon leur type :
            - actions ("a")
            - temporaires ("t"), permanents ("p") | différence utile uniquement lors de l'affichage dans l'UI

        et les envoit dans self.inventory.actions ou self.inventory.items respectivement


        """
        items_description = params.ITEMS_DESCRIPTION_DICT
        items_out = {} # dictionnaire temp.

    
        for item,quantity in self.inventory.items.items():

            item_type = items_description.get(item)[2] # récupère type d'item associé 

            # Action utilisable directement dans la salle
            if(item_type=="a"):
                self.inventory.actions[item] = quantity
                
            # Objet temporaire ou permanent stocké comme item
            if(item_type=="p" or item_type=="t"):
                items_out[item] = quantity

        self.inventory.items = items_out



    def returnNameWithoutUnderscore(self):
        """
        Remplace les underscores du nom de la pièce par des espaces. "Room_exemple" devient "Room exemple". Utile pour l'affichage et l'UI

        Returns:
            str: Nom human-readable.
        """
        name = self.name
        text_output = ""

        for letter in name:
            if letter == "_":
                text_output += " " #remplace underscore par un espace
            else:
                text_output +=letter

        return(text_output)
    
    
    def updateImage(self):
        """
        Met à jour les images de la salle :
            - IMAGE (petit format pour la grille)
            - BIG_IMAGE (grand format pour l'affichage latéral)
        en tenant compte de la rotation de la pièce.
        """

        # image pour la grille
        img = pygame.image.load(self.image_path).convert_alpha()
        scaled_image = pygame.transform.scale(img, (params.ROOM_TILE_SIZE, params.ROOM_TILE_SIZE))
        rot =  90*(self.room_rotation) #conversion rotation [0,1,2,3] en [0,90,180,270]º
        self.IMAGE = pygame.transform.rotozoom(scaled_image, rot, 1)

        # image grand format pour affichage bas-droite
        img = pygame.image.load(self.image_path).convert_alpha()
        scaled_image = pygame.transform.scale(img, (params.BIG_TILE, params.BIG_TILE))
        rot =  90*(self.room_rotation)
        self.BIG_IMAGE = pygame.transform.rotozoom(scaled_image, rot, 1)


    def rotate90Trigo(self):
        """
        Fait tourner la pièce de 90° dans le sens trigonométrique.

        La rotation affecte :
            - l’ordre des portes
            - l’ordre des statuts de portes
            - la valeur room_rotation
            - l’image affichée
        """
        #rotation portes: [E, N, W, S] devient [S, E, N, W]
        self.doors = [self.doors[3], self.doors[0], self.doors[1], self.doors[2]]
        self.room_rotation = (self.room_rotation +1)%4 # si rotation = 4, alors elle est mise à 0. Équivalent à faire un tour complet. Wrapping entre 0-3.

        #rotation des statuts des portes également
        self.door_status = [self.door_status[3], self.door_status[0], self.door_status[1], self.door_status[2]]
      

        # mise à jour des conditions limites des portes
        self.doorHandleEdgeConditions()

        # mise à jour de l'image
        self.updateImage()
        
      

    def __repr__(self):
        """
        Fournit une représentation textuelle utile au debug.

        Returns:
            str: Nom + couleur + statuts de portes.
        """
        return f"<{self.name} ({self.color}) DStat={self.door_status}>"
