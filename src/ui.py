import pygame
from src import params
import time
import math

import os
from src import handler




class HandleScreen:
    """
    Gère la fenêtre principale du jeu :
        - ouverture de la fenêtre Pygame
        - chargement de l'icône
        - chargement et affichage du fond d'écran
        - configuration initiale de la résolution
    Une instance unique est utilisée dans le jeu.
    """

    def __init__(self):
        """Initialisation de l'écran, du fond et de l'icône Pygame."""

        ICON_IMAGE_DIR = "assets/images/icon.png"
        ICON_IMAGE  = pygame.image.load(ICON_IMAGE_DIR)

        BACKGROUND_DIR =  "assets/images/ui/background.png" # fond du Jeu
    

        self.width, self.height= params.DEFAULT_SCREEN_WIDTH,params.DEFAULT_SCREEN_HEIGHT #taille image

        # Création de la fenêtre
        self.screen = pygame.display.set_mode((self.width, self.height))
       
        pygame.display.set_icon(ICON_IMAGE)
        pygame.display.set_caption("Blue Prince Emulation")

        # Chargement et scale de l'image de fond
        BACKGROUND = pygame.image.load(BACKGROUND_DIR).convert_alpha()
        scale = pygame.transform.scale(BACKGROUND, (params.screenWidth, params.screenHeight))
        self.BACKGROUND = scale

    

        # Centre la fenêtre (si supporté)
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        
    

    def showBackground(self):
        """Montre le fond d'écran."""
        self.screen.blit(self.BACKGROUND, (0, 0))

    def update(self):
        """Met simplement à jour le fond d’écran."""
        self.showBackground()
        pass




class HandleText(handler.BaseHandler):
    """
    Gère tout l’affichage de texte dans le jeu :
        - inventaire
        - descriptions de salles
        - objets trouvés
        - texte de debug et d'historique
        - suggestions utilisateur (press ENTER, press F, etc.)
        - affichage des coûts des salles en mode draft


    Hérite de BaseHandler
    """

    def __init__(self,data,screen):
        """
        Initialise toutes les polices et stocke les références nécessaires.

        Args:
            data: HandleData
            screen: Surface Pygame sur laquelle dessiner
        """
        super().__init__(data)

        self.screen = screen

        # Tailles de police
        self.default_text_size = params.DEFAULT_FONT_SIZE
        self.special_text_size = params.SPECIAL_FONT_SIZE
        self.small_text_size = params.SMALL_FONT_SIZE
        self.alt_default_text = params.ALT_DEFAULT_SIZE
        

   
        # Chargement de toutes les polices nécessaires
        self.room_status_font = pygame.font.Font(params.DEFAULT_TEXT_DIR, params.ROOM_INFO_TEXT_SIZE)  
        self.default_font = pygame.font.Font(params.DEFAULT_TEXT_DIR, params.DEFAULT_FONT_SIZE)  
        self.special_font = pygame.font.Font(params.SPECIAL_TEXT_DIR, params.SPECIAL_FONT_SIZE)  
        self.small_font = pygame.font.Font(params.SMALL_TEXT_DIR, params.SMALL_FONT_SIZE) 
        self.alt_default_font = pygame.font.Font(params.ALT_DEFAULT_TEXT_DIR, params.ALT_DEFAULT_SIZE) 
        self.inventory_font = pygame.font.Font(params.ALT_DEFAULT_TEXT_DIR, params.INVENTORY_TEXT_SIZE) 
        self.random_group_font = pygame.font.Font(params.ALT_DEFAULT_TEXT_DIR, params.RANDOM_ROOM_TEXT_SIZE) 
        self.dice_suggestion_font  = pygame.font.Font(params.ALT_DEFAULT_TEXT_DIR, params.DICE_SUGGESTION_TEXT_SIZE) 
        self.enter_suggestion_font =  pygame.font.Font(params.ALT_DEFAULT_TEXT_DIR, params.ENTER_SUGGESTION_TEXT_SIZE) 
        self.items_in_room_font = pygame.font.Font(params.ALT_DEFAULT_TEXT_DIR, params.ROOM_TEXT_SIZE) 
        self.items_size_font = pygame.font.Font(params.DEFAULT_TEXT_DIR, params.ITEM_TEXT_SIZE) 
        self.you_found_font = pygame.font.Font(params.DEFAULT_TEXT_DIR, params.YOU_FOUND_TEXT_SIZE) 
        self.history_font = pygame.font.Font(params.DEFAULT_TEXT_DIR, params.HISTORY_TITLES_SIZE) 
        self.items_cursor =  pygame.font.Font(params.ALT_DEFAULT_TEXT_DIR, params.YOU_FOUND_TEXT_SIZE) 
        self.room_description_font = pygame.font.Font(params.ALT_DEFAULT_TEXT_DIR, params.DESCRIPTION_TEXT_SIZE)

        # Stockage pour les items/actions courants
        self.items_length = 0
        self.actions_length = 0

        self.items_descriptor = []
        self.actions_descriptor = []
        
    def showText(self, text, position, font=None, color=params.TEXT_COLOR, center=False, rotation=0):
        """
        Affiche un texte avec rotation et centrage optionnels.

        Args:
            text (str): Texte à afficher.
            position (tuple): Coordonnées d'affichage.
            font: Police à utiliser (default = default_font).
            color: Couleur du texte.
            center (bool): Centrer le texte sur la position.
            rotation (int): Rotation en degrés.
        """

        if font is None:
            font = self.default_font # font par défaut

        rendered_text = font.render(text, True, color) 

        if rotation != 0:
            rendered_text = pygame.transform.rotate(rendered_text, rotation) #tourne text

        text_rect = rendered_text.get_rect()

        if center: # si centrage 
            text_rect.center = position
        else:
            text_rect.topleft = position

        self.screen.blit(rendered_text, text_rect)


    def showNextRoomInfo(self):
        """Affiche l'état de la pièce suivante (mur, vide, verrouillée…)."""
        stat = self.data.player.next_room_status
        txt = ""
        if(stat==-1):
            txt = "Next room is empty - press  space to generate it"
        elif(stat==1):
            txt="Next room is unlocked - press  space to enter"
        elif(stat==2):
            txt="Next room is locked - press  space to enter to use a key"
        elif(stat==3):
            txt="Next room is locked twice - press  space to enter to use one key"
        elif(stat==4):
            txt="I like to boogie"
        elif(stat==0 ):
            txt="There's a wall..."
        elif(stat==-2): # pas utilisé
            txt="That's a nice  wall..."
        self.showText(txt, (params.ROOM_INFO_ORIGIN[0], params.ROOM_INFO_ORIGIN[1]), font=self.room_status_font, color=params.YELLOW)



    def showFPS(self):
        """Affiche les FPS."""

        fps_text = f"FPS: {int(self.data.clock.get_fps())}"
        self.showText(fps_text, (params.screenWidth//2 - params.PADDING_FPS -  self.small_font.size(fps_text)[0],  params.screenHeight - params.PADDING_FPS),font=self.small_font,color=params.BLACK)


    def showPlayerInventoryItems(self):
        """Affiche les valeurs (quantité) des objets de l'inventaire joueur - uniquement items tels que or, gemmes... (non permanents)"""
        
        padding = [i*params.INVENTORY_ITEMS_PADDING for i in range(1,7)]
        
        for i in range(0,5):
            q  = self.data.player.inventory.ui_items[i] # quantité de l'item
            text = str(q)
            col = params.RED if q == 0 else params.WHITE # en rouge si quantité nulle, blanc si supérieur à 0
            self.showText(text, (params.ORIGIN_INVENTORY[0], params.ORIGIN_INVENTORY[1]+padding[i]), font=self.inventory_font, color=col,center=True)



    def showPlayerSpecialItems(self):
        """Affiche les objets spéciaux (permanents) du joueur."""
        x0,y0 = params.ORIGIN_SPECIAL_ITEMS
        padding = params.SPECIAL_ITEMS_PADDING
        
        special_items = self.data.player.inventory.getSpecialItems()
        
        for item,val in special_items.items():
            if(val>0):
                descript = params.ITEMS_DESCRIPTION_DICT.get(item) # description textuelle de l'objet
                txt = descript[0] 
                self.showText(txt, (x0,y0+padding), font=self.items_size_font, color=params.WHITE)
                padding += params.ITEMS_IN_ROOM_PADDING

        if(len(special_items)==0): # si aucun item special
            txt = "No special items in inventory"
            self.showText(txt, (x0,y0+padding), font=self.items_size_font, color=params.LIGHT_GRAY)


    def showRandomRoomsNames(self):
        """Affiche les noms des 3 salles tirées en mode draft."""
        if(self.data.state_machine.mode==1): # uniquement en mode 1
            rooms = self.data.gridHandler.randomGeneratedRooms #récupère les 3 chambres
            x0,y0 = params.ORIGIN_ROOM_RANDOM_TEXT
            x0 += params.RANDOM_GROUP_TILE_SIZE//2
            padding = 0
            
            for (i,r) in enumerate(rooms):
                text = r.cleaned_name
                colr = params.WHITE if i == self.data.counter_room_selection_cursor else params.GRAY # en blanc si curseur dessus, gris sinon - utile pour l'esthétique
                self.showText(text, (x0+padding,y0), font=self.room_description_font, color=colr,center=True)
                padding += params.HORIZONTAL_PADDING_RANDOM_GROUP + params.RANDOM_GROUP_TILE_SIZE
        

    def showRandomRoomCost(self):
        """Affiche le coût en gemmes des salles tirées."""
        if not self.data.state_machine.mode==1:
            return

        rooms = self.data.gridHandler.randomGeneratedRooms #  récupère les chambres aléatoires
        x0,y0 = params.ORIGIN_RANDOM_ROOM_COST
        x0 += (params.RANDOM_GROUP_TILE_SIZE *0.3)//1

        for i in range(3):
            cost = rooms[i].cost
            txt = "costs " + str(cost)
            txt += " gem" + ("" if cost == 1 else "s")

            col = params.WHITE if self.data.player.inventory.getItemQ("gems") >= cost else params.RED # si trop chère alors en rouge, blanc si achetable (assez de gemmes)
            self.showText(txt, (x0,y0), font=self.alt_default_font, color=col)
            
            x0 += params.RANDOM_GROUP_TILE_SIZE+params.HORIZONTAL_PADDING_RANDOM_GROUP
        

    def showCurrentRoomName(self):
        """Affiche le nom de la salle actuelle."""
        if not self.data.state_machine.mode == 0:
            return  
        x,y = self.data.player.x,self.data.player.y
        current_room = self.data.gridHandler.grid[x][y]
        txt = current_room.returnNameWithoutUnderscore() #récupère nom nétoyé de "_"
        x0,y0 = params.ORIGIN_ROOM_TEXT_INFO
        self.showText(txt, (x0,y0), font=self.items_in_room_font)


    def showItemsInRoom(self):
        """
        Affiche la liste des actions et items présents dans la salle actuelle,
        sous forme :
            Nom : xQuantité (description)
        """
        if not self.data.state_machine.mode == 0:
            return
        
        # Titre
        x0,y0 = params.ORIGIN_YOU_FOUND_TEXT
        self.showText("You found:", (x0,y0), font=self.you_found_font) # texte "Tu as trouvé"

        x0 = params.ORIGIN_ITEMS_IN_ROOM[0]
        y0 = params.ORIGIN_ITEMS_IN_ROOM[1]
        x,y = self.data.player.x,self.data.player.y
        current_room = self.data.gridHandler.grid[x][y]

        items_in_room = current_room.inventory.items # récupère items dans la chambre
        actions = current_room.inventory.actions # récupère les actions dans la chambre
        
        descript_dict = params.ITEMS_DESCRIPTION_DICT
        count_items = len(items_in_room) + len(actions) # compte les items en total pour affichage

        if(count_items==0): # il n'y a rien 
            self.showText("Nothing!", (x0,y0), font=self.enter_suggestion_font, color=params.LIGHT_GRAY)
            return
        
        # Stockage des actions/items (sert au curseur)
       
        self.actions_descriptor = []
        self.actions = []

        # format Nom: x1 dig spot (You can dig here...
        for action, value in actions.items():
            desc = descript_dict[action]
            self.actions_descriptor.append(desc[4])
            self.actions.append(action) #  met à jour self.actions - utile pour synchronisation avec le curseur
            txt = desc[0] +" :  x" + str(value) + "  (" + desc[1] + ")"
            self.showText(txt, (x0,y0), font=self.items_size_font)
            y0 += params.ITEMS_IN_ROOM_PADDING

        

        # Items
        self.items_descriptor = []
        for item, value in items_in_room.items():
            desc = descript_dict[item]
            self.items_descriptor.append(desc[4])
            txt = desc[0] +" :  x" + str(value) + "  (" + desc[1] + ")"
            self.showText(txt, (x0,y0), font=self.items_size_font)
            y0 += params.ITEMS_IN_ROOM_PADDING
        
        # mise à jour pour le curseur
        self.items_length = len(items_in_room)
        self.actions_length = len(actions)
        

    def showDiceSuggestion(self):
        """Affiche le message suggérant l'utilisation d'un dé (si disponible)."""
        
        if not self.data.state_machine.mode == 1:
            return

        if not(self.data.player.inventory.getItemQ("dice") >0): # pas de dès disponibles
            col = params.RED
            txt = "No dices left"
        else:
            txt = "Press R to use a die to redraft"
            col = params.WHITE    
        x,y = params.DICE_TEXT_SUGGESTION_ORIGIN
        self.showText(txt,(x,y),font= self.dice_suggestion_font,rotation=270,color=col)


    def showEnterTextSuggestion(self):
        """Affiche les instructions contextuelles (Press F, Press ENTER…)."""

        if(self.data.state_machine.mode == 0):
            if(self.actions_length + self.items_length >0): # s'il y a des items dans la chambre alors affiche suggestion F
                txt  = "Press F to interact"
            else:
                txt = ""
        elif(self.data.state_machine.mode == 1):
            txt  = "Press ENTER to choose a room!"
        else:
            txt  = ""

        x,y = params.ORIGIN_PRESS_ENTER_TEXT
        self.showText(txt,(x,y),font= self.enter_suggestion_font,color=params.LIGHT_GRAY)


    def showItemsCursor(self):
        """
        Affiche le curseur indiquant l'action/item actuellement sélectionné
        via les touches fléchées haut/bas.
        """
        if not self.data.state_machine.mode == 0:
            return  

        x,y = self.data.player.x,self.data.player.y
        current_room = self.data.gridHandler.grid[x][y]

        count_items = len(current_room.inventory.items ) + len(current_room.inventory.actions)
        if count_items == 0:
            return

        # Sécurise la valeur du curseur
        self.data.counter_inventory = min(
            self.data.counter_inventory,
            count_items - 1
        )

        x0,y0 = params.CURSOR_ITEMS_ORIGIN

        col = params.LIGHT_GRAY

        if(self.data.counter_inventory>=self.actions_length):
            # Items
            txt = ">" + self.items_descriptor[self.data.counter_inventory-self.actions_length]
        else:
            # Actions
            if(len(self.actions_descriptor)>0):
                txt = ">" + self.actions_descriptor[self.data.counter_inventory]
                action = self.actions[self.data.counter_inventory]
                # Action impossible → rouge
                if(not self.data.gridHandler.checkIsInteractionPossible(action)=="ok"):
                    col = params.RED
            else:
                return
        
        y0 += params.ITEMS_IN_ROOM_PADDING*self.data.counter_inventory

        self.showText(txt,(x0,y0),font= self.enter_suggestion_font,color=col)


    def showRandomRoomDescription(self):
        """Affiche la description de la salle actuellement sélectionnée en mode draft."""
        if not self.data.state_machine.mode==1:
            return

        rooms = self.data.gridHandler.randomGeneratedRooms
        x0,y0 = params.ORIGIN_RANDOM_ROOM_GROUP_DESCRIPTION
        x0 += (params.RANDOM_GROUP_TILE_SIZE *0.3)//1

        room = rooms[self.data.counter_room_selection_cursor]
        description = room.description # description dans room.json
       
        self.showText(description, (x0,y0), font=self.room_description_font, color=params.WHITE,center=True)


    def showHistory(self):
        """Affiche l'historique court des événements (You gain…, You lose…, etc.)."""
        x,y = params.ORIGIN_HISTORY
        txt = self.data.history_text
        self.showText(txt,(x,y),font= self.history_font,color=params.WHITE,center=True)


    def update(self):
        """Met à jour tous les éléments de texte affichés à l’écran."""
        self.showFPS()
        self.showHistory()
        self.showNextRoomInfo()
        self.showCurrentRoomName()
        self.showPlayerInventoryItems()
        self.showRandomRoomsNames()
        self.showItemsInRoom()
        self.showDiceSuggestion()
        self.showRandomRoomCost()
        self.showEnterTextSuggestion()
        self.showItemsCursor()
        self.showPlayerSpecialItems()
        self.showRandomRoomDescription()

        




class HandleGridUI(handler.BaseHandler):
    """
    Gère l’affichage de la grille du manoir :
        - affichage des salles
        - curseur du joueur
        - salles tirées aléatoirement
        - grande case de la salle actuelle (BIG_IMAGE)
    """

    def __init__(self,data,screen):
        """
        Args:
            data: HandleData
            screen: surface Pygame cible
        """
        super().__init__(data)
        self.screen = screen

        # Image du curseur
        self.cursor_image = pygame.image.load(params.CURSOR_IMAGE_DIR).convert_alpha()


    def showBigRoom(self):
        """Affiche la grande image de la salle actuelle."""
        room = self.data.gridHandler.grid[self.data.player.x][self.data.player.y]
        if room is None:
            return
        image = room.BIG_IMAGE
        self.screen.blit(image, (params.ORIGIN_BIG_TILE[0], params.ORIGIN_BIG_TILE[1]))


    def showCursor(self):
        """Affiche le curseur de direction du joueur dans la grille."""
        x = self.data.player.x*params.ROOM_TILE_SIZE + params.ORIGIN_TILE[0]
        y =  self.data.player.y * params.ROOM_TILE_SIZE + params.ORIGIN_TILE[1]
        
        scaled_image = pygame.transform.scale(self.cursor_image, (params.ROOM_TILE_SIZE, params.ROOM_TILE_SIZE))
        rot =  90*(self.data.player.direction-1)
        rotated_image = pygame.transform.rotozoom(scaled_image, rot, 1)
        
        pygame.draw.rect(self.screen, params.WHITE, (x, y, params.ROOM_TILE_SIZE, params.ROOM_TILE_SIZE), 1)
        self.screen.blit(rotated_image, (x, y))



    def showRoom(self,x0,y0):
        """Affiche une pièce individuelle dans la  grille."""
        room = self.data.gridHandler.grid[x0][y0]

        x = x0*params.ROOM_TILE_SIZE + params.ORIGIN_TILE[0]
        y = y0 *params.ROOM_TILE_SIZE + params.ORIGIN_TILE[1]

        if room is None:
            return
        
        # Effet Dark_Room : masque les pièces du manoir lors du drafting
        if(self.data.dark_room_effect==True):
            if not room.name == "Dark_Room":
                return
        
        image = room.IMAGE        
        self.screen.blit(image, (x, y))


    def showRandomDraftedRooms(self):
        """Affiche les 3 salles tirées lorsqu’on est en mode draft."""
        if not(self.data.state_machine.mode==1):
            return

        x0 = params.ORIGIN_ROOM_RANDOM_GROUP[0]
        y0 = params.ORIGIN_ROOM_RANDOM_GROUP[1]
        y = y0  #origine y
     
        for i,room in enumerate(self.data.gridHandler.randomGeneratedRooms):
            if(room is not None):
                x = x0 + i*(params.RANDOM_GROUP_TILE_SIZE+params.HORIZONTAL_PADDING_RANDOM_GROUP) #origine x
                img = pygame.image.load(room.image_path).convert_alpha()
                scaled_image = pygame.transform.scale(img, (params.RANDOM_GROUP_TILE_SIZE, params.RANDOM_GROUP_TILE_SIZE))
                rot =  90*(room.room_rotation)
                rotated_image = pygame.transform.rotozoom(scaled_image, rot, 1)
                self.screen.blit(rotated_image, (x, y))
            else:
                pygame.draw.rect(self.screen, (150, 150,150), (x, y, params.RANDOM_GROUP_TILE_SIZE, params.RANDOM_GROUP_TILE_SIZE), 1)
            

    def showRoomSelectionCursor(self):
        """Affiche le cadre de sélection autour de la salle choisie en mode draft (possible de choisir entre 3 chambres)
        Méthode qui pourrait être migrée ailleurs car pas explicitement partie de la "grid" techniquement...
        """
        if not self.data.state_machine.mode==1:
            return

        x0 = params.ORIGIN_ROOM_RANDOM_GROUP[0]
        y0 = params.ORIGIN_ROOM_RANDOM_GROUP[1]
        y = y0
        i = self.data.counter_room_selection_cursor
        x = x0 + i*(params.RANDOM_GROUP_TILE_SIZE+params.HORIZONTAL_PADDING_RANDOM_GROUP)
        pygame.draw.rect(self.screen, params.RANDOM_CURSOR_WIDTH_COLOR, (x, y, params.RANDOM_GROUP_TILE_SIZE, params.RANDOM_GROUP_TILE_SIZE), params.RANDOM_CURSOR_WIDTH)
       

    def showGrid(self):
        """Affiche le fond de la grille + toutes les pièces du manoir."""
        self.showGridBackground()
        for y in range(params.ROOM_GRID_SIZE_VERTICAL):
            for x in range(params.ROOM_GRID_SIZE_HORIZONTAL):
                self.showRoom(x,y)
                  

    def showGridBackground(self):
        """Affiche un fond noir derrière la grille."""
        x0,y0 = params.ORIGIN_TILE
        w = params.ROOM_GRID_SIZE_HORIZONTAL*params.ROOM_TILE_SIZE
        h = params.ROOM_GRID_SIZE_VERTICAL*params.ROOM_TILE_SIZE
        pygame.draw.rect(self.screen, params.BLACK, (x0, y0,w, h), 0)



    def update(self):
        """Met à jour tous les éléments de la grille"""
        self.showGrid()
        self.showBigRoom()       
        self.showRandomDraftedRooms()
        self.showRoomSelectionCursor()
        self.showCursor()




class HandleUI(handler.Handlerception):
    """
    Gestionnaire principal de l’interface utilisateur.
    Il orchestre :
        - HandleText
        - HandleGridUI
        - HandleScreen
        - et affiche les écrans de victoire / défaite

    Permet d'éviter avoir 1000 .update() dans le main
    """

    def __init__(self,data ,screen):
        """
        Args:
            data: HandleData
            screen: surface Pygame principale
        """
        super().__init__(data)
        self.screen = screen



    def showGameOverScreen(self):
        """
        Affiche l’écran de défaite lorsqu’il n’y a plus de steps_left.
        """
        if not(self.data.game_over[0] and self.data.game_over[1]==1):# si pas game over alors on sort
            return
            
        self.screen.fill(params.RED) #fond rouge

        # UI game over

        big_font = pygame.font.Font(params.SPECIAL_TEXT_DIR, 100)
        small_font = pygame.font.Font(params.DEFAULT_TEXT_DIR, 40)

        game_over_text = big_font.render("GAME OVER", True, params.WHITE)
        text_rect = game_over_text.get_rect(center=(params.screenWidth // 2, params.screenHeight // 2 - 50))

        txt = "you ran out of steps..."
        small_text = small_font.render(txt, True, params.WHITE)
        small_rect = small_text.get_rect(center=(params.screenWidth // 2, params.screenHeight // 2 + 50))

        self.screen.blit(game_over_text, text_rect)
        self.screen.blit(small_text, small_rect)



    def showWinGameScreen(self):
        """
        Affiche l’écran de victoire lorsque le joueur atteint l'Antechamber.
        """
        if not(self.data.game_over[0] and self.data.game_over[1]==2): # si pas victoire alors on sort
            return
        
        self.screen.fill((0, 150, 0)) # fond vert

        big_font = pygame.font.Font(params.SPECIAL_TEXT_DIR, 100)
        small_font = pygame.font.Font(params.DEFAULT_TEXT_DIR, 40)

        game_over_text = big_font.render("YOU WIN", True, params.WHITE)
        text_rect = game_over_text.get_rect(center=(params.screenWidth // 2, params.screenHeight // 2 - 50))
     
        txt = "you can try again if you have nothing else to do!"
        small_text = small_font.render(txt, True, params.WHITE)
        small_rect = small_text.get_rect(center=(params.screenWidth // 2, params.screenHeight // 2 + 50))

        self.screen.blit(game_over_text, text_rect)
        self.screen.blit(small_text, small_rect)


    def update(self):
        """
        Appelle les handlers enfants puis dessine l’écran de victoire/défaite si pertinent,
        puis rafraîchit l’affichage.
        """
        super().update()

        self.showGameOverScreen()
        self.showWinGameScreen()
        pygame.display.flip()
