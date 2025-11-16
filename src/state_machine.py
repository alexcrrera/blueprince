from src import params
from src import handler

class StateMachineHandler(handler.BaseHandler):
    """
    Gère la logique de haut niveau du jeu à l’aide d’une machine à états.

    États principaux :
        mode = 0 : déplacement du curseur / navigation dans le manoir
        mode = 1 : sélection des 3 salles lors d’un tirage
       

    La StateMachine :
        - décide si on entre dans une salle ou si on doit générer 3 salles
        - gère le redraft
        - gère les interactions dans les salles
        - applique les effets d’entrée dans certaines salles
        - coordonne Player, Inventory et RoomGrid

    Hérite aussi de BaseHandler
    """

    def __init__(self,data):
        """
        Initialise la machine à états.

        Args:
            data: Instance HandleData contenant tout l’état du jeu.
        """
        super().__init__(data)
    
        self.generate_random_rooms_flag = False  # signal pour RoomGrid
        self.mode = 0  # 0 = curseur, 1 = tirage des salles


    def updateNextRoomCursor(self):
        """
        Calcule la position de la prochaine pièce en fonction de la direction du joueur.
        Contraintes :
            - empêcher de sortir de la grille
            - corriger automatiquement la direction si collision avec bord
            - mettre à jour next_room_position
            - demander à RoomGrid de mettre à jour current_room et next_room
        """
        direction = self.data.player.direction


        # calcul du dx,dy à réaliser par le jouer pour se déplacer selon sa direction
        dx,dy = 0,0


        if(direction==0): dx = 1 # on se déplace vers l'EST
        elif(direction==1): dy = -1  # on se déplace vers l'OUEST
        elif(direction==2): dx = -1 # on se déplace vers le NORD
        elif(direction==3): dy = +1 # on se déplace vers le SUD

        out =[self.data.player.x+dx,self.data.player.y+dy]

        x,y = out[0],out[1]

        # Gestion des collisions avec les bords

        if(x<0): # si MUR WEST 
            out[0] = out[0]+2
            self.data.player.direction = 0
            
        if(x>params.ROOM_GRID_SIZE_HORIZONTAL-1): # si MUR EST 
            out[0] = out[0]-2
            self.data.player.direction = 2

        if(y<0): # si MUR NORD 
            out[1] += 2
            self.data.player.direction =3

        if(y>params.ROOM_GRID_SIZE_VERTICAL-1): # si MUR SUD 
            out[1] +=-2
            self.data.player.direction =1

        # Rebornage défensif, rédondant mais bon...
        out[0] = min(out[0],params.ROOM_GRID_SIZE_HORIZONTAL-1)
        out[0] = max(0,out[0])
        out[1] = min(out[1],params.ROOM_GRID_SIZE_VERTICAL-1)
        out[1] = max(0,out[1])

        # out forcément à l'intérieur du Manoir. Si ceci n'est pas le cas, nous aurions un index error lors de la lecture du "grid" (liste)
        
        
        # Mise à jour des références pièce actuelle / prochaine
        self.data.player.next_room_position = out

        self.data.gridHandler.update()



    def cursorSpacePressed(self):
        """
        Gestion de la barre espace en mode curseur (mode 0).

        Selon next_room_status :
            - -1 > pièce vide > générer 3 salles
            - 1  > pièce ouverte > entrée dans la pièce
            - 2  > porte verrouillée > utiliser 1 clef ou lockpick
            - 3  > porte double verrou > nécessite 1 clef
        """
        self.data.space_pressed = False # flag réinitialisée

        # Cas 1 : pièce vide > générer 3 salles
        if(self.data.player.next_room_status ==-1):
            self.data.state_machine.generate_random_rooms_flag = True
            self.data.gridHandler.generateRandomRooms()
            self.mode = 1 # mode choix chambre
            return

        # Cas 2 : porte ouverte > on entre
        elif(self.data.player.next_room_status ==1):

            self.data.enter_room_play = True # son quand on rentre dans une salle
      
            self.mode = 0 # toujours mode mouvement
            self.data.player.next_room_status =0 

            # Mise à jour position du joueur, du curseur, de prochaine chambre et chambre actuelle
            self.data.player.x = self.data.player.next_room_position[0]
            self.data.player.y = self.data.player.next_room_position[1]
            self.updateNextRoomCursor()
            self.data.gridHandler.updateRoomAndNextRoom()

            # Coût d’entrée et effet GYMNASIUM

            if(self.data.gymnasium_effet):
                steps_lost = 2
            else:
                steps_lost = 1


            self.data.player.inventory.removeItems("steps_left",steps_lost)
            self.data.counter_inventory = 0

            # Effets d’entrée dans une salle
            room = self.data.gridHandler.grid[self.data.player.x][self.data.player.y]
            self.handleRoomEntryEffects(room)
            return
                    
        # Cas 3 : porte simple verrou
        elif(self.data.player.next_room_status ==2):

            if(self.data.player.inventory.getItemQ("keys")>0):
                # utilisation clef ou lockpick
                if(not self.data.player.inventory.getItemQ("lockpick")>0): #pas de lockpick dans inventaire donc faut utiliser une clef
                    self.data.updateDebugText(f"You use a key to open the door")
                    self.data.player.inventory.removeItems("keys",1)
                else:
                    self.data.lockpick_used_play = True #sfx lockpick
                    self.data.updateDebugText(f"You use the lockpick and open the door")

                self.data.door_locked_play = True #sfx ouverture porte à un tour
                self.data.gridHandler.openDoor()

        # Cas 4 : porte double verrou
        elif(self.data.player.next_room_status ==3):
            if(self.data.player.inventory.getItemQ("keys")>0):
                    self.data.player.inventory.removeItems("keys",1)
                    self.data.door_locked_play = True
                    self.data.gridHandler.openDoor()


    def handleRedraft(self):
        """
        Gère le "redraft" : le joueur dépense un dé ('dice') pour reroll les 3 salles.
        """
        self.data.room_redraft_play = True # sfx reroll
        self.data.redraft_pressed = False # flag réinitialisée
        self.data.dark_room_effect = False # effet plus actif si chambre non draftée
        self.data.player.inventory.removeItems("dice",1,keep_item=True)
        self.data.updateHistory("dice",1,verb="use")
        
        self.data.state_machine.generate_random_rooms_flag = True
        self.data.gridHandler.generateRandomRooms() 


    def handleRoomSelectedWithEnter(self):
        """
        Le joueur sélectionne l’une des 3 salles proposées.
        Cette fonction :
            - vérifie le coût en gemmes
            - retire les gemmes
            - place la salle dans la grille
            - revient en mode curseur
        """
        self.data.enter_pressed = False
        #récupère chambre choisie par curseur
        room = self.data.gridHandler.randomGeneratedRooms[self.data.counter_room_selection_cursor]
        cost = room.cost #coût

        # Vérification ressources
        if(self.data.player.inventory.getItemQ("gems")-cost<0):
            return

        # mise à jour inventaire
        self.data.player.inventory.removeItems("gems",cost,keep_item=True)
        self.data.updateHistory("gems",cost,verb="use") # You use 1 gem > la chambre coûte une gemme - pour UI

        # Placement final
        x = self.data.player.next_room_position[0]
        y = self.data.player.next_room_position[1]
        self.data.gridHandler.handlenewRoom(x,y) # gestion finale de la nouvelle chambre

        # Retour au mode curseur
        self.room_selection_mode = False
        self.cursor_selection_mode = True
        self.mode = 0



    def handleRoomEntryEffects(self,room):
        """
        Applique les effets d’entrée dans certaines pièces spéciales.
        """
        name = room.name

        if name == "Chapel": # perte 1 de or lors que l'on rentre
            self.data.player.inventory.removeItems("gold",1)
            self.data.updateDebugText("You lose 1 x coin")
        
        if name == "Bedroom": # donne deux pas lorsque l'on rentre
            self.data.player.inventory.addItem("steps_left",2)
            self.data.updateDebugText("You gain 2 x steps")
            return


    def handleInteraction(self):
        """
        Gère l'interaction (touche F) avec les objets dans une salle :
            - actions (dig, locker, trunk…)
            - items (ramasser un objet)
        """
        if(not self.data.interact_pressed):
            return

        self.data.interact_pressed = False

        current_room = self.data.gridHandler.current_room
        count_items = len(current_room.inventory.items) + len(current_room.inventory.actions) # combien d'items en total

        if(count_items==0):
            return

        cursor_pos = self.data.counter_inventory # récupère position curseur

        # On distingue actions (en haut de la liste) et items (en bas)
        if(cursor_pos > len(current_room.inventory.actions)-1): # cas ici: curseur dans la partie "items" et non actions
            cursor_pos_rel = cursor_pos - len(current_room.inventory.actions)  # mise à jour du curseur - position relative en fonction de si gestion item ou action
            self.interactWithItem(current_room,cursor_pos_rel) # méthode pour intéragir avec un item
        else:
            self.interactWithAction(current_room,cursor_pos) # méthode pour intéragir avec une action


    def interactWithItem(self,current_room,cursor_pos):
        """
        Le joueur ramasse un item depuis la salle.
        """
        ind = 0
        items_dict = current_room.inventory.items.copy()

        for item,q in items_dict.items(): # on itère over le dictionnaire - déterministe une si inchangé (on aura le même ordre des items tant que rien n'est modifié dans le dictionnaire)
            if ind == cursor_pos: 
                self.data.player.inventory.addItem(item,q) # ajoute q quantité de item au inventory du joueur
                current_room.inventory.removeItems(item,q,self.data) # enlève item du inventory de la chambre
                return
            ind += 1


    def interactWithAction(self,current_room,cursor_pos):
        """
        Le joueur interagit avec une action de la salle
        (ouvrir trunk, locker, dig, package, etc.)
        """
        ind = 0
        actions_dict = current_room.inventory.actions.copy()

        for action,_ in actions_dict.items(): #même logique que pour les items
            if ind == cursor_pos:

                reply = self.data.gridHandler.checkIsInteractionPossible(action) # on vérifie s'il est possible de réaliser cette action

                if(reply=="ok"):
                    self.data.gridHandler.doAction(action) # si oui, on réalise l'action
                    current_room.inventory.removeActions(action,1) # mise à jour de l'inventaire
                else:
                    self.data.updateDebugText(reply) # sinon on montre sur l'UI pourquoi ("You need a shovel...")

                return

            ind += 1


    def update(self):
        """
        Méthode principale appelée chaque frame.

        Selon self.mode :
            0 > mode curseur (déplacement + interaction)
            1 > mode sélection des 3 salles tirées
            2 > placeholder
        """
        if(self.mode ==0):
            # Mode navigation
            self.data.dark_room_effect = False # cet effet n'est appliqué lors du drafting actif de la chambre Darkroom
            self.updateNextRoomCursor() # mise à jour du curseur pour la prochaine chambre

            if(self.data.space_pressed):
                self.cursorSpacePressed() # gestion de touche espace 
            else:
                self.handleInteraction()
                
        elif(self.mode==1):
            # Mode sélection des salles
            if(self.data.redraft_pressed):
                self.handleRedraft() # gestion du reroll
                
            elif(self.data.enter_pressed):
                self.handleRoomSelectedWithEnter() # gestion de touche enter 

 
