from src import params
from src import handler
import pygame


class HandleInputs(handler.BaseHandler):
    def __init__(self,data):
        super().__init__(data)
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
                print("exit")

            if event.type == pygame.KEYDOWN:
                self.key_pressed[event.key] = True
                
                if event.key == pygame.K_m:
                    self.data.music_play = not self.data.music_play
                
                
                if event.key == pygame.K_SPACE:
                    if(self.data.state_machine.cursor_selection_mode):
                        self.data.click_play = True
                        self.data.space_pressed = True
                    else:
                        self.data.space_pressed = False



                if event.key == pygame.K_RETURN:
                    if(self.data.state_machine.room_selection_mode):
                        self.data.enter_pressed = True
                        self.data.click_play = True
                    else:
                        self.data.enter_pressed = False  

                if event.key == pygame.K_d:   
                    self.data.player.direction = 0
                    self.data.small_click_play = True
                if event.key == pygame.K_w:
                    self.data.player.direction= 1
                    self.data.small_click_play = True
                if event.key == pygame.K_a:
                    self.data.small_click_play = True
                    self.data.player.direction = 2
                       
                if event.key == pygame.K_s:
                    self.data.small_click_play = True
                    self.data.player.direction = 3

                if event.key == pygame.K_RIGHT:
                    
                    if(self.data.state_machine.room_selection_mode):
                        self.data.small_click_play = True

                        self.data.counter_room_selection_cursor +=1
                        
                        if(self.data.counter_room_selection_cursor >=3):
                             self.data.counter_room_selection_cursor = 0
                if event.key == pygame.K_LEFT:
                
                    if(self.data.state_machine.room_selection_mode):
                        self.data.small_click_play = True
                      
                        self.data.counter_room_selection_cursor -=1
                        if(self.data.counter_room_selection_cursor <0):
                             self.data.counter_room_selection_cursor = 2

            if event.type == pygame.KEYUP:
                self.key_pressed[event.key] = False

        

    def is_pressed(self, key):
        """
        Check if a key was pressed this frame.
        Example: inputs.is_pressed(pygame.K_SPACE)
        """
        return self.key_pressed.get(key, False)


