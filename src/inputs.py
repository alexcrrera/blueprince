from src import params

import pygame


class HandleInputs:
    def __init__(self,data):
        self.data = data
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
                self.data.keep_running = False

            if event.type == pygame.KEYDOWN:
                self.key_pressed[event.key] = True
                
                if event.key == pygame.K_m:
                    self.data.music_play = not self.data.music_play
                if event.key == pygame.K_SPACE:
                    self.data.click_play = True


                if event.key == pygame.K_d:   
                    self.data.arrow_dir = 0
                if event.key == pygame.K_w:
                    self.data.arrow_dir = 1
                if event.key == pygame.K_a:
                    self.data.arrow_dir = 2
                       
                if event.key == pygame.K_s:
                    self.data.arrow_dir = 3

            if event.type == pygame.KEYUP:
                self.key_pressed[event.key] = False

        

    def is_pressed(self, key):
        """
        Check if a key was pressed this frame.
        Example: inputs.is_pressed(pygame.K_SPACE)
        """
        return self.key_pressed.get(key, False)


