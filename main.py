import pygame
import sys
import os
import time

from src import player
from src import params
from src import ui
from src import sound
from src import inputs
from src import data
from src import manor
from src import room  # import the class Room from room.py

# Constants



class Game:
    def __init__(self):
        pygame.init()

        self.screenHandler = ui.HandleScreen()
        self.clock = pygame.time.Clock()
        self.dataHandler = data.HandleData()

        self.playerHandler = player.Player()

        self.textHandler = ui.HandleText(self.screenHandler.screen,self.clock,self.playerHandler)
        
     
        self.dataHandler = data.HandleData()
        self.backgroundHandler = ui.HandleBackground(self.screenHandler.screen)
        self.audioHandler = sound.HandleSound(self.dataHandler)
        self.inputHandler = inputs.HandleInputs(self.dataHandler)

        self.running = True

        self.gridHandler = manor.RoomGrid(self.dataHandler)
        self.gridUIHandler = ui.HandleGridUI(self.dataHandler,self.screenHandler.screen)
        

    def update(self):
        
        self.backgroundHandler.update()
        
        self.playerHandler.update()
        self.running = self.dataHandler.keep_running
        self.screenHandler.update()
        self.textHandler.update()
        self.inputHandler.update()
         
        self.audioHandler.update()
        self.gridHandler.update()
        self.gridUIHandler.update()
        pygame.display.flip()


    def run(self):
        while self.running:
            self.update()
            
            self.clock.tick(params.TARGET_FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    time.sleep(1)
    sys.exit()
