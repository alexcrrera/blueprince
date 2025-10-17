import math
import pygame
# Screen settings
DEFAULT_SCREEN_WIDTH= 1920
DEFAULT_SCREEN_HEIGHT = 1080
screenWidth = DEFAULT_SCREEN_WIDTH #taille image horizontal par défaut
screenHeight = DEFAULT_SCREEN_HEIGHT #taille image vertical par défaut

#TODO: TIDY UP TOUT ÇA

#Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game settings
fps = 60
splitRatioScreen = 0.33 # ratio entre côté gauche et droite

SFX_LEVEL =0.5
MUSIC_LEVEL = 1

AUDIO_DIR = "assets/audio"

MUSIC_TRACK_DIR = AUDIO_DIR +"/music" +"/mainTrack.mp3" 

SFX_DIR =  AUDIO_DIR + "/mainTrack.mp3" 

PLAY_MUSIC_START = False #play music at start




# UI

BG_COLOR = (30, 30, 30)

TEXT_COLOR = (255, 255, 255)

FONT_SIZE = 30

PADDING = 20

SMALL_FONT_SIZE = 10
DEFAULT_FONT_SIZE = 20
SPECIAL_FONT_SIZE = 30
# Fonts

SMALL_TEXT_DIR = "assets/fonts/Helvetica.ttf"
DEFAULT_TEXT_DIR = "assets/fonts/Helvetica.ttf"
SPECIAL_TEXT_DIR = "assets/fonts/damnarc.ttf"






ROOM_GRID_SIZE_HORIZONTAL = 5
ROOM_GRID_SIZE_VERTICAL = 9

ROOM_TILE_SIZE = 5

ORIGIN_TILE = [0,screenHeight]