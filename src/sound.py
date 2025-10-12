import pygame
from src import params

class HandleSound:
    def __init__(self):
  
        self.music_path = params.MUSIC_TRACK_DIR
        self.sfx_folder_path = params.SFX_DIR
        self.music_volume = params.MUSIC_LEVEL
        self.sfx_volume = params.SFX_LEVEL


        self.sfx = {}
        self.play_music()


    # ----------------- Music -----------------
    def play_music(self):
        
        pygame.mixer.music.load(params.MUSIC_TRACK_DIR)
        pygame.mixer.music.set_volume(params.MUSIC_LEVEL)
        pygame.mixer.music.play(loops=-1)

    def stop_music(self):
        """Pause la musique"""
        pygame.mixer.music.stop()

    def set_music_volume(self, volume):
        """Permet d'ajuster la musique"""
        self.music_volume = volume
        pygame.mixer.music.set_volume(volume)

    # ----------------- Sound Effects -----------------
    def load_sfx(self, name):
        pass

    def play_sfx(self, name):
        pass

    
    def update(self):
        if(not(params.PLAY_MUSIC)):
            self.stop_music()
        pass