import pygame
from src import params

import math

import os

class HandleBackground:
    """
    Création de la base de l'interface

    """

    def __init__(self, surface: pygame.Surface):
        """Initialisation"""
        self.surface = surface
        self.leftColor = params.DARK_BLUE_COLOR
        self.rightColor = params.WHITE
        self.splitRatio = params.splitRatioScreen  # 33%

    def draw(self):
        """
        Crée le fond de l'interface
        - Gauche 33%: noir
        - Doite 67%: blanc"""
        width, height = self.surface.get_size()
        leftWidth = int(width * self.splitRatio)

        pygame.draw.rect(self.surface, self.leftColor, (0, 0, leftWidth, height))
        pygame.draw.rect(self.surface, self.rightColor, (leftWidth, 0, width - leftWidth, height))
        
        
        x0 =params.ORIGIN_SPECIAL_ITEMS[0]
        y0 = params.ORIGIN_SPECIAL_ITEMS[1]
        w = params.SPECIAL_ITEMS_SIZE[0]
        h = params.SPECIAL_ITEMS_SIZE[1]
        pygame.draw.rect(self.surface, params.SPECIAL_ITEMS_COLOR, (x0,y0,w,h))



    def update(self):
        self.draw()


class HandleScreen:
    def __init__(self):
        """Initialisation"""


        self.width, self.height= params.DEFAULT_SCREEN_WIDTH,params.DEFAULT_SCREEN_HEIGHT

        self.screen = pygame.display.set_mode((self.width, self.height))
       

        pygame.display.set_icon(params.ICON_IMAGE)
        pygame.display.set_caption("Blue Prince Emulation")
        os.environ['SDL_VIDEO_CENTERED'] = '1'
    

    def update(self):
        pass




class HandleText():
    def __init__(self,screen,clock,data):
        self.data = data
    

        self.clock = clock
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

    def draw(self):
        
        self.draw_text(self.special_text, (params.PADDING, params.PADDING), font=self.special_font, color=(255, 200, 0))

        fps_text = f"FPS: {int(self.clock.get_fps())}"
        self.draw_text(fps_text, (params.screenWidth//2 - params.PADDING -  self.small_font.size(fps_text)[0],  params.screenHeight - params.PADDING),font=self.small_font,color=params.BLACK)


    def updateInventory(self):
        self.draw_text(params.INVENTORY_TEXT, (params.ORIGIN_INVENTORY[0], params.ORIGIN_INVENTORY[1]), font=self.inventory_font, color=params.BLACK)
        
        padding = [i*params.INVENTORY_ITEMS_PADDING for i in range(1,7)]
        
        for i in range(0,5):
            text = str(self.data.player.inventory.ui_items[i])
            self.draw_text(text, (params.ORIGIN_INVENTORY[0], params.ORIGIN_INVENTORY[1]+padding[i]), font=self.inventory_font, color=params.BLACK,center=True)

        text = str(params.DIRECTION_CARDINAL[self.data.player.direction])

        self.draw_text(text, (params.ORIGIN_INVENTORY[0], params.ORIGIN_INVENTORY[1]+padding[5]), font=self.inventory_font, color=params.BLACK,center=True)
    def update(self):

        self.draw()
        self.updateInventory()
        

        




class HandleGridUI():
    def __init__(self,data,screen):
        self.data = data
        self.screen = screen

    def updateGrid(self):

        

        for row in range(params.ROOM_GRID_SIZE_VERTICAL):
            for col in range(params.ROOM_GRID_SIZE_HORIZONTAL):


                x = col * params.ROOM_TILE_SIZE + params.ORIGIN_TILE[0]
                y = row * params.ROOM_TILE_SIZE + params.ORIGIN_TILE[1]

                current_room = self.data.manor[col][row]

                if(current_room is not None):
                    curr_room_image = current_room.image_path
                    img = pygame.image.load(curr_room_image).convert_alpha()


                    scaled_image = pygame.transform.scale(img, (params.ROOM_TILE_SIZE, params.ROOM_TILE_SIZE)
                    )

                    self.screen.blit(scaled_image, (x, y))

            

                if(row==self.data.roomY and col == self.data.roomX):

                
                    scaled_image = pygame.transform.scale(
                        params.SELECTOR_IMAGE, (params.ROOM_TILE_SIZE, params.ROOM_TILE_SIZE)
                    )
                    rot =  90*(self.data.player.direction-1)
                    
                    rotated_image = pygame.transform.rotozoom(scaled_image, rot, 1)
                    self.screen.blit(rotated_image, (x, y))
                else:
                    
                #self.screen.blit(room_image, (x, y))

                # Optional: draw borders
                    pygame.draw.rect(self.screen, (80, 80, 80), (x, y, params.ROOM_TILE_SIZE, params.ROOM_TILE_SIZE), 1)

        #big room item placeholder
        pygame.draw.rect(self.screen, (80, 80, 80), (params.ORIGIN_BIG_TILE[0], params.ORIGIN_BIG_TILE[1], params.BIG_TILE, params.BIG_TILE), 1)
        
        

       # pygame.display.flip()

    def update(self):
        if(self.data.update_tiles):
           
            self.updateGrid()
        