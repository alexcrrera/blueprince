import pygame
from src import params
import random

class HandleSound:
    def __init__(self,data):
        self.data = data
        self.music_path = params.MUSIC_TRACK_DIR
        self.sfx_folder_path = params.SFX_DIR
        self.sfx_volume = params.SFX_LEVEL


        self.sfx = {}
        self.randomStartMusic = random.uniform(0,3500) # un peu moins d'une heure au cas où
        self.play_music()

        

        self.sounds = params.SFX_DICT



    # ----------------- Music -----------------
    def play_music(self):
        
        pygame.mixer.music.load(params.MUSIC_TRACK_DIR)
        pygame.mixer.music.set_volume(self.data.music_level)
        pygame.mixer.music.play(loops=-1, start = self.randomStartMusic)

    def stop_music(self):
        """Pause la musique"""
        self.data.music_level = 0
        pygame.mixer.music.set_volume(self.data.music_level)
     

    def set_music_volume(self):
        volume=self.data.music_level
        """Permet d'ajuster la musique"""
        self.music_volume = volume
        pygame.mixer.music.set_volume(volume)

    # ----------------- Sound Effects -----------------
    def load_sfx(self, name,dir):
        self.sounds[name] = dir

    def play_sfx(self, name):
        sound = pygame.mixer.Sound(self.sounds.get(name))
        sound.play()
    

    
    def update(self):
        if(not(self.data.music_play)):
            self.stop_music()
        else:
            self.data.music_level = params.MUSIC_LEVEL
            self.set_music_volume()

        if( self.data.click_play):
             self.data.click_play = False
             self.play_sfx("longclick")
             
        if(self.data.small_click_play):
            self.data.small_click_play = False
            i = random.randint(1, 3)
            rand_audio = "click" + str(i)
            self.play_sfx(rand_audio)

        if(self.data.door_locked_play):
            self.data.door_locked_play = False
            i = random.randint(1, 2)
            rand_audio = "door_lock_" + str(i)
            self.play_sfx(rand_audio)
            
        if(self.data.enter_room_play):
            self.data.enter_room_play = False
           # self.play_sfx("door_open")

        if(self.data.enter_room_play):
            print("dfo")
            self.data.enter_room_play = False
            self.play_sfx("lockpick")
            pass
    
        if(self.data.interact_play):
            self.data.interact_play = False
            self.play_sfx("grab")