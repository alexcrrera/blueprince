from src import params

import pygame


class inputHandling:
    def __init__(self):
        # Dictionary to track key presses
        self.key_pressed = {}

    def update(self):
        """
        Call this every frame to update key presses.
        """
        self.key_pressed = {}  # reset for this frame

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.key_pressed["QUIT"] = True
                params.KEEP_RUNNING = False

            if event.type == pygame.KEYDOWN:
                self.key_pressed[event.key] = True
                
                if event.key == pygame.K_m:
                    params.PLAY_MUSIC = not params.PLAY_MUSIC
               
                   
                if event.key == pygame.K_f:
                    pass
                   
             
               
                   


            if event.type == pygame.KEYUP:
                self.key_pressed[event.key] = False

        

    def is_pressed(self, key):
        """
        Check if a key was pressed this frame.
        Example: inputs.is_pressed(pygame.K_SPACE)
        """
        return self.key_pressed.get(key, False)


