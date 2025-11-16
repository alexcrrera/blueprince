import pygame
import sys
import time

from src import player
from src import params
from src import ui
from src import sound
from src import inputs
from src import data


# =====================================================================
#  GAME
# =====================================================================


class Game:
    """
    Classe principale contrôlant tout le cycle du jeu.

    Responsabilités :
        - initialisation de tous les sous-systèmes (affichage, audio, inputs, data…)
        - création de la boucle principale
        - mise à jour de tous les gestionnaires à chaque frame
        - synchronisation de l’ordre d’exécution :
              Inputs > Player > Audio > UI > Data
        - gestion du framerate via pygame.time.Clock()

    Cette classe construit l’ensemble des handlers et les connecte entre eux :
        HandleData       > état global du jeu
        Player           > position/inventaire
        HandleScreen     > affichage du fond et fenêtre
        HandleText       > affichage textes
        HandleGridUI     > grille et tuiles
        HandleUI         > gestionnaire UI composite
        HandleSound      > sons & musique
        HandleInputs     > clavier


    Il s'agit d'un handler de handler de handler!
    """

    def __init__(self):
        """Initialise Pygame, instancie tous les gestionnaires et prépare la boucle de jeu."""
        pygame.init()

        # Handler Gestionnaire de l'écran principal
        self.screenHandler = ui.HandleScreen()

        # Horloge pour gérer le framerate
        self.clock = pygame.time.Clock()

        # Handler Gestionnaire global des données
        self.dataHandler = data.HandleData(self.clock)

        # Joueur
        self.playerHandler = player.Player(self.dataHandler) # player nécéssite data
        self.dataHandler.addPlayer(self.playerHandler) #  ajoute player
        self.dataHandler.secondaryInit()  # complète l'initialisation en initialisation le reste des classes intra-dataHandler

        #  Handler UI texte
        self.textHandler = ui.HandleText(self.dataHandler, self.screenHandler.screen)

        # Handler Audio
        self.audioHandler = sound.HandleSound(self.dataHandler)

        # Handler  clavier
        self.inputHandler = inputs.HandleInputs(self.dataHandler)

        # Handler UI graphique (grille)
        self.gridUIHandler = ui.HandleGridUI(self.dataHandler, self.screenHandler.screen)

        # Handler UI globale (interface principale)
        self.uiHandler = ui.HandleUI(self.dataHandler, self.screenHandler.screen)

        # Ajout des sous-handlers UI à la Handlerception
        self.uiHandler.addHandler(self.screenHandler)
        self.uiHandler.addHandler(self.gridUIHandler)
        self.uiHandler.addHandler(self.textHandler)

        self.running = True
       
    def update(self):
        """
        Exécuté à chaque frame.  
        Ordre important pour éviter les bugs :
            1. Inputs      > récolte des commandes utilisateur
            2. Player      > mise à jour position & inventaire
            3. Audio       > lecture des sons déclenchés
            4. UI          > affichage de l’interface
            5. Data        > mise à jour état global et logique interne
        """
        self.inputHandler.update()
        self.playerHandler.update()
        self.audioHandler.update()
        self.uiHandler.update()
        self.dataHandler.update()

    def run(self):
        """
        Boucle principale du jeu.  
        Continue tant que keep_running=True dans HandleData.
        """
        while self.dataHandler.keep_running:
            self.update()
            self.clock.tick(params.TARGET_FPS) # assure que nos FPS sont tels que ceux désirés



if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    time.sleep(1)
    sys.exit()
