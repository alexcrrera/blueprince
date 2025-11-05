import math

import json
import os



# Screen settings
USE_DEFAULT = True

if(USE_DEFAULT):
        
    DEFAULT_SCREEN_WIDTH= 1920
    DEFAULT_SCREEN_HEIGHT = 1080
else:
    DEFAULT_SCREEN_WIDTH= 1080
    DEFAULT_SCREEN_HEIGHT = 720


    
screenWidth = DEFAULT_SCREEN_WIDTH #taille image horizontal par défaut
screenHeight = DEFAULT_SCREEN_HEIGHT #taille image vertical par défaut

#TODO: TIDY UP TOUT ÇA

#Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0,255,0)
GRAY = (100,100,100)
LIGHT_GRAY = (200,200,200)
RED = (220,0,0)

YELLOW = (255, 200, 0)
# Game settings
TARGET_FPS = 10
splitRatioScreen = 0.33 # ratio entre côté gauche et droite

INITIAL_STEPS = 70
INTIAL_GOLD = 0
INITIAL_GEMS = 2
INTIAL_KEY =10
INTIAL_DICE = 2

INITIAL_ITEMS_DICT ={
    "steps_left": INITIAL_STEPS,
    "gems": INITIAL_GEMS,
    "gold": INTIAL_GOLD,
    "keys": INTIAL_KEY,
    "dice": INTIAL_DICE

}


json_path = os.path.join("src", "rooms.json")
DICT_ROOM_ATTRIBUTES = {}
with open(json_path, "r") as file:
    DICT_ROOM_ATTRIBUTES = json.load(file)



SFX_LEVEL =1
MUSIC_LEVEL = 1

AUDIO_DIR = "assets/audio"

MUSIC_TRACK_DIR = AUDIO_DIR +"/music" +"/mainTrack.mp3" 

SFX_DIR =  AUDIO_DIR + "/mainTrack.mp3" 

CLICK_1_AUDIO_DIR = AUDIO_DIR + "/longclick.mp3"
SHORT_CLICK_AUDIO_DIR = AUDIO_DIR + "/click1.mp3"



sfx_json_path = os.path.join("src", "sfx.json")
SFX_DICT = {}

if os.path.exists(sfx_json_path):
    with open(sfx_json_path, "r", encoding="utf-8") as f:
        SFX_DICT = json.load(f)
else:
    print(" No SFX loaded!")

    

PLAY_MUSIC_START = False #play music at start


#IMAGES
IMAGE_CONVERSION_SIZE = 500

#TODO REPLACE WITH DICT



CURSOR_IMAGE_DIR =  "assets/images/ui/cursor.png"

# UI

DIRECTION_CARDINAL = ["E","N","W","S"] # 0 = East, 1 = North...

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


INVENTORY_SEPARATION = [150,100]
ORIGIN_INVENTORY = [1825,125]
INVENTORY_ITEMS_PADDING = 46
INVENTORY_TEXT_SIZE = 30



ORIGIN_ROOM_RANDOM_GROUP = [(0.7*screenWidth//2)//1,(0.7*screenHeight//2)//1]
RANDOM_GROUP_TILE_SIZE = 210
ORIGIN_ROOM_RANDOM_TEXT = [ORIGIN_ROOM_RANDOM_GROUP[0],ORIGIN_ROOM_RANDOM_GROUP[1]+RANDOM_GROUP_TILE_SIZE+10]
HORIZONTAL_PADDING_RANDOM_GROUP = 60
RANDOM_ROOM_TEXT_SIZE = 20


ROOM_GRID_SIZE_HORIZONTAL = 5
ROOM_GRID_SIZE_VERTICAL = 9

ROOM_TILE_SIZE = 100

ORIGIN_TILE = [100,90]

BIG_TILE = 250
ORIGIN_BIG_TILE = [screenWidth-BIG_TILE-65,screenHeight-BIG_TILE-65]



ROOM_INFO_PADDING = 85
ROOM_INFO_ORIGIN = [(ORIGIN_TILE[0]+0.85*ROOM_TILE_SIZE)//1,screenHeight-ROOM_INFO_PADDING]
ROOM_INFO_TEXT_SIZE = 14


NEXT_ROOM_SHOW = False
RANDOM_CURSOR_WIDTH = 6
RANDOM_CURSOR_WIDTH_COLOR = WHITE


DICE_TEXT_SUGGESTION_ORIGIN = [ORIGIN_ROOM_RANDOM_GROUP[0] + 3*RANDOM_GROUP_TILE_SIZE + 2* HORIZONTAL_PADDING_RANDOM_GROUP+5,ORIGIN_ROOM_RANDOM_GROUP[1]+5]
DICE_SUGGESTION_TEXT_SIZE = 15

ORIGIN_RANDOM_ROOM_COST = [ORIGIN_ROOM_RANDOM_GROUP[0],ORIGIN_ROOM_RANDOM_GROUP[1]-30]







ORIGIN_PRESS_ENTER_TEXT = [(ORIGIN_RANDOM_ROOM_COST[0] + 1*RANDOM_GROUP_TILE_SIZE + HORIZONTAL_PADDING_RANDOM_GROUP)//1,ORIGIN_ROOM_RANDOM_GROUP[1]-100]
ENTER_SUGGESTION_TEXT_SIZE = 20




ORIGIN_HISTORY = [ORIGIN_PRESS_ENTER_TEXT[0],ORIGIN_PRESS_ENTER_TEXT[1]+700]
HISTORY_TITLES_SIZE = 30





ORIGIN_ROOM_TEXT_INFO = [750,350]
ROOM_TEXT_SIZE = 50

ORIGIN_YOU_FOUND_TEXT = [ORIGIN_ROOM_TEXT_INFO[0],ORIGIN_ROOM_TEXT_INFO[1]+ROOM_TEXT_SIZE+10]
YOU_FOUND_TEXT_SIZE = 21

ORIGIN_ITEMS_IN_ROOM = [ORIGIN_YOU_FOUND_TEXT[0],ORIGIN_YOU_FOUND_TEXT[1]+75]
ITEMS_IN_ROOM_PADDING = 45
ITEM_TEXT_SIZE = 20


ITEMS_DESCRIPTION_DICT = {

    "gold": ["Coin","Use it to buy items","t",0,"TAKE","USE"], 
    "gems": ["Gem","Use it to buy special rooms","t",0,"TAKE"],
    "rabbits_foot": ["Rabbit's foot", "Greater chance of finding items","p",3,"TAKE","NAN"],
    "keys": ["Key","Useful for opening doors and chests","t",0,"TAKE","USE"],
    "apple": ["Apple", "Restores 2 steps", "t",2,"TAKE"],
    "banana": ["Banana", "Restores 3 steps", "t",2,"TAKE"],
    "lockpick": ["Lockpick", "You can now use the lockpick to open doors", "p",3,"TAKE"],
    "metal_detector": ["Metal Detector","Increases chances of finding extra gold or keys","p",3,"TAKE"],
    "dig_spots": ["Dig spot", "Use the shovel to dig and find items","a",0,"DIG"],
    "chest": ["Chest", "Use a key to open and find items", "a",3,"OPEN","NAN"],
    "shovel": ["Shovel", "You will need this to dig", "p",3,"TAKE","USE"],
    "dice": ["Dice","Use this to redraw rooms when drafting", "t",3,"TAKE","USE"],
    "steps_left": ["Step", "If you are seeing this text then something went really wrong", "t",0,"USE","TAKE"],
    "hammer": ["Hammer","Use this to break open chests without keys","p",3,"TAKE","USE"],
    "package": ["Package","A mysterious package. Who knows what is inside?","a",0,"OPEN","USE"]
    }


POSSIBLE_ITEMS_PER_ACTION_DICT = {
    "dig_spots": {"gold":[5,1],"keys":[5,1],"gems":[5,1]},
    "package": {"gold":[10,2],"keys":[3,1],"gems":[2,1],"rabbits_foot":[1,1]},
}


MAX_ITEMS_SHOW = 69 #montrer max MAX_ITEMS_SHOW items dans l'inventaire


CURSOR_ITEMS_ORIGIN = [ORIGIN_ITEMS_IN_ROOM[0]-100,ORIGIN_ITEMS_IN_ROOM[1]-5]


ORIGIN_DEBUG_TEXT = [CURSOR_ITEMS_ORIGIN[0],3*screenHeight//2]


PADDINGS_SPECIAL_ITEMS = 350

ORIGIN_SPECIAL_ITEMS = [screenWidth-PADDINGS_SPECIAL_ITEMS, screenHeight*0.4]
SPECIAL_ITEMS_TEXT_SIZE = 30
SPECIAL_ITEMS_PADDING = INVENTORY_ITEMS_PADDING