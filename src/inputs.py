from src import params
from src import handler
import pygame


class HandleInputs(handler.BaseHandler):
    """
    Gère toutes les entrées clavier du jeu. Hérite de BaseHandler

    Cette classe :
        - lit les événements Pygame (KEYDOWN, KEYUP, QUIT)
        - met à jour les flags de HandleData (space_pressed, enter_pressed, interact, etc.)
        - gère les changements de direction du joueur
        - gère la navigation dans l’inventaire et la sélection de salles lors du tirage
        - active les effets sonores (click, small_click) via des flags
        - contrôle l’accès aux actions selon le mode de la state machine

    Modes importants :
        mode == 0 : mode navigation/mouvement/interaction chambre
        mode == 1 : mode sélection des 3 nouvelles salles (room draft)
    """

    def __init__(self,data):
        """
        Initialise le gestionnaire d’entrées.

        Args:
            data: Instance de HandleData contenant toutes les variables globales.
        """
        super().__init__(data)
        # Dictionnaire des touches pressées pour cette frame
      

    def update(self):
        """
        Analyse chaque événement Pygame et met à jour les différents flags du jeu.

        Aucun traitement de logique n'est fait ici :
        HandleInputs se limite à modifier des signaux dans self.data.
        """


        for event in pygame.event.get():
            
            # Fermeture fenêtre
            if event.type == pygame.QUIT:
                self.data.keep_running = False # arrêt jeu
                print("exit")

            # Touche pressée
            if event.type == pygame.KEYDOWN:
            
                
                # On/Off musique avec touche M
                if event.key == pygame.K_m:
                    self.data.music_play = not self.data.music_play
                

                # Barre espace : déplacement / validation ouverture de porte
                if event.key == pygame.K_SPACE:
                    if(self.data.state_machine.mode==0):
                        self.data.click_play = True
                        self.data.space_pressed = True
                    else:
                        self.data.space_pressed = False


                # Touche R : redraft (si dés disponibles)
                if event.key == pygame.K_r:
                    if(self.data.state_machine.mode==1 and self.data.player.inventory.getItemQ("dice") > 0):
                        self.data.redraft_pressed = True
                    else:
                        self.data.redraft_pressed = False


                # Touche F : interaction objets salle (dig, trunk, locker...)
                if event.key == pygame.K_f:
                    if(self.data.state_machine.mode==0): # si en mode interaction alors:
                        self.data.interact_pressed = True # input/flag mis à jour
                        self.data.interact_play = True
                    else:
                        self.data.interact_pressed = False

                # Entrée : choisir une salle en mode tirage
                if event.key == pygame.K_RETURN:
                    if(self.data.state_machine.mode==1):
                        self.data.enter_pressed = True
                        self.data.click_play = True
                    else:
                        self.data.enter_pressed = False  


                # ---- Mouvement du curseur en mode 0 ----
                # POSSIBLE EN QWERTY OU AZERTY

                if event.key == pygame.K_d: 
                    if(self.data.state_machine.mode==0):  
                        self.data.player.direction = 0 # regarder vers le L'EST
                        self.data.small_click_play = True#sfx
                        self.data.gridHandler.updateRoomAndNextRoom()# met à jour la "prochaine chambre" relative au joueur
                    

                if event.key == pygame.K_w or  event.key == pygame.K_z :
                    if(self.data.state_machine.mode==0):  
                        self.data.player.direction = 1 # regarder vers le NORD
                        self.data.small_click_play = True #sfx
                        self.data.gridHandler.updateRoomAndNextRoom() # met à jour la "prochaine chambre" relative au joueur

                if event.key == pygame.K_a or  event.key == pygame.K_q:
                    if(self.data.state_machine.mode==0):  
                        self.data.small_click_play = True#sfx
                        self.data.player.direction = 2 # regarder vers l'OUEST
                        self.data.gridHandler.updateRoomAndNextRoom()# met à jour la "prochaine chambre" relative au joueur
                       
                if event.key == pygame.K_s:
                    if(self.data.state_machine.mode==0):  
                        self.data.small_click_play = True#sfx
                        self.data.player.direction = 3 # regarder vers le SUD
                        self.data.gridHandler.updateRoomAndNextRoom()# met à jour la "prochaine chambre" relative au joueur


                # ---- Défilement inventaire salle (mode 0) ----

                if event.key == pygame.K_DOWN: #flèche vers le bas
                    if(self.data.state_machine.mode==0):
                        
                        self.data.counter_inventory +=1 

                        x,y = self.data.player.x,self.data.player.y
                        current_room = self.data.gridHandler.grid[x][y]

                        # Récupère nombre total d’objets/action par chambre = limite de défilement
                        count_items = len(current_room.inventory.items) + len(current_room.inventory.actions)

                        var = count_items

                        if(self.data.counter_inventory>=var): #si on dépasse
                            self.data.counter_inventory = 0 # remet à zéro le curseur 
                            
                        
                if event.key == pygame.K_UP: #flèche vers le haut
                    if(self.data.state_machine.mode==0):
                        self.data.counter_inventory += -1

                        x,y = self.data.player.x,self.data.player.y
                        current_room = self.data.gridHandler.grid[x][y]


                        # Récupère nombre total d’objets/action par chambre = limite de défilement
                        count_items = len(current_room.inventory.items)+ len(current_room.inventory.actions)
                        var = count_items
                        if(self.data.counter_inventory<0):
                            self.data.counter_inventory = var-1 # on place le curseur à la fin


                # ---- Sélection des 3 salles tirées (mode 1) ----

                if event.key == pygame.K_RIGHT:
                    if(self.data.state_machine.mode==1):
                        self.data.small_click_play = True

                        self.data.counter_room_selection_cursor +=1
                        
                        if(self.data.counter_room_selection_cursor >=3):  # remise à zérro du curseur
                             self.data.counter_room_selection_cursor = 0

                if event.key == pygame.K_LEFT:
                    if(self.data.state_machine.mode==1):
                        self.data.small_click_play = True
                      
                        self.data.counter_room_selection_cursor -=1
                        if(self.data.counter_room_selection_cursor <0):
                             self.data.counter_room_selection_cursor = 2

        
