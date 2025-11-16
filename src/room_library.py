from src.room import Room  # import la classe Room from room.py
from src import params

import random


class RoomGrid():
    """
    Gère la totalité de la grille du manoir (5 × 9), la génération des pièces,
    le suivi de la pièce actuelle, et la logique associée aux portes et effets.

    Cette classe est responsable de :
        - stocker toutes les pièces du manoir
        - tirer et placer les nouvelles salles
        - vérifier la validité des connexions de portes
        - appliquer les effets globaux (greenhouse, furnace, etc.)
        - gérer les interactions (openDoor, doAction, etc.)
    """

    def __init__(self,data):
        """
        Initialise la grille du manoir, place l'Entrance Hall et l'Antechamber,
        et prépare les structures nécessaires au tirage de pièces.

        Args:
            data: Référence au gestionnaire global (HandleData)
        """
        self.data = data

        # Création de la grille (5 × 9)
        self.grid = [[None for _ in range(params.ROOM_GRID_SIZE_VERTICAL)] for _ in range(params.ROOM_GRID_SIZE_HORIZONTAL)]

        # Données JSON source
        self.rooms_data  = params.DICT_ROOM_ATTRIBUTES

        # Placement initial des deux salles fixes
        self.grid[2][8] = Room("Entrance_Hall",self.rooms_data ,2,8,data=self.data)
        self.grid[2][0] = Room("Antechamber",self.rooms_data ,2,0,data=self.data)

    
        # Contiendra les 3 salles proposées lors du tirage
        self.randomGeneratedRooms = []

        # Références utilitaires
        self.current_room = self.grid[self.data.player.x][self.data.player.y] # chambre actuelle
        self.next_room = self.grid[self.data.player.next_room_position[0]][self.data.player.next_room_position[1]] # prochaine chambre relative au jouer

        # Statut de porte par défaut
        # -1 = vide, 0 = mur, 1 = ouverte, 2 = verrouillée, 3 = double-verrou
        self.next_room_status = -1



    def countRoomsInManor(self):
        """
        Compte le nombre de pièces déjà placées dans le manoir.
        Utile notamment pour l’effet “Master Bedroom”.

        Returns:
            int: Nombre de salles non vides.
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
            int: Statut de porte :
                 -1 : vide mais générable
                  0 : mur
                  1 : ouverte
                  2 : verrouillée
                  3 : double-verrou
        """
        next_room = self.next_room  
        current_room = self.current_room

        dir =  self.data.player.direction
        dir_opposed = (dir+2)%4 # direction opposée à celle où on regarde

        # Cas 1 : pièce absente > possible génération
        if next_room is None:
            if(current_room.doors[self.data.player.direction]==1): # si porte existe
                if(current_room.door_status[dir]==1): # si porte ouverte
                    return -1 # retourne 1 - possible générer chambre
                else:
                    return current_room.door_status[dir] # sinon retoure statut porte
            else:
                return 0  # Mur ou pas de porte

        # Cas 2 : les deux pièces existent > vérifier cohérence portes/statuts
        #  Nous allons vérifier les statuts de la porte par laquelle nous allons passer dans notre chambre et l'autre de la prochaine chambre
        # Si notre porte est au NORD, alors la prochaine porte à vérifier de la prochaine chambre est celle du SUD
        curr_door_stat = current_room.door_status[dir]
        next_door_stat = next_room.door_status[dir_opposed]

        if(self.checkDoorsConnectionExists(next_room)): # S'il y a deux portes entre les chambres
                if(curr_door_stat==1 or next_door_stat ==1): # si une porte est ouverte alors les deux le sont - évite devoir reouvrir des portes si on passe "de l'autre côté"
                    next_room.door_status[dir_opposed] = 1
                    current_room.door_status[dir] = 1
                    return 1
                else:
                    out = max(curr_door_stat,next_door_stat) # si chambre 1 = bloquée à un tour et chambre 2 à double -> statut final = bloqué à double tour  rend plus difficile le jeu
                    current_room.door_status[dir] = out # mise à jour du statut
                    next_room.door_status[dir_opposed] = out
                    return(out)

        return 0 # mur



    def checkDoorsConnectionExists(self,room):
        """
        Vérifie si une connexion porte-porte est possible entre la pièce actuelle
        et une pièce candidate.

        Args:
            room (Room): Candidate à placer.

        Returns:
            int: 1 si les portes existent dans les deux directions, sinon 0.
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
        Tire une salle aléatoire selon rareté, contraintes de placement et exclusions.

        Args:
            initial_rotation (int): Rotation donnée par la direction du joueur.
            exclusions (set): Noms de salles à exclure (doublons, Antechamber, Entrance_Hall).

        Returns:
            Room: Instance temporairement générée.
        """
        excluded_rooms = ["Antechamber", "Entrance_Hall"]
        pioche = []  # stockage des chambres admissibles

        for name, data in self.rooms_data.items(): # on itère suur toutes les  chambres dans room.json

            if name in excluded_rooms or name in exclusions: #exclusion chambres 
                continue

            # Quantité disponible - on ne considère que les chambres avec q>0
            q = self.rooms_data[name]["q"]
            if q < 1:
                continue

            # Pour vérification condition de placement
            condition = data["placement_condition"]
            
            # pour effets spéciaux
            color = data["color"]
            
            x,y = self.data.player.next_room_position

            if not (self.checkPlacememtCondition(x0=x,y0=y,cond=condition)==1): #si condition de placement non respectée, chambre non admissible
                continue

            rarity = data["rarity"]

            # Effets Globaux : greenhouse / furnace

            # effet Greenhouse: probabilité plus importante de trouver des chambres vertes
            if(color == "green" and  self.data.green_house_effect):
                rarity = max(0,rarity-1) 

            # effet Furnace: probabilité plus importante de trouver des chambres rouges
            if(color == "red" and  self.data.furnace_effect):
                rarity = max(0,rarity-1)

            weight = 1 / (3 ** rarity) # proba divisée par 3 à chaque incrément de rareté
            pioche.append((name, weight)) #on ajoute à la pioche le nom de la chambre pondéré par une probabilité

        if not pioche:
            raise ValueError("Aucune pièce disponible pour le tirage (toutes exclues).")

        # Tirage pondéré
        name = random.choices(
            [n for n, _ in pioche],
            weights=[w for _, w in pioche],
            k=1
        )[0]

        # Création temporaire
        room = self.createRoomTemp(name,initial_rotation)
        return room


    def createRoomTemp(self, name,rotation=0):
        """
        Crée une instance temporaire de Room à la position next_room.

        Args:
            name (str): Nom de la pièce à instancier.
            rotation (int): Rotation initiale.

        Returns:
            Room: Instance temporaire de Room.
        """
        out = self.data.player.next_room_position
        x = out[0]
        y = out[1]
        return Room(name,self.rooms_data, x, y,rotation,data=self.data)


    def checkPlacememtCondition(self,x0=-1,y0=-1,cond=-1):
        """
        Vérifie les conditions de placement d'une salle.

        Args:
            x0, y0: Coordonnées si room=None.
            cond (int): Code de condition de placement.

        Returns:
            int: 1 si condition respectée, sinon -1.
        """
       
        x = x0
        y = y0
        condition = cond
       

        if condition == 0: # aucune condition 
            return 1
        
        # 1 = uniquement possible gén. dans coins manoir
        if condition == 1:
            c1 = x==0 and y==0
            c2 = x==0 and y==params.ROOM_GRID_SIZE_VERTICAL-1
            c3 = x==params.ROOM_GRID_SIZE_HORIZONTAL-1 and y==0
            c4 = x==params.ROOM_GRID_SIZE_HORIZONTAL-1 and y==params.ROOM_GRID_SIZE_VERTICAL-1
            if c1 or c2 or c3 or c4:
                return 1
        
        # 2 = bords gauche ou droit
        if condition == 2:
            if x==0 or x==params.ROOM_GRID_SIZE_HORIZONTAL-1:
                return 1
        
        # 3 = uniquement moitié Est
        if condition == 3:
            if x > (params.ROOM_GRID_SIZE_HORIZONTAL-1)//2:
                return 1

        return -1


    def generateRandomRooms(self):
        """
        Tire exactement 3 pièces compatibles pour le joueur :
            - respect de la direction
            - portes bien orientées
            - pas de portes vers l’extérieur de la grille
            - s’assure qu’au moins une pièce a coût en gemmes = 0
            - applique les effets de pièces tirées
            - évite les doublons grâce à l’ensemble exclude
        """
        if(self.data.state_machine.generate_random_rooms_flag):
            
            self.data.state_machine.generate_random_rooms_flag = False

            room_output = []
            room_index = 0
            gem_cost_0 = False
            exclude = set()  # évite doublons

            while(room_index<3):

                room_is_ok = False
                attemps = 0  # time-out sécurité

                while(not room_is_ok):
                        room_rotation = 0

                        # Tirage brut
                        new_room = self.drawRandomRoom(self.data.player.direction,exclude)
                        name = new_room.name
                        attemps += 1

                        if(attemps>1000000): # evite boucles infinies
                            raise TypeError("Pas assez de chambres disponibles")
                        if(new_room is None):
                            raise TypeError("Chambre vide générée")

                        # Jusqu'à 4 rotations possibles
                        for _ in range(4):

                            x,y = self.data.player.next_room_position

                            # 1) Vérifier connexion porte > porte
                            if self.checkDoorsConnectionExists(new_room)==1:
                                room_is_ok = True # première condition vérifée

                            # 2) Vérifier aucune porte qui sort de la grille
                            if(x==0 and new_room.doors[2]==1):
                                room_is_ok = False #deuxième condition non respectée
                            if(y==params.ROOM_GRID_SIZE_VERTICAL-1 and new_room.doors[3]==1):
                                room_is_ok = False #3ème condition non respectée
                            if(x==params.ROOM_GRID_SIZE_HORIZONTAL-1 and new_room.doors[0]==1):
                                room_is_ok = False #4ème condition non respectée
                            if(y==0 and new_room.doors[1]==1):
                                room_is_ok = False #5ème condition non respectée

                            # 3) Assurer une salle gratuite parmi les trois
                            if(room_index==2 and not gem_cost_0):
                                room_is_ok = False

                            if(not room_is_ok): # on tourne chambre
                                room_rotation +=1
                                new_room.rotate90Trigo()

                            if(room_is_ok): # chambre validée
                                break

                        if(not room_is_ok):
                            exclude.add(name)

                exclude.add(name)  # empêche doublons
                room_output.append(new_room)

                # Application effets immédiats
                self.handleDraftingRoomEffect(new_room) 
                
                if(new_room.cost<1): # existe chambre telle que coût nul
                    gem_cost_0 = True

                room_index += 1

            self.randomGeneratedRooms = room_output


    def handleDraftingRoomEffect(self,room):
        """
        Applique les effets immédiats des pièces tirées pendant le draft.

        Effets pris en charge :
            - Weight Room : retire 50% des steps
            - Master Bedroom : steps_bonus = nombre de pièces du manoir
            - Darkroom : active blackout
            - Maids Chamber : moins de chance de trouver objets
            - Furnace : augmente probabilité de salles rouges
        """
        if room.name == "Weight_Room":
            player_steps = self.data.player.inventory.getItemQ("steps_left")
            half_steps = (player_steps-player_steps%2)//2 # divise en deux le nombre de pas

            self.data.player.inventory.removeItems("steps_left",half_steps) # divise en deux le nombre de pas
            self.data.updateDebugText(f"The Weight Room drains half of your  steps")
            return
        
        if room.name == "Master_Bedroom":
            # ajoute autant de pas qu'il y a de chambres (générées) dans le manoir
            rooms_in_manor = self.countRoomsInManor()
            self.data.player.inventory.addItem("steps_left",rooms_in_manor)
            txt = "The Master Bedroom gives you " + str(rooms_in_manor) + " steps"
            self.data.updateDebugText(txt)
            return
        
        if room.name == "Darkroom":
            self.data.dark_room_effect = True
            self.data.updateDebugText(f"Darkroom: Everything turns dark...")
        
        if room.name == "Maids_Chamber":
            self.data.updateDebugText("Maid's Chamber: have less chances of finding items...")
            self.data.maid_chamber_effect = True
        
        if room.name == "Furnace":
            self.data.updateDebugText("Furnace: you will draw more red rooms now")
            self.data.furnace_effect = True


    def openDoor(self):
        """
        Ouvre une porte :
            - met à jour le statut de porte côté pièce actuelle
            - synchronise avec la porte opposée si une pièce existe
        """
        current_room  = self.current_room
        dir = self.data.player.direction

        current_room.door_status[dir] = max(1,current_room.door_status[dir]-1) # enlève 1 au statut en bornant par 1 ("ouvert")

        next_room =  self.next_room  
        if(next_room is None):
            return
        
        dir_opposed = (dir+2)%4

        next_room.door_status[dir_opposed] = max(1,next_room.door_status[dir_opposed]-1) # statut minimal est "1" - ouvert
    

    def checkIsInteractionPossible(self,action):
        """
        Vérifie si une interaction (dig, trunk, locker, achat) est possible.

        Returns:
            str: "ok" si action autorisée, sinon message expliquant pourquoi.
        """
        inventory = self.data.player.inventory.items
       
       # nécéssite pêle
        if action == "dig_spots":
            if not "shovel" in inventory:
                return "You need a shovel to dig here"
        
          # nécéssite clef ou marteau
        if action == "trunk":
            if ("keys" in inventory and inventory["keys"]>0) or "hammer" in inventory:
                return "ok"
            else:
                return "You need a key or a hammer to open the trunk"
            
          # nécéssite clef
        if action == "locker":
            if ("keys" in inventory and inventory["keys"]>0):
                return "ok"
            else:
                return "You need a key to open the locker"

        # Gestion achat
        if "_buy" in action:
            item = action.replace("_buy", "") # on récupère le nom de l'objet ("apple_buy" -> "apple")

            if item not in params.POSSIBLE_CONSUMABLES_DICT: # si item non référencé (débug - en pratique jamais vu)
                return "Missing reference"

            cost = params.POSSIBLE_CONSUMABLES_DICT[item]["costs"] # recupère coût associé

            if self.data.player.inventory.getItemQ("gold") - cost < 0: # si pas assez d'or
                return "Not enough coins"

        return "ok"


    def generateBox(self,box_type):
        """
        Génère le contenu d'un coffre, casier ou spot de creusage
        en utilisant generateItems() de la Room.
        """
        possible_items = params.POSSIBLE_ITEMS_PER_ACTION_DICT.get(box_type,{}) # récupère les items possibles par coffre/casier...
    
        self.current_room.generateItems(def_items={}, possible_items=possible_items, box_generation=True)
           
        
    def doAction(self,action):
        """
        Exécute l'action choisie :
            - dig_spots
            - package
            - locker
            - trunk
            - achats (_buy)
        Met à jour :
            - audio (sons)
            - historique (textes)
            - inventaire
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

            
            # affiche texte différent si ouvert avec marteau
            if self.data.player.inventory.getItemQ("hammer")>0:
                self.data.updateDebugText("You open the trunk using the hammer...")
                self.data.hammer_play = True
            else:
                self.data.player.inventory.removeItems("keys",1)

            self.generateBox(action)

        # gère action
        if "_buy" in action:
            item = action.replace("_buy", "")
            cost = params.POSSIBLE_CONSUMABLES_DICT[item]["costs"] # récupère coût associé
            self.data.player.inventory.addItem(item,1) # ajoute item acheté à l'inventaire
            self.data.player.inventory.removeItems("gold",cost) # mise à jour des monnais 


    def __repr__(self):
        """
        Représentation textuelle utile au débogage.
        Liste toutes les pièces déjà placées.
        """
        return "\n".join(room.__repr__() for row in self.grid for room in row if room)
    

    def handlenewRoom(self,x,y):
        """
        Place définitivement la nouvelle salle dans la grille,
        réduit la quantité disponible (q) dans la pioche
        puis applique les effets éventuels d'entrée dans la salle.
        """
        self.grid[x][y] = self.randomGeneratedRooms[self.data.counter_room_selection_cursor]
        newRoom = self.grid[x][y]

        self.rooms_data[newRoom.name]["q"] += -1

        self.applyNewRoomEffect(newRoom)


    def applyNewRoomEffect(self,room):
        """
        Applique les effets passifs au moment où la salle est ajoutée.

        Effets gérés :
            - Veranda
            - Greenhouse
        """
        if room.name == "Veranda":
            self.data.veranda_effect = True
            self.data.updateDebugText("Green rooms will have more gems")

        if room.name == "Greenhouse":
            self.data.updateDebugText("You will draw more green rooms now")
            self.data.green_house_effect= True
   

    def updateRoomAndNextRoom(self):
        """
        Met à jour la pièce actuelle, la pièce suivante et le statut de la porte.
        """
        self.current_room = self.grid[self.data.player.x][self.data.player.y]
        self.next_room = self.grid[self.data.player.next_room_position[0]][self.data.player.next_room_position[1]]
        self.data.player.next_room_status = self.checkRoomDoorStatus()
       
    def update(self):
        """
        Appelé à chaque frame.
        Met simplement à jour :
            - current_room
            - next_room
            - next_room_status
        """
        self.updateRoomAndNextRoom()
