import math
import pygame


if not pygame.get_init():
    pygame.init()
pygame.display.set_mode((1, 1))  # Hidden 1×1 window just for convert()


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


#IMAGES
IMAGE_CONVERSION_SIZE = 500

#TODO REPLACE WITH DICT
ENTRANCE_HALL_IMAGE_DIR = "assets/images/Entrance_Hall.jpg"
ENTRANCE_HALL_IMAGE = pygame.image.load(ENTRANCE_HALL_IMAGE_DIR).convert_alpha()


ANTECHAMBER_IMAGE_DIR = "assets/images/Antechamber.jpg"
ANTECHAMBER_HALL_IMAGE = pygame.image.load(ANTECHAMBER_IMAGE_DIR).convert_alpha()



# UI

BG_COLOR = (30, 30, 30)

DARK_BLUE_COLOR = (30,70,136)

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

ROOM_TILE_SIZE = 100

ORIGIN_TILE = [70,90]

BIG_TILE = 360
ORIGIN_BIG_TILE = [685,185]