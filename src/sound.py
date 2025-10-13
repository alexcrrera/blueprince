import pygame
from src import params
import random

class HandleSound:
    def __init__(self,data):
        self.data = data
        self.music_path = params.MUSIC_TRACK_DIR
        self.sfx_folder_path = params.SFX_DIR
        self.music_volume = params.MUSIC_LEVEL
        self.sfx_volume = params.SFX_LEVEL


        self.sfx = {}
        self.randomStartMusic = random.uniform(0,3500) # un peu moins d'une heure au cas où
        self.play_music()


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
    def load_sfx(self, name):
        pass

    def play_sfx(self, name):
        pass

    
    def update(self):
        if(not(self.data.music_play)):
            self.stop_music()
        else:
            self.data.music_level = params.MUSIC_LEVEL
            self.set_music_volume()
        pass