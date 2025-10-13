import pygame
import sys
import os
import time


from src import params
from src import ui
from src import sound
from src import inputs
# Constants

BG_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)
FONT_SIZE = 30
PADDING = 20
SMALL_FONT_SIZE = 10


class Game:
    def __init__(self):
        pygame.init()
        # permet d'ajuster l'écran afin de maximiser la taille tout en conservant un aspect ratio de 16:9
        info = pygame.display.Info()
        self.screenHandler = ui.handleScreen(info.current_w, info.current_h)
        self.textHandler = ui.handleText(self.screenHandler.screen)
      
 
        self.bg = ui.handleBackground(self.screenHandler.screen)
        self.audio = sound.HandleSound()
        self.input = inputs.inputHandling()


        self.clock = pygame.time.Clock()
        self.running = True

    def update(self):
        self.running = params.KEEP_RUNNING
        self.screenHandler.update()
        self.textHandler.update()
        self.input.update()
        self.bg.draw()
        self.audio.update()
        
        pass


    def run(self):
        while self.running:
            self.update()
            self.clock.tick(params.fps)

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    time.sleep(1)
    sys.exit()
