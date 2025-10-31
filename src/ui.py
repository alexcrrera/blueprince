import pygame
from src import params
import time
import math

import os
from src import handler




class HandleScreen:
    def __init__(self):
        """Initialisation"""

        ICON_IMAGE_DIR = "assets/images/icon.png"
        ICON_IMAGE  = pygame.image.load(ICON_IMAGE_DIR)

        BACKGROUND_DIR =  "assets/images/ui/background.png"
    

        self.width, self.height= params.DEFAULT_SCREEN_WIDTH,params.DEFAULT_SCREEN_HEIGHT

        self.screen = pygame.display.set_mode((self.width, self.height))
       

        pygame.display.set_icon(ICON_IMAGE)

        pygame.display.set_caption("Blue Prince Emulation")

        BACKGROUND = pygame.image.load(BACKGROUND_DIR).convert_alpha()
        scale = pygame.transform.scale(BACKGROUND, (params.screenWidth, params.screenHeight))
        self.BACKGROUND = scale

        print("starting")
        time.sleep(0.5)
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        
    

    def drawBackground(self):
        self.screen.blit(self.BACKGROUND, (0, 0))

    def update(self):
        self.drawBackground()
        pass




class HandleText(handler.BaseHandler):
    def __init__(self,data,screen):
        super().__init__(data)

        
        self.screen = screen

       
        self.default_text_size = params.DEFAULT_FONT_SIZE
        self.special_text_size = params.SPECIAL_FONT_SIZE
        self.small_text_size = params.SMALL_FONT_SIZE

        self.alt_default_text = params.ALT_DEFAULT_SIZE
        

        self.left_text = "Left info"
        self.right_text = "Right info"
        self.special_text = "Day One"


        self.default_font = pygame.font.Font(params.DEFAULT_TEXT_DIR, params.DEFAULT_FONT_SIZE)  
        self.special_font = pygame.font.Font(params.SPECIAL_TEXT_DIR, params.SPECIAL_FONT_SIZE)  
        self.small_font = pygame.font.Font(params.SMALL_TEXT_DIR, params.SMALL_FONT_SIZE) 
        self.alt_default_font = pygame.font.Font(params.ALT_DEFAULT_TEXT_DIR, params.ALT_DEFAULT_SIZE) 
        self.inventory_font = pygame.font.Font(params.ALT_DEFAULT_TEXT_DIR, params.INVENTORY_TEXT_SIZE) 
        self.random_group_font = pygame.font.Font(params.ALT_DEFAULT_TEXT_DIR, params.RANDOM_ROOM_TEXT_SIZE) 
        self.dice_suggestion_font  = pygame.font.Font(params.ALT_DEFAULT_TEXT_DIR, params.DICE_SUGGESTION_TEXT_SIZE) 
        self.enter_suggestion_font =  pygame.font.Font(params.ALT_DEFAULT_TEXT_DIR, params.ENTER_SUGGESTION_TEXT_SIZE) 
        self.room_info_font = pygame.font.Font(params.ALT_DEFAULT_TEXT_DIR, params.ROOM_TEXT_SIZE) 
        self.items_size_font = pygame.font.Font(params.DEFAULT_TEXT_DIR, params.ITEM_TEXT_SIZE) 

        self.you_found_font = pygame.font.Font(params.DEFAULT_TEXT_DIR, params.YOU_FOUND_TEXT_SIZE) 

        self.items_cursor =  pygame.font.Font(params.ALT_DEFAULT_TEXT_DIR, params.YOU_FOUND_TEXT_SIZE) 
    def draw_text(self, text, position, font=None, color=params.TEXT_COLOR, center=False, rotation=0):
    # Choose default font if none given
        if font is None:
            font = self.default_font

        # Render text surface
        rendered_text = font.render(text, True, color)

        # Apply rotation if specified
        if rotation != 0:
            rendered_text = pygame.transform.rotate(rendered_text, rotation)

        # Get rect after rotation (important — rotated text has new dimensions)
        text_rect = rendered_text.get_rect()

        # Position text
        if center:
            # Center both horizontally and vertically
            text_rect.center = position
        else:
            text_rect.topleft = position

        # Draw the text
        self.screen.blit(rendered_text, text_rect)


    def drawNextRoomInfo(self):
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
       
        elif(stat==0 ):
             txt="There's a wall..."
        elif(stat==-2):
            txt="That's a nice  wall..."
        self.draw_text(txt, (params.ROOM_INFO_ORIGIN[0], params.ROOM_INFO_ORIGIN[1]), font=self.small_font, color=(255, 200, 0))



    def draw(self):
        self.drawNextRoomInfo()
        
        self.draw_text(self.special_text, (params.PADDING, params.PADDING//4), font=self.special_font, color=(255, 200, 0))

        fps_text = f"FPS: {int(self.data.clock.get_fps())}"
        self.draw_text(fps_text, (params.screenWidth//2 - params.PADDING -  self.small_font.size(fps_text)[0],  params.screenHeight - params.PADDING),font=self.small_font,color=params.BLACK)


    def updateInventoryUI(self):
        #self.draw_text(params.INVENTORY_TEXT, (params.ORIGIN_INVENTORY[0], params.ORIGIN_INVENTORY[1]), font=self.inventory_font, color=params.BLACK)
        
        padding = [i*params.INVENTORY_ITEMS_PADDING for i in range(1,7)]
        
        for i in range(0,5):
            text = str(self.data.player.inventory.ui_items[i])
            self.draw_text(text, (params.ORIGIN_INVENTORY[0], params.ORIGIN_INVENTORY[1]+padding[i]), font=self.inventory_font, color=params.WHITE,center=True)
        #text = str(params.DIRECTION_CARDINAL[self.data.player.direction])

        #self.draw_text(text, (params.ORIGIN_INVENTORY[0], params.ORIGIN_INVENTORY[1]+padding[5]), font=self.inventory_font, color=params.WHITE,center=True)

    def drawRandomRoomInfo(self):
         
        if(self.data.state_machine.mode==1):
           
            rooms = self.data.gridHandler.randomGeneratedRooms
            x0,y0 = params.ORIGIN_ROOM_RANDOM_TEXT
            x0 += params.RANDOM_GROUP_TILE_SIZE//2
            padding = 0
            
            for (i,r) in enumerate(rooms):
                text = r.cleaned_name
                if(i == self.data.counter_room_selection_cursor):
                    colr = params.WHITE
                else:
                    colr = params.GRAY
                self.draw_text(text, (x0+padding,y0), font=self.random_group_font, color=colr,center=True)
                padding +=params.HORIZONTAL_PADDING_RANDOM_GROUP + params.RANDOM_GROUP_TILE_SIZE
        

    def showRandomRoomCost(self):
        if(not self.data.state_machine.mode==1):
            return
        rooms = self.data.gridHandler.randomGeneratedRooms
        x0,y0 = params.ORIGIN_RANDOM_ROOM_COST
        x0 += (params.RANDOM_GROUP_TILE_SIZE *0.3)//1
        for i in range(3):
            cost = rooms[i].cost

            txt = "costs " +  str(cost) 
            add = "" if cost ==1 else "s"
            txt +=" gem" + add

            if(self.data.player.inventory.gems - cost>=0):
                col = params.WHITE
            else:
                col = params.RED
            self.draw_text(txt, (x0,y0), font=self.alt_default_font, color=col)
            
            x0 += params.RANDOM_GROUP_TILE_SIZE+params.HORIZONTAL_PADDING_RANDOM_GROUP
        
    def showCurrentRoomInfo(self):
        if(not self.data.state_machine.mode == 0):
            return  
        x,y = self.data.player.x,self.data.player.y
        current_room =self.data.gridHandler.grid[x][y]
        txt = current_room.returnNameWithoutUnderscore()
        x0,y0 = params.ORIGIN_ROOM_TEXT_INFO[0],params.ORIGIN_ROOM_TEXT_INFO[1]
        self.draw_text(txt, (x0,y0), font=self.room_info_font)


        x0,y0 = params.ORIGIN_YOU_FOUND_TEXT[0], params.ORIGIN_YOU_FOUND_TEXT[1]
        txt = "You found:"
        self.draw_text(txt, (x0,y0), font=self.you_found_font)

        

    def showItemsInRoom(self):
        if(not self.data.state_machine.mode == 0):
            return
        x0 = params.ORIGIN_ITEMS_IN_ROOM[0]
        y0 =params.ORIGIN_ITEMS_IN_ROOM[1]
        x,y = self.data.player.x,self.data.player.y
        current_room =self.data.gridHandler.grid[x][y]
       # print("itemasdas: ",current_room.name)
        data = current_room.items
        
        descript_dict = params.ITEMS_DESCRIPTION_DICT
        count_items = len(current_room.items)
        if(count_items==0):
            txt = "Nothing!"
            self.draw_text(txt,(x0,y0),font= self.enter_suggestion_font,color=params.LIGHT_GRAY)
            return
        
        for key, value in data.items():

            desc = descript_dict[key]
    
            txt = desc[0] +" :  x" + str(value) + "  (" +desc[1]  + ")"
            #print("items: ",txt)
            self.draw_text(txt, (x0,y0), font=self.items_size_font)
            y0 += params.ITEMS_IN_ROOM_PADDING
        
        
        

    def showDiceSuggestion(self):
        """Suggere l'utilisation du dé pour regénérer les chambres"""
        
        if(not self.data.state_machine.mode == 1):
            return
        if(not(self.data.player.inventory.dice >0)):
            col = params.RED
            txt = "No dices left"
        else:
            txt = "Press R to use a dice to redraft"
            col = params.WHITE    
        x,y = params.DICE_TEXT_SUGGESTION_ORIGIN
        self.draw_text(txt,(x,y),font= self.dice_suggestion_font,rotation=270,color=col)

    def showEnterTextSuggestion(self):
        if(not self.data.state_machine.mode == 1):
            return  
        x,y = params.ORIGIN_PRESS_ENTER_TEXT
        txt  = "Press ENTER to choose a room!"
        self.draw_text(txt,(x,y),font= self.enter_suggestion_font,color=params.LIGHT_GRAY)


    def showItemsCursor(self):
        if(not self.data.state_machine.mode == 0):
            return  
        x,y = self.data.player.x,self.data.player.y
        current_room =self.data.gridHandler.grid[x][y]

        count_items = len(current_room.items)
        if(count_items==0):
           
            return
        x0,y0 = params.CURSOR_ITEMS_ORIGIN[0],params.CURSOR_ITEMS_ORIGIN[1]
        txt = ">"
        y0 += params.ITEMS_IN_ROOM_PADDING*self.data.counter_inventory
        self.draw_text(txt,(x0,y0),font= self.enter_suggestion_font,color=params.LIGHT_GRAY)
    def update(self):

        self.draw()
        self.showItemsCursor()
        self.showItemsInRoom()
        self.showCurrentRoomInfo()
        self.updateInventoryUI()
        self.drawRandomRoomInfo()
        self.showItemsInRoom()
        self.showDiceSuggestion()
        self.showRandomRoomCost()
        self.showEnterTextSuggestion()
        

        




class HandleGridUI(handler.BaseHandler):
    def __init__(self,data,screen):
        super().__init__(data)
        self.screen = screen
        
    

        SELECTOR_IMAGE_DIR =  "assets/images/selector.png"
        self.SELECTOR_IMAGE = pygame.image.load(SELECTOR_IMAGE_DIR).convert_alpha()


    def showBigTile(self):
        curr_room = self.data.gridHandler.grid[self.data.player.x][self.data.player.y]
        if(curr_room is None):
            return
  
        curr_room_image = curr_room.BIG_IMAGE
  
        self.screen.blit(curr_room_image, (params.ORIGIN_BIG_TILE[0], params.ORIGIN_BIG_TILE[1]))
       

    def showCursor(self):
       
        x = self.data.player.x*params.ROOM_TILE_SIZE + params.ORIGIN_TILE[0]
        y =  self.data.player.y * params.ROOM_TILE_SIZE + params.ORIGIN_TILE[1]
        if(not(self.data.state_machine.cursor_selection_mode)):
            pygame.draw.rect(self.screen, (255, 0,0), (x, y, params.ROOM_TILE_SIZE, params.ROOM_TILE_SIZE), 1)
            return
        
        scaled_image = pygame.transform.scale(self.SELECTOR_IMAGE, (params.ROOM_TILE_SIZE, params.ROOM_TILE_SIZE))
        rot =  90*(self.data.player.direction-1)
        rotated_image = pygame.transform.rotozoom(scaled_image, rot, 1)
        
        self.screen.blit(rotated_image, (x, y))
        

    def drawNextRoom(self):
        
        if(not(self.data.state_machine.cursor_selection_mode) or not params.NEXT_ROOM_SHOW):
            
            return
        x0 = self.data.player.next_room_position[0]
        y0 = self.data.player.next_room_position[1]
        x= x0*params.ROOM_TILE_SIZE + params.ORIGIN_TILE[0]
        y =  y0 * params.ROOM_TILE_SIZE + params.ORIGIN_TILE[1]
        pygame.draw.rect(self.screen, (0, 255,0), (x, y, params.ROOM_TILE_SIZE, params.ROOM_TILE_SIZE), 1)


    def drawRoom(self,x0,y0):
        curr_room = self.data.gridHandler.grid[x0][y0]
        x = x0*params.ROOM_TILE_SIZE + params.ORIGIN_TILE[0]
        y =  y0 * params.ROOM_TILE_SIZE + params.ORIGIN_TILE[1]
        if(curr_room is None):
            #pygame.draw.rect(self.screen, params.WHITE, (x, y, params.ROOM_TILE_SIZE, params.ROOM_TILE_SIZE), 1)
            return
    
        curr_room_image = curr_room.IMAGE
        
   
        self.screen.blit(curr_room_image, (x, y))




    def showRandomRooms(self):
        if(not(self.data.state_machine.room_selection_mode)):
            return
        x0 = params.ORIGIN_ROOM_RANDOM_GROUP[0]
        y0 = params.ORIGIN_ROOM_RANDOM_GROUP[1]
        y = y0 
     
        for i,room in enumerate(self.data.gridHandler.randomGeneratedRooms):
            if(room is not None):
                x = x0 + i*(params.RANDOM_GROUP_TILE_SIZE+params.HORIZONTAL_PADDING_RANDOM_GROUP)
                curr_room_image = room.image_path
                img = pygame.image.load(curr_room_image).convert_alpha()
                scaled_image = pygame.transform.scale(img, (params.RANDOM_GROUP_TILE_SIZE, params.RANDOM_GROUP_TILE_SIZE))

                rot =  90*(room.room_rotation)
                rotated_image = pygame.transform.rotozoom(scaled_image, rot, 1)
       
                self.screen.blit(rotated_image, (x, y))


                
            else:
                pygame.draw.rect(self.screen, (150, 150,150), (x, y, params.RANDOM_GROUP_TILE_SIZE, params.RANDOM_GROUP_TILE_SIZE), 1)
            

    
    def showRandomSelectionCursor(self):
        if(not self.data.state_machine.room_selection_mode):
            return
        x0 = params.ORIGIN_ROOM_RANDOM_GROUP[0]
        y0 = params.ORIGIN_ROOM_RANDOM_GROUP[1]
        y = y0
        i = self.data.counter_room_selection_cursor
        x = x0 + i*(params.RANDOM_GROUP_TILE_SIZE+params.HORIZONTAL_PADDING_RANDOM_GROUP)
        pygame.draw.rect(self.screen, params.RANDOM_CURSOR_WIDTH_COLOR, (x, y, params.RANDOM_GROUP_TILE_SIZE, params.RANDOM_GROUP_TILE_SIZE), params.RANDOM_CURSOR_WIDTH)
       


    def updateGrid(self):

        for row in range(params.ROOM_GRID_SIZE_VERTICAL):
            for col in range(params.ROOM_GRID_SIZE_HORIZONTAL):
                self.drawRoom(col,row)
                
                
                
            
    def showManorBg(self)           :
        x0,y0 = params.ORIGIN_TILE
        w = params.ROOM_GRID_SIZE_HORIZONTAL*params.ROOM_TILE_SIZE
        h = params.ROOM_GRID_SIZE_VERTICAL*params.ROOM_TILE_SIZE
        pygame.draw.rect(self.screen, params.BLACK, (x0, y0,w, h), 0)

       
       # pygame.display.flip()

    def update(self):
        self.showManorBg()
        self.updateGrid()
        self.showBigTile()
        self.showCursor()
        self.drawNextRoom()
        self.showRandomRooms()
        self.showRandomSelectionCursor()
      


class HandleUI(handler.Handlerception):

    def __init__(self,data ,screen):
        
        super().__init__(data)
        self.screen = screen



    def addHandler(self,handler):
        self.handlingFunctions.append(handler)


    def gameOver(self):
        """Affiche l'écran de fin de partie."""
        if(not(self.data.game_over[0] and self.data.game_over[1]==1) ):
            return
            
    # Remplit l'écran en rouge
        self.screen.fill((150, 0, 0))

        # Crée les polices
        big_font = pygame.font.Font(params.SPECIAL_TEXT_DIR, 100)
        small_font = pygame.font.Font(params.DEFAULT_TEXT_DIR, 40)

        # Texte principal
        game_over_text = big_font.render("GAME OVER", True, params.WHITE)
        text_rect = game_over_text.get_rect(center=(params.screenWidth // 2, params.screenHeight // 2 - 50))

        # Texte secondaire
        
        txt = "you ran out of steps..."
       
        small_text = small_font.render(txt, True, params.WHITE)
        small_rect = small_text.get_rect(center=(params.screenWidth // 2, params.screenHeight // 2 + 50))

        # Affiche les deux textes
        self.screen.blit(game_over_text, text_rect)
        self.screen.blit(small_text, small_rect)

    def winGame(self):
        """Affiche l'écran de fin de partie."""
        if(not(self.data.game_over[0] and self.data.game_over[1]==2) ):
            return
        

    # Remplit l'écran en rouge
        self.screen.fill((0, 150, 0))

        # Crée les polices
        big_font = pygame.font.Font(params.SPECIAL_TEXT_DIR, 100)
        small_font = pygame.font.Font(params.DEFAULT_TEXT_DIR, 40)

        # Texte principal
        game_over_text = big_font.render("YOU WIN", True, params.WHITE)
        text_rect = game_over_text.get_rect(center=(params.screenWidth // 2, params.screenHeight // 2 - 50))

     
        txt = "you can try again if you have nothing else to do!"
        small_text = small_font.render(txt, True, params.WHITE)
        small_rect = small_text.get_rect(center=(params.screenWidth // 2, params.screenHeight // 2 + 50))

        # Affiche les deux textes
        self.screen.blit(game_over_text, text_rect)
        self.screen.blit(small_text, small_rect)


    def update(self):
        super().update()


        self.gameOver()
        self.winGame()
        pygame.display.flip()
            