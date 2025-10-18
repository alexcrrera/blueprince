import math
import pygame
import json
import os

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
TARGET_FPS = 60
splitRatioScreen = 0.33 # ratio entre côté gauche et droite

INITIAL_STEPS = 70
INTIAL_GOLD = 0
INITIAL_GEMS = 2
INTIAL_KEY =0
INTIAL_DICE = 0



json_path = os.path.join("src", "rooms.json")
DICT_DIRECTORIES = {}
with open(json_path, "r") as file:
    DICT_DIRECTORIES = json.load(file)



SFX_LEVEL =0.5
MUSIC_LEVEL = 1

AUDIO_DIR = "assets/audio"

MUSIC_TRACK_DIR = AUDIO_DIR +"/music" +"/mainTrack.mp3" 

SFX_DIR =  AUDIO_DIR + "/mainTrack.mp3" 

PLAY_MUSIC_START = False #play music at start


#IMAGES
IMAGE_CONVERSION_SIZE = 500

#TODO REPLACE WITH DICT
ICON_IMAGE_DIR = "assets/images/icon.png"
ICON_IMAGE  = pygame.image.load(ICON_IMAGE_DIR)


SELECTOR_IMAGE_DIR =  "assets/images/selector.png"
SELECTOR_IMAGE = pygame.image.load(SELECTOR_IMAGE_DIR).convert_alpha()


ENTRANCE_HALL_IMAGE_DIR = "assets/images/rooms/Entrance_Hall.jpg"
ENTRANCE_HALL_IMAGE = pygame.image.load(ENTRANCE_HALL_IMAGE_DIR).convert_alpha()


ANTECHAMBER_IMAGE_DIR = "assets/images/rooms/Antechamber.jpg"
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

ALT_DEFAULT_SIZE= DEFAULT_FONT_SIZE
# Fonts

SMALL_TEXT_DIR = "assets/fonts/Helvetica.ttf"
DEFAULT_TEXT_DIR = "assets/fonts/Helvetica.ttf"
SPECIAL_TEXT_DIR = "assets/fonts/damnarc.ttf"
ALT_DEFAULT_TEXT_DIR = "assets/fonts/Coolvetica Rg.otf"


DIV_ITEMS = [850,80]
ORIGIN_SPECIAL_ITEMS =  [DIV_ITEMS[0],DIV_ITEMS[1]]
SPECIAL_ITEMS_SIZE= [600,140]
SPECIAL_ITEMS_COLOR = DARK_BLUE_COLOR


INVENTORY_SEPARATION = [50,0]
ORIGIN_INVENTORY = [ORIGIN_SPECIAL_ITEMS[0]+SPECIAL_ITEMS_SIZE[0] + INVENTORY_SEPARATION[0],DIV_ITEMS[1]]
INVENTORY_TEXT = "INVENTORY"
INVENTORY_ITEMS_PADDING = 40
INVENTORY_TEXT_SIZE = 40


ROOM_GRID_SIZE_HORIZONTAL = 5
ROOM_GRID_SIZE_VERTICAL = 9

ROOM_TILE_SIZE = 100

ORIGIN_TILE = [70,90]

BIG_TILE = 250
ORIGIN_BIG_TILE = [screenWidth-BIG_TILE,screenHeight-BIG_TILE]