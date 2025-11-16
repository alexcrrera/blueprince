

import json
import os



"""
===============================================================================
PARAMÈTRES GLOBAUX DU JEU
Ce fichier regroupe toutes les constantes utilisées par :

    - l’affichage
    - l’UI
    - l’audio
    - la grille de salles
    - les items
    - les chambres
    - le joueur

Aucune logique : uniquement des données et paramètres de configuration.
===============================================================================
"""
# ============================================================================
# 1) CONFIGURATION DE L'ÉCRAN
# =============

DEFAULT_SCREEN_WIDTH = 1920
DEFAULT_SCREEN_HEIGHT = 1080
    
screenWidth = DEFAULT_SCREEN_WIDTH #taille image horizontal par défaut
screenHeight = DEFAULT_SCREEN_HEIGHT #taille image vertical par défaut


# ============================================================================
# 2) CONSTANTES  COULEURS ET AFFICHAGE
# ============================================================================

#Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0,255,0)
GRAY = (100,100,100)
LIGHT_GRAY = (200,200,200)
RED = (220,0,0)
YELLOW = (255, 200, 0)

BG_COLOR = (30, 30, 30)

DARK_BLUE_COLOR = (30,70,136)



# ============================================================================
# 3) CONFIGURATION DU JEU (FPS, inventaire initial…)
# ============================================================================
# Game settings
TARGET_FPS = 100




INITIAL_STEPS = 70
INTIAL_GOLD = 0
INITIAL_GEMS = 2
INTIAL_KEY =0
INTIAL_DICE = 0

INITIAL_ITEMS_DICT ={
    "steps_left": INITIAL_STEPS,
    "gems": INITIAL_GEMS,
    "gold": INTIAL_GOLD,
    "keys": INTIAL_KEY,
    "dice": INTIAL_DICE

}

# ============================================================================
# 4) CHARGEMENT DES DONNÉES EXTERNES
# ============================================================================

# Chargement des chambres
json_path = os.path.join("src", "rooms.json")
DICT_ROOM_ATTRIBUTES = {}
with open(json_path, "r") as file:
    DICT_ROOM_ATTRIBUTES = json.load(file)

# Chargement des effets sonores
sfx_json_path = os.path.join("src", "sfx.json")
SFX_DICT = {}

if os.path.exists(sfx_json_path):
    with open(sfx_json_path, "r", encoding="utf-8") as f:
        SFX_DICT = json.load(f)
else:
    print(" No SFX loaded!")


# ============================================================================
# 5) PARAMÈTRES AUDIO
# ============================================================================

SFX_LEVEL =1
MUSIC_LEVEL = 1

AUDIO_DIR = "assets/audio"

MUSIC_TRACK_DIR = AUDIO_DIR +"/music" +"/mainTrack.mp3" 

SFX_DIR =  AUDIO_DIR + "/mainTrack.mp3" 

CLICK_1_AUDIO_DIR = AUDIO_DIR + "/longclick.mp3"
SHORT_CLICK_AUDIO_DIR = AUDIO_DIR + "/click1.mp3"

PLAY_MUSIC_START = True #jouer musique au débu

# ============================================================================
# 6) PARAMÈTRES D'IMAGES
# ============================================================================

IMAGE_CONVERSION_SIZE = 500 # taille des images lors de la conversion .webp à .jpg
CURSOR_IMAGE_DIR =  "assets/images/ui/cursor.png"


# ============================================================================
# 7) PARAMÈTRES UI (textes, polices, bordures…)
# ============================================================================
TEXT_COLOR = (255, 255, 255)

FONT_SIZE = 30


PADDING_FPS = 20 

SMALL_FONT_SIZE = 10
DEFAULT_FONT_SIZE = 20
SPECIAL_FONT_SIZE = 30

ALT_DEFAULT_SIZE= DEFAULT_FONT_SIZE

SMALL_TEXT_DIR = "assets/fonts/Helvetica.ttf"
DEFAULT_TEXT_DIR = "assets/fonts/Helvetica.ttf"
SPECIAL_TEXT_DIR = "assets/fonts/damnarc.ttf"
ALT_DEFAULT_TEXT_DIR = "assets/fonts/Coolvetica Rg.otf"


# ============================================================================
# 8) PARAMÈTRES DE LA GRILLE DU MANOIR
# ============================================================================
ROOM_GRID_SIZE_HORIZONTAL = 5
ROOM_GRID_SIZE_VERTICAL = 9
ROOM_TILE_SIZE = 100 # taille en pixels des chambres dans la grille



# ============================================================================
# 9) PARAMÈTRES POUR UI
# ============================================================================

# UI: AFFICHAGE GRILLE
ORIGIN_TILE = [100,90]#ORIGINE 

# UI: AFFICHAGE GRANDE IMAGE DE CHAMBRE (EN BAS DROITE)
BIG_TILE = 250
ORIGIN_BIG_TILE = [screenWidth-BIG_TILE-65,screenHeight-BIG_TILE-65]


# UI: AFFICHAGE INVENTAIRE
ORIGIN_INVENTORY = [1825,125]
INVENTORY_ITEMS_PADDING = 46
INVENTORY_TEXT_SIZE = 30


# UI: AFFICHAGE CHAMBRES GÉNÉRÉES - AFFICHAGE IMAGE

ORIGIN_ROOM_RANDOM_GROUP = [(0.7*screenWidth//2)//1,(0.7*screenHeight//2)//1] # origine chambres tirés aléatoirement
RANDOM_GROUP_TILE_SIZE = 210
ORIGIN_ROOM_RANDOM_TEXT = [ORIGIN_ROOM_RANDOM_GROUP[0],ORIGIN_ROOM_RANDOM_GROUP[1]+RANDOM_GROUP_TILE_SIZE+10]
HORIZONTAL_PADDING_RANDOM_GROUP = 60
RANDOM_ROOM_TEXT_SIZE = 15

# UI AAFFICHE CHAMBRES GÉNÉRÉE - INFO POUR LES DÉS
DICE_TEXT_SUGGESTION_ORIGIN = [ORIGIN_ROOM_RANDOM_GROUP[0] + 3*RANDOM_GROUP_TILE_SIZE + 2* HORIZONTAL_PADDING_RANDOM_GROUP+5,ORIGIN_ROOM_RANDOM_GROUP[1]+5]
DICE_SUGGESTION_TEXT_SIZE = 15 # taille suggestion utilisation du dés


# UI CHAMBRES GÉNÉRÉES TIRAGE - AFFICHAGE COÛT
ORIGIN_RANDOM_ROOM_COST = [ORIGIN_ROOM_RANDOM_GROUP[0],ORIGIN_ROOM_RANDOM_GROUP[1]-30] # affiche coût de la chambre

# UI CHAMBRES GÉNÉRÉES TIRAGE - DESCRIPTION CHAMBRE
ORIGIN_RANDOM_ROOM_GROUP_DESCRIPTION = [ORIGIN_ROOM_RANDOM_GROUP[0]+HORIZONTAL_PADDING_RANDOM_GROUP+RANDOM_GROUP_TILE_SIZE*1.25,ORIGIN_ROOM_RANDOM_GROUP[1]+RANDOM_GROUP_TILE_SIZE+90]
DESCRIPTION_TEXT_SIZE = 20

#UI: AFFICHAGE CURSEUR POUR CHOIX CHAMBRE

RANDOM_CURSOR_WIDTH = 6 # epeisseur
RANDOM_CURSOR_WIDTH_COLOR = WHITE #couleur du curseur


# UI: AFFICHAGE SUGGESTION TEXTUELLE SELON CONTEXT

ORIGIN_PRESS_ENTER_TEXT = [(ORIGIN_RANDOM_ROOM_COST[0] + 1*RANDOM_GROUP_TILE_SIZE + HORIZONTAL_PADDING_RANDOM_GROUP)//1,ORIGIN_ROOM_RANDOM_GROUP[1]-100]
ENTER_SUGGESTION_TEXT_SIZE = 20



# UI: AFFICHAGE HISTORIQUE ACTIONS
ORIGIN_HISTORY = [ORIGIN_PRESS_ENTER_TEXT[0]+150,ORIGIN_PRESS_ENTER_TEXT[1]+700]
HISTORY_TITLES_SIZE = 30


# UI: AFFICHAGE NOM CHAMBRE
ROOM_TEXT_SIZE = 50 # Taille nom de la chambre

# UI: AFFICHAGE TEXT "YOU FOUND"
ORIGIN_ROOM_TEXT_INFO = [750,350]
ORIGIN_YOU_FOUND_TEXT = [ORIGIN_ROOM_TEXT_INFO[0],ORIGIN_ROOM_TEXT_INFO[1]+ROOM_TEXT_SIZE+10]
YOU_FOUND_TEXT_SIZE = 21


# UI: AFFICHAGE TEXT ITEMS DANS CHAMBRE
ORIGIN_ITEMS_IN_ROOM = [ORIGIN_YOU_FOUND_TEXT[0],ORIGIN_YOU_FOUND_TEXT[1]+75]
ITEMS_IN_ROOM_PADDING = 45
ITEM_TEXT_SIZE = 20 # taille text item dans chambre


# UI: AFFICHAGE CURSEUR DES ITEMS/ACTIONS DANS CHAMBRE
CURSOR_ITEMS_ORIGIN = [ORIGIN_ITEMS_IN_ROOM[0]-100,ORIGIN_ITEMS_IN_ROOM[1]-5]



# UI: AFFICHAGE INFO SUR STATUT PROCHAINE CHAMBRE (OUVERTE, MUR...)
ROOM_INFO_PADDING = 85
ROOM_INFO_ORIGIN = [(ORIGIN_TILE[0]+0.85*ROOM_TILE_SIZE)//1,screenHeight-ROOM_INFO_PADDING]
ROOM_INFO_TEXT_SIZE = 14


# UI: AFFICHAGE ITEMS SPECIFAUX AFFICHAGE INVENTAIRE JOUEUR
PADDINGS_SPECIAL_ITEMS = 350
ORIGIN_SPECIAL_ITEMS = [screenWidth-PADDINGS_SPECIAL_ITEMS, screenHeight*0.4]
SPECIAL_ITEMS_TEXT_SIZE = 30
SPECIAL_ITEMS_PADDING = INVENTORY_ITEMS_PADDING



# ============================================================================
# 12) DICTIONNAIRE DES ITEMS
# ============================================================================


ITEMS_DESCRIPTION_DICT = {
    # nom interne: [nom displayed, phrase descriptive displayed, type tempo/permanent ou action, rareté, verbe si ajoute par utilisateur, verbe si utilisé par utilisateur]

    "gold": ["Coin","Use it to buy items","t",1,"TAKE","USE"], 
    "gems": ["Gem","Use it to buy special rooms","t",2,"TAKE","USE"],
    "rabbits_foot": ["Rabbit's foot", "Greater chance of finding items","p",3,"TAKE","NAN"],
    "keys": ["Key","Useful for opening doors and chests","t",1,"TAKE","USE"],
    "apple": ["Apple", "Restores 2 steps", "t",2,"TAKE","BUY"],
    "banana": ["Banana", "Restores 3 steps", "t",2,"TAKE","BUY"],
    "lockpick": ["Lockpick", "You can now use the lockpick to open doors", "p",3,"TAKE","USE"],
    "metal_detector": ["Metal Detector","Increases chances of finding extra gold or keys","p",3,"TAKE","USE"],
    "dig_spots": ["Dig spot", "Use the shovel to dig and find items","a",2,"DIG","DIG"],
    "trunk": ["Trunk", "Use a key or the hammer to open and find items", "a",3,"OPEN","NAN"],
    "shovel": ["Shovel", "You will need this to dig", "p",3,"TAKE","USE"],
    "dice": ["Dice","Use this to redraw rooms when drafting", "t",2,"TAKE","USE"],
    "steps_left": ["Step", "", "t",0,"GAIN","USE"],
    "hammer": ["Hammer","Use this to break open chests without keys","p",3,"TAKE","USE"],
    "package": ["Package","A mysterious package. Who knows what is inside?","a",1,"OPEN","USE"],
    "apple_buy":["Apple", "Buy an apple - 2 coins", "a",0,"BUY","NAN"],
    "banana_buy":["Banana", "Buy a banana - 3 coins", "a",1,"BUY","NAN"],
    "cake_buy":["Cake", "Buy a cake - 6 coins", "a",2,"BUY","NAN"],
    "sandwich_buy":["Sandwich", "Buy a sandwich - 8 coins", "a",3,"BUY","NAN"],
    "meal_buy":["Meal", "Buy a meal - 15 coins", "a",3,"BUY","NAN"],
    "locker": ["Locker", "Use a key to open a locke","a",1,"OPEN","OPEN"],
    }

# ============================================================================
# 13) DICTIONNAIRE DES ITEMS POSSIBLES/ACTION
# ============================================================================

POSSIBLE_ITEMS_PER_ACTION_DICT = {
    "dig_spots": {"gold":[5,1],"keys":[3,1],"gems":[2,1]},
    "package": {"gold":[10,1],"keys":[2,1],"gems":[1,1],"rabbits_foot":[1,1]},
    "trunk": {"keys":[2,1], "gems":[2,1], "gold":[3,0], "dice":[2,0],"lockpick":[1,0]},
    "locker": {"gems":[1,0],"gold":[5,1],"apple":[1,0],"keys":[1,0]}
}

# ============================================================================
# 14) CONSOMMABLES ACHETABLES / COÛT ET EFFET
# ============================================================================


POSSIBLE_CONSUMABLES_DICT = {
    "apple": {"gives":2,"costs":2},
    "banana": {"gives":3,"costs":3},
    "cake": {"gives":10,"costs":6},
    "sandwich": {"gives":15,"costs":8},
    "meal": {"costs":15,"gives":20},
}


