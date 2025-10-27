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



    def draw_text(self, text, position, font=None, color=params.TEXT_COLOR,center=False):
          # Render the text surface
        rendered_text = font.render(text, True, color)
        text_rect = rendered_text.get_rect()

       
        rendered_text = font.render(text, True, color)
        text_rect = rendered_text.get_rect()

        if center:
            # Center only horizontally
            text_rect.centerx = position[0]
            text_rect.top = position[1]
        else:
            text_rect.topleft = position

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
            txt="Another wall..."
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

        

    def update(self):

        self.draw()
        self.updateInventoryUI()
        

        




class HandleGridUI(handler.BaseHandler):
    def __init__(self,data,screen):
        super().__init__(data)
        self.screen = screen
        
    

        SELECTOR_IMAGE_DIR =  "assets/images/selector.png"
        self.SELECTOR_IMAGE = pygame.image.load(SELECTOR_IMAGE_DIR).convert_alpha()


    def showBigTile(self):
        curr_room = self.data.manor[self.data.player.x][self.data.player.y]
        if(curr_room is None):
            return
  
        curr_room_image = curr_room.IMAGE
  
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
        curr_room = self.data.manor[x0][y0]
        x = x0*params.ROOM_TILE_SIZE + params.ORIGIN_TILE[0]
        y =  y0 * params.ROOM_TILE_SIZE + params.ORIGIN_TILE[1]
        if(curr_room is None):
            pygame.draw.rect(self.screen, (150, 150,150), (x, y, params.ROOM_TILE_SIZE, params.ROOM_TILE_SIZE), 1)
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
                
                
                
            
                
       
       # pygame.display.flip()

    def update(self):
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
        if(not(self.data.game_over[0])):
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
        gType = self.data.game_over[1]
        txt = ""
        if(gType==1):
            txt = "you ran out of steps..."
        elif(gType==2):
            txt = "oops, you locked yourself out!"
        small_text = small_font.render(txt, True, params.WHITE)
        small_rect = small_text.get_rect(center=(params.screenWidth // 2, params.screenHeight // 2 + 50))

        # Affiche les deux textes
        self.screen.blit(game_over_text, text_rect)
        self.screen.blit(small_text, small_rect)

        

    def update(self):
        super().update()


        self.gameOver()
        pygame.display.flip()
            