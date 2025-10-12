import math

# Screen settings

screenWidth = 1920
screenHeight = 1080


#Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game settings
fps = 60


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

    echelle = min(screenW / 16.0, screenH / 9.0)
    w = round(math.floor(16 * echelle))
    h = int(math.floor(9 * echelle))
    return(w,h)



