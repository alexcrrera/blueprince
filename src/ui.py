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
    def update(self):
        self.draw()


class HandleScreen:
    def __init__(self):
        """Initialisation"""


        self.width, self.height= params.DEFAULT_SCREEN_WIDTH,params.DEFAULT_SCREEN_HEIGHT

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Blue Prince Emulation")
        os.environ['SDL_VIDEO_CENTERED'] = '1'
    

    def update(self):
        pass




class HandleText():
    def __init__(self,screen,clock):

        self.clock = clock
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

        fps_text = f"FPS: {int(self.clock.get_fps())}"
        self.draw_text(fps_text, (params.screenWidth//2 - params.PADDING -  self.small_font.size(fps_text)[0],  params.screenHeight - params.PADDING),font=self.small_font,color=params.BLACK)

    def update(self):
        self.draw()
        pygame.display.flip()

        pass