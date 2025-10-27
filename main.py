import pygame
import sys
import os
import time
from collections import defaultdict

from src import player
from src import params
from src import ui
from src import sound
from src import inputs
from src import data

from src import room  # import the class Room from room.py

from src import state_machine

# Constants



class Game:
    def __init__(self):
        pygame.init()

        self.screenHandler = ui.HandleScreen()
        self.clock = pygame.time.Clock()
        self.playerHandler = player.Player()

        self.dataHandler = data.HandleData(self.playerHandler,self.clock)


        self.textHandler = ui.HandleText(self.dataHandler,self.screenHandler.screen)
        
        self.audioHandler = sound.HandleSound(self.dataHandler)
        self.inputHandler = inputs.HandleInputs(self.dataHandler)

        

        
        self.gridUIHandler = ui.HandleGridUI(self.dataHandler,self.screenHandler.screen)
        
        self.interfaceHandler = ui.HandleUI(self.dataHandler,self.screenHandler.screen)

        self.interfaceHandler.addHandler(self.screenHandler)
        self.interfaceHandler.addHandler(self.gridUIHandler)
        self.interfaceHandler.addHandler(self.inputHandler)
        self.interfaceHandler.addHandler(self.textHandler)


        self.running = True
       
    def update(self):

        self.dataHandler.update()
        self.playerHandler.update()
   
        self.audioHandler.update()
        self.interfaceHandler.update()
        
        
 


    def run(self):
        while self.dataHandler.keep_running:
            self.update()
            self.clock.tick(params.TARGET_FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    time.sleep(1)
    sys.exit()
