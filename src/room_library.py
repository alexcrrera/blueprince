from src.room import Room  # import la classe Room from room.py
from src import params

import random


class RoomGrid():
    """
    Gère la totalité de la grille du manoir (5 × 9), la génération des pièces,
    le suivi de la pièce actuelle, et la logique associée aux portes et effets.
    """

    def __init__(self,data):
        """
        Initialise la grille du manoir, place l'Entrance Hall et l'Antechamber,
        et prépare les structures nécessaires au tirage de pièces.

        Args:
            data: Référence au gestionnaire global (HandleData)
        """
        self.space_counter = 0
        self.data = data

        # Grille contenant toutes les pièces (None = case vide)
        self.grid = [[None for _ in range(params.ROOM_GRID_SIZE_VERTICAL)] for _ in range(params.ROOM_GRID_SIZE_HORIZONTAL)]

        # Données brutes issues du JSON
        self.rooms_data  = params.DICT_ROOM_ATTRIBUTES  # dict with room attributes

        # Placement initial des deux pièces fixes du jeu
        self.grid[2][8] = Room("Entrance_Hall",self.rooms_data ,2,8,data=self.data)
        self.grid[2][0] = Room("Antechamber",self.rooms_data ,2,0,data=self.data)

        # Cache pour les images (pas encore utilisé ici)
        self.gridImages = [[None for _ in range(params.ROOM_GRID_SIZE_VERTICAL)] for _ in range(params.ROOM_GRID_SIZE_HORIZONTAL)]

        # Stock temporaire des 3 salles générées
        self.randomGeneratedRooms = []

        # Références vers la pièce actuelle et la prochaine pièce
        self.current_room = self.grid[self.data.player.x][self.data.player.y]
        self.next_room = self.grid[self.data.player.next_room_position[0]][self.data.player.next_room_position[1]]

        # -1 = vide, 0 = mur, 1 = ouverte, 2 = verrouillée, 3 = double-verrou
        self.next_room_status = -1



    def countRoomsInManor(self):
        """
        Compte le nombre de pièces déjà placées dans le manoir.  Utile pour l'effet de Master Bedroom

        Returns:
            int: Nombre de salles non-None dans la grille.
        """
        count = 0
        for col in self.grid:
            for room in col:
                if room is not None:
                    count += 1
        return count


    def checkRoomDoorStatus(self):
        """
        Détermine le statut de la porte entre la pièce actuelle et la prochaine.

        Returns:
            int: Code signifiant le statut de la porte selon la nomenclature :
                 -1 = vide mais générable
                  0 = mur
                  1 = ouverte
                  2 = verrouillée
                  3 = double-verrou
        """
        next_room = self.next_room  
        current_room = self.current_room

        dir =  self.data.player.direction
        dir_opposed = (dir+2)%4

        # Cas où la prochaine pièce n'existe pas encore
        if next_room is None:
            if(current_room.doors[self.data.player.direction]==1):  # une porte existe dans cette direction
                if(current_room.door_status[dir]==1):  # porte ouverte
                    return -1  # on peut générer une pièce
                else:
                    return current_room.door_status[dir]
            else:
                return 0  # mur ou aucune porte

        # Les deux pièces existent : vérifier cohérence des portes
        curr_door_stat = current_room.door_status[dir]
        next_door_stat = next_room.door_status[dir_opposed]

        # Vérification de l’existence des portes dans les deux pièces
        if(current_room.doors[dir] ==1 and  next_room.doors[dir_opposed]==1):
                if(curr_door_stat==1 or next_door_stat ==1):
                    # Si une des deux portes est déjà ouverte, on synchronise
                    next_room.door_status[dir_opposed] = 1
                    current_room.door_status[dir] = 1
                    return 1
                else:
                    # Sinon on retourne le verrou le plus fort des deux
                    out = max(curr_door_stat,next_door_stat)
                    current_room.door_status[dir] = out
                    next_room.door_status[dir_opposed] = out
                    return(out)

        return 0




    def checkDoorsConnectionExists(self,room):
        """
        Vérifie si une connexion porte-porte est possible entre la pièce actuelle
        et une pièce candidate.

        Args:
            room: Objet Room testée.

        Returns:
            int: 1 si les portes existent dans les deux directions, 0 sinon.
        """
        current_room = self.current_room
        next_room = room
        dir =  self.data.player.direction
        dir_opposed = (dir+2)%4

        if(current_room.doors[dir] ==1 and  next_room.doors[dir_opposed]==1):
            return 1

        return 0


    def drawRandomRoom(self, initial_rotation,exclusions):
        """
        Tire une salle aléatoire selon rareté, contraintes de placement et exclusions. Les chambres 

        Args:
            initial_rotation (int): Rotation initiale de la salle.
            exclusions (set): Liste des salles à exclure du tirage.

        Returns:
            Room: La salle temporaire générée et son nom.
        """
        excluded_rooms = ["Antechamber", "Entrance_Hall"]
        pioche = [] # stockage des chambres possibles

        for name, data in self.rooms_data.items():

            # Exclusions directes
            if name in excluded_rooms or name in exclusions: 
                continue # chambres ignorées

            # Vérifie la disponibilité q > 0 - q est la quantité de chambres disponibles dans la pioche
            q = self.rooms_data[name]["q"]
            if(q<1):
                continue

            condition = data["placement_condition"]
            color = data["color"]
            x,y = self.data.player.next_room_position[0],self.data.player.next_room_position[1]

            # Respect des conditions de placement
            if not((self.checkPlacememtCondition(x0=x,y0=y,cond=condition)==1)):
                continue

            rarity = data["rarity"]

            # Effets spéciaux influençant la rareté
            if(color == "green" and  self.data.green_house_effect):
                rarity = max(0,rarity-1)

            if(color == "red" and  self.data.furnace_effect):
                rarity = max(0,rarity-1)

            # Poids basé sur la rareté
            weight = 1 / (3 ** rarity)
            pioche.append((name, weight))


        if not pioche: #si pioche vide, alors erreur
            raise ValueError("Aucune pièce disponible pour le tirage (toutes exclues).")


        # Tirage d'une chambre unique. Tirage pondéré par les poids
        name = random.choices(
            [name for name, _ in pioche],
            weights=[w for _, w in pioche],
            k=1
        )[0]

        room = self.createRoomTemp(name,initial_rotation)
        return room


    def createRoomTemp(self, name,rotation=0):
        """
        Instancie temporairement une Room à la position next_room.

        Args:
            name (str): Nom de la salle.
            rotation (int): Rotation appliquée.

        Returns:
            Room: Instance temporaire.
        """
        out = self.data.player.next_room_position
        x = out[0]
        y = out[1]
        return Room(name,self.rooms_data, x, y,rotation,data=self.data)


    def checkPlacememtCondition(self,room=None,x0=-1,y0=-1,cond=-1):
        """
        Vérifie si les conditions de placement indiquées par la salle sont respectées.

        Args:
            room: Salle testée (sinon utilise x0, y0, cond)
            x0, y0: Coordonnées si room=None
            cond (int): Condition de placement codée.

        Returns:
            int: 1 si condition respectée, -1 sinon.
        """
        if(room==None):
            x = x0
            y = y0
            condition = cond
        else:
            x,y = room.x,room.y
            condition = room.placement_condition

        # 0 = aucune contrainte
        if(condition==0):
            return 1
        
        # 1 = coins uniquement
        if(condition==1):
            c1 = x== 0 and y ==0
            c2 = x== 0 and y == params.ROOM_GRID_SIZE_VERTICAL-1
            c3 = x == params.ROOM_GRID_SIZE_HORIZONTAL-1 and y == 0
            c4 = x == params.ROOM_GRID_SIZE_HORIZONTAL-1 and y == params.ROOM_GRID_SIZE_VERTICAL-1
            if(c1 or c2 or c3 or c4):
                return 1
        
        # 2 = bords gauche ou droit uniquement
        if(condition==2):
            c1 = x== 0 or x == params.ROOM_GRID_SIZE_HORIZONTAL-1
            if(c1):
                return 1
            
        # 3 = moitié Est uniquement
        if(condition == 3):
            if x > (params.ROOM_GRID_SIZE_HORIZONTAL-1)//2:
                return 1

        return -1
   

    def generateRandomRooms(self):
        """
        Gère la sélection complète des 3 salles proposées au joueur lors d'une ouverture de porte :
        - Tire 3 salles compatibles
        - Vérifie alignement des portes
        - Gère rotations
        - Assure qu'au moins une salle a coût en gemmes = 0
        - Stocke les résultats dans randomGeneratedRooms
        """
        if(self.data.state_machine.generate_random_rooms_flag):
            
            self.data.state_machine.generate_random_rooms_flag = False

            room_output = []
            room_index = 0
            gem_cost_0 = False
            exclude = set()  # Pour éviter doublons

            while(room_index<3):

                room_is_ok = False
                attemps = 0 #timeout pour éviter boucle infinie

                while(not room_is_ok):
                        room_rotation = 0

                        # Tirage brut
                        new_room = self.drawRandomRoom(self.data.player.direction,exclude)
                        name = new_room.name
                        attemps +=1

                        if(attemps>100000):
                            raise TypeError("Pas assez de chambres disponibles") # oooops
                        if(new_room is None): 
                            raise TypeError("Chambre vide générée") #ooops x2

                        # Test jusqu'à 4 rotations
                        for _ in range(4):

                            x,y = self.data.player.next_room_position

                            # Vérifie connexion possible
                            if self.checkDoorsConnectionExists(new_room)==1:
                                room_is_ok = True


                            # Vérifie murs du manoir pour éviter d'avoir une porte vers l'extérieur
                            if(x==0 and new_room.doors[2]==1):
                                room_is_ok = False
                                
                            if(y==params.ROOM_GRID_SIZE_VERTICAL-1 and new_room.doors[3]==1):
                                room_is_ok = False

                            if(x==params.ROOM_GRID_SIZE_HORIZONTAL-1 and new_room.doors[0]==1):
                                room_is_ok = False

                            if(y==0 and new_room.doors[1]==1):
                                room_is_ok = False



                            # Au moins une pièce gratuite
                            if(room_index==2 and not(gem_cost_0)):
                                room_is_ok = False




                            if(not room_is_ok):
                                room_rotation +=1
                                new_room.rotate90Trigo()

                            if(room_is_ok):
                                break

                        if(not room_is_ok):
                            exclude.add(name)

                exclude.add(name) # exclure nouvelle chambre pour éviter doublons lors de la génération des 3 chambres

                room_output.append(new_room) 

                # Applique effets spéciaux des salles générées si applicable
                self.handleDraftingRoomEffect(new_room) 
                
                if(new_room.cost<1): # s'il existe une chambre avec un coût de 0, alors set variable a True
                    gem_cost_0 = True

                room_index +=1

            self.randomGeneratedRooms = room_output


    def handleDraftingRoomEffect(self,room):
        """
        Applique les effets immédiats des pièces tirées pendant le draft :
        - Weight Room -> retire des steps
        - Master Bedroom -> ajoute steps
        - Darkroom -> active effet global
        - Maids Chamber -> modifie probabilités d’objets
        - Furnace -> plus de salles rouges
        """
        if room.name == "Weight_Room":
            player_steps = self.data.player.inventory.getItemQ("steps_left")
            half_steps = (player_steps-player_steps%2)//2

            self.data.player.inventory.removeItems("steps_left",half_steps)
            self.data.updateDebugText(f"The Weight Room drains half of your  steps")
            return
        
        if room.name == "Master_Bedroom":
            
            rooms_in_manor = self.countRoomsInManor()
            self.data.player.inventory.addItem("steps_left",rooms_in_manor)
            txt = "The Master Bedroom gives you " + str(rooms_in_manor) + " steps"
            self.data.updateDebugText(txt)
            return
        
        if room.name == "Darkroom":
            self.data.dark_room_effect = True
            self.data.updateDebugText(f"Everything turns dark...")
        
        if room.name == "Maids_Chamber":
            self.data.updateDebugText("You now have less chances of finding items...")
            self.data.maid_chamber_effect = True
        
        if room.name == "Furnace":
            self.data.updateDebugText("You will draw more red rooms now")
            self.data.furnace_effect= True


    def openDoor(self):
        """
        Gère l'ouverture d'une porte :
        - Décrémente le niveau de verrouillage côté pièce actuelle
        - Met à jour la porte opposée dans la pièce suivante si elle existe
        """
        current_room  = self.current_room
        dir = self.data.player.direction
        current_room.door_status[dir] += -1

        next_room =  self.next_room  
        if(next_room is None):
            return
        
        dir_opposed = (dir+2)%4
        next_room.door_status[dir_opposed] = max(1,next_room.door_status[dir_opposed]-1)
    

    def checkIsInteractionPossible(self,action):
        """
        Vérifie si une interaction demandée est possible (dig, trunk, locker, achat).
        Retourne "ok" ou une string expliquant pourquoi ce n’est pas possible.
        """
        current_room  = self.current_room

        inventory = self.data.player.inventory.items
       
        if action == "dig_spots":
            if not "shovel" in inventory:
                return "You need a shovel to dig here"
        
        if action == "trunk":
            if ("keys" in inventory and inventory["keys"]>0) or "hammer" in inventory:
                return "ok"
            else:
                return "You need a key or a hammer to open the trunk"
            
        if action == "locker":
            if ("keys" in inventory and inventory["keys"]>0):
                return "ok"
            else:
                return "You need a key to open the locker"


        if "_buy" in action:
            item = action.replace("_buy", "")

            # Vérifie référence
            if (not item in params.POSSIBLE_CONSUMABLES_DICT):
                return("Missing reference")

            cost = params.POSSIBLE_CONSUMABLES_DICT.get(item).get("costs")

            if(self.data.player.inventory.getItemQ("gold")-cost<0):
                return("Not enough coins")

        return "ok"


    def generateBox(self,box_type):
        """
        Génère le contenu d’un coffre / casier / spot de creusage en utilisant
        la fonction generateItems() d’une Room.
        """
        possible_items = params.POSSIBLE_ITEMS_PER_ACTION_DICT.get(box_type,{})
        current_room  = self.current_room

        current_room.generateItems(def_items={} ,possible_items=possible_items,box_generation=True)
           
        
        
            
    def doAction(self,action):
        """
        Exécute réellement l’action demandée (ouvrir, creuser, acheter, etc.).
        Gère aussi les sons associés et les messages de debug.
        """
        if action == "dig_spots":
            self.data.shovel_play = True
            self.generateBox(action)
            self.data.updateDebugText("You dig...")
            
        if action == "package":
            self.data.mail_play = True    
            self.data.updateDebugText("You open the mysterious package...")
            self.generateBox(action)

        if action == "locker":
            self.data.locker_play = True    
            self.data.updateDebugText("You open the locker...")
            self.generateBox(action)

        if action == "trunk":
            self.data.trunk_play = True

            if self.data.player.inventory.getItemQ("hammer")>0:
                self.data.updateDebugText("You open the trunk using the hammer...")
                self.data.hammer_play = True
            else:
                self.data.player.inventory.removeItems("keys",1)

            self.generateBox(action)

        if "_buy" in action:
            item = action.replace("_buy", "")
            cost = params.POSSIBLE_CONSUMABLES_DICT.get(item).get("costs")
            self.data.player.inventory.addItem(item,1)
            self.data.player.inventory.removeItems("gold",cost)


    def __repr__(self):
        """
        Retourne une représentation lisible de toutes les salles du manoir.
        """
        return "\n".join(room.__repr__() for row in self.grid for room in row if room)
    

    def handlenewRoom(self,x,y):
        """
        Place définitivement la salle sélectionnée dans la grille,
        retire 1 unité de disponibilité (q) de son type,
        puis applique ses effets d’entrée.
        """
        self.grid[x][y] = self.randomGeneratedRooms[self.data.counter_room_selection_cursor]
        newRoom = self.grid[x][y]

        self.rooms_data[newRoom.name]["q"] +=-1 

        self.applyNewRoomEffect(newRoom)

    def applyNewRoomEffect(self,room):
        """
        Applique certains effets immédiats lorsqu’une salle est ajoutée au manoir :
        - Veranda : augmente chances de gemmes dans rooms vertes
        - Greenhouse : augmente probabilité de tirer des rooms vertes
        """
        if room.name == "Veranda":
            self.data.veranda_effect = True
            self.data.updateDebugText("Green rooms will have more gems")

        if room.name == "Greenhouse":
            self.data.updateDebugText("You will draw more green rooms now")
            self.data.green_house_effect= True
   

    def updateRoomAndNextRoom(self):
        """
        Met à jour la pièce actuelle, la prochaine pièce, et calcule le statut
        de la porte entre les deux.
        """
        self.current_room = self.grid[self.data.player.x][self.data.player.y]
        self.next_room = self.grid[self.data.player.next_room_position[0]][self.data.player.next_room_position[1]]
        self.data.player.next_room_status = self.checkRoomDoorStatus()
       
    def update(self):
        """
        Méthode appelée à chaque frame.
        Met à jour uniquement current_room, next_room et next_room_status.
        """
        self.updateRoomAndNextRoom()