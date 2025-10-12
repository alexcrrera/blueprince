import math

# Screen settings
DEFAULT_SCREEN_WIDTH= 1920
DEFAULT_SCREEN_HEIGHT = 1080
screenWidth = DEFAULT_SCREEN_WIDTH #taille image horizontal par défaut
screenHeight = DEFAULT_SCREEN_HEIGHT #taille image vertical par défaut
USE_DEFAULT_SCREEN_SIZE = True

#Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game settings
fps = 60
splitRatioScreen = 0.33 # ratio entre côté gauche et droite

SFX_LEVEL =0.5
MUSIC_LEVEL = 0.4

AUDIO_DIR = "assets/audio"

MUSIC_TRACK_DIR = AUDIO_DIR +"/music" "/mainTrack.mp3" 

SFX_DIR =  AUDIO_DIR + "/mainTrack.mp3" 

PLAY_MUSIC = True

def getScreenSize(screenW:int,screenH:int)->int:
    """   
    Fonction qui vérifie quelle taille (en pixels) maximale on peut avoir de sorte à avoir un ratio
    d'image 16:9 et minimiser la bordure

    Parametres:
    screenW:int - taille écran horizontal
    screenH:int - taille écran verticale

    Retourne:
    w,h:int - taille finale telle que aspect ratio conservé et taille image conservée
    """
    if(USE_DEFAULT_SCREEN_SIZE):
        return(DEFAULT_SCREEN_WIDTH,DEFAULT_SCREEN_HEIGHT)
    echelle = min(screenW / 16.0, screenH / 9.0)
    w = round(math.floor(16 * echelle))
    h = int(math.floor(9 * echelle))

    return(w,h)



