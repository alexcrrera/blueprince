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
        self.dataHandler = data.HandleData(self.playerHandler)


        self.textHandler = ui.HandleText(self.screenHandler.screen,self.clock,self.dataHandler)
        
     
        self.backgroundHandler = ui.HandleBackground(self.screenHandler.screen)
        self.audioHandler = sound.HandleSound(self.dataHandler)
        self.inputHandler = inputs.HandleInputs(self.dataHandler)

        self.running = True

        
        self.gridUIHandler = ui.HandleGridUI(self.dataHandler,self.screenHandler.screen)
        

        self.id = 0

       
    def update(self):
        self.id +=+1
        start_total = time.time()
        indx = 0
        dt = list()
        t1 = time.time()
        t0 = time.time()

        self.dataHandler.update()
        dt.append(time.time() - t1)

        t1 = time.time()
        self.backgroundHandler.update()
        dt.append(time.time() - t1)

        t1 = time.time()
        self.screenHandler.update()
        dt.append(time.time() - t1)

        t1 = time.time()
        self.gridUIHandler.update()
        dt.append(time.time() - t1)


        t1 = time.time()
        self.playerHandler.update()
        dt.append(time.time() - t1)

        t1 = time.time()
        self.textHandler.update()
        dt.append(time.time() - t1)

        t1 = time.time()
        self.inputHandler.update()
        dt.append(time.time() - t1)
         
        t1 = time.time()
        self.audioHandler.update()
        dt.append(time.time() - t1)
       
        t1 = time.time()
        pygame.display.flip()
        dt.append(time.time() - t1)

        if(self.id%60==59):
            print("Total time: " + str(round(time.time()-t0,4)*1000)+ "ms")
            strI = ""
            for i in dt:
                strI += str(round(i*1000,4)) + "ms," 
            print("Time per/fct: " + strI)
            self.id = 0



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
