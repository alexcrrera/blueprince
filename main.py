import pygame
import sys
import os
import time


from src import params
from src import ui
from src import sound
from src import inputs
from src import data
from src import manor
from src import room  # import the class Room from room.py

# Constants

BG_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)
FONT_SIZE = 30
PADDING = 20
SMALL_FONT_SIZE = 10


class Game:
    def __init__(self):
        pygame.init()

        self.screenHandler = ui.HandleScreen()
        self.clock = pygame.time.Clock()
        self.textHandler = ui.HandleText(self.screenHandler.screen,self.clock)
        
        self.dataHandler = data.HandleData()
        self.backgroundHandler = ui.HandleBackground(self.screenHandler.screen)
        self.audioHandler = sound.HandleSound(self.dataHandler)
        self.inputHandler = inputs.HandleInputs(self.dataHandler)

        self.running = True

        self.gridHandler = manor.RoomGrid(data)

        print(self.gridHandler.__repr__())
 

    def update(self):
        self.running = self.dataHandler.keep_running
        self.screenHandler.update()
        self.textHandler.update()
        self.inputHandler.update()
        self.backgroundHandler.update()
        self.audioHandler.update()
        self.gridHandler.update()
        
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
