import pygame
from src import params

import math

import os

class handleBackground:
    """
    Création de la base de l'interface

    """

    def __init__(self, surface: pygame.Surface):
        """Initialisation"""
        self.surface = surface
        self.leftColor = params.BLACK
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



class handleScreen:
    def __init__(self,width,height):
        """Initialisation"""
        self.maxWidth = width
        self.maxHeight = height

        self.width, self.height= self.getScreenSize(width,height,params.USE_DEFAULT_SCREEN_SIZE)

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Blue Prince Emulation")
        
    def getScreenSize(self,screenW:int,screenH:int,isFullscreen=False)->int:
        """   
        Fonction qui vérifie quelle taille (en pixels) maximale on peut avoir de sorte à avoir un ratio
        d'image 16:9 et minimiser la bordure

        Parametres:
        screenW:int - taille écran horizontal
        screenH:int - taille écran verticale
        useDefault:bool - pour savoir si prendre par defaut la taille 1920x1080

        Retourne:
        w,h:int - taille finale telle que aspect ratio conservé et taille image conservée ou 1920x1080 si argument defaut choisi
        """
        if(isFullscreen):
            return(params.DEFAULT_SCREEN_WIDTH,params.DEFAULT_SCREEN_HEIGHT)
        echelle = min(screenW / 16.0, screenH / 9.0)
        w = round(math.floor(16 * echelle))
        h = int(math.floor(9 * echelle))

        return(w,h)

    def update(self):
        if(params.changeScreenSizeFlag):
            params.changeScreenSizeFlag = False
            self.width, self.height= self.getScreenSize(self.maxWidth ,self.maxHeight,params.FULL_SCREEN)
            self.screen = pygame.display.set_mode((self.width, self.height))
            params.screenHeight = self.height
            params.screenWidtht = self.width

            os.environ['SDL_VIDEO_CENTERED'] = '1'




class handleText():
    def __init__(self,screen):
        self.screen = screen

       
        self.default_text_size = params.DEFAULT_FONT_SIZE
        self.special_text_size = params.SPECIAL_FONT_SIZE
        self.small_text_size = params.SMALL_FONT_SIZE


        self.left_text = "Left info"
        self.right_text = "Right info"
        self.special_text = "Day One"

        self.default_font = pygame.font.Font(params.DEFAULT_TEXT_DIR, params.DEFAULT_FONT_SIZE)  
        self.special_font = pygame.font.Font(params.SPECIAL_TEXT_DIR, params.SPECIAL_FONT_SIZE)  
        self.small_font = pygame.font.Font(params.SMALL_TEXT_DIR, params.SMALL_FONT_SIZE) 
    
    def draw_text(self, text, position, font=None, color=params.TEXT_COLOR):
        font = font or self.default_font

        rendered_text = font.render(text, True, color)
        self.screen.blit(rendered_text, position)

    def draw(self):
            
        self.draw_text(self.special_text, (params.PADDING, params.PADDING), font=self.special_font, color=(255, 200, 0))

       # fps_text = f"FPS: {int(self.clock.get_fps())}"
        #self.draw_text(fps_text, (params.screenWidth//2 - params.PADDING -  self.small_font.size(fps_text)[0],  params.screenHeight - params.PADDING),font=self.small_font)

    def update(self):
        self.draw()
        pygame.display.flip()

        pass