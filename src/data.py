from src import params
from src import room_library
from src import state_machine
from src import handler

class HandleData(handler.BaseHandler):
    """
    Contient toutes les données globales du jeu.

    Cette classe regroupe :
        - l’état global du jeu (game over, flags, états des interactions)
        - les références vers Player, StateMachine et RoomGrid
        - les effets spéciaux globaux appliqués aux tirages d’objets/salles
        - les informations affichées dans le UI (textes, historique, debug)
        - les flags utilisés par l’audio (clicks, sons d’interactions)

    Elle hérite de  BaseHandler

    C’est le conteneur principal entre tous les sous-systèmes du jeu.
    """
    
    def __init__(self,clock):
        """
        Initialise les champs minimaux nécessaires avant le second init.

        Args:
            clock: Référence au pygame.time.Clock() principal.
        """
        super().__init__()
        
        self.keep_running = True          # Contrôle principal de la boucle de jeu
        self.player = None                # Le joueur sera ajouté plus tard
        self.clock = clock                # Horloge pour le calcul FPS/temps


    def secondaryInit(self):
        """
        Effectue l'initialisation complète des systèmes après avoir ajouté le joueur.
        Ceci permet d'éviter des dépendances circulaires.

        Initialise :
            - state_machine
            - gridHandler
            - flags d'interactions
            - flags UI
            - effets globaux (veranda, furnace, etc.)
            - texte d'historique et debug
        """

        # Gestionnaires principaux
        self.state_machine =  state_machine.StateMachineHandler(self)
        self.gridHandler = room_library.RoomGrid(self)


        # flags pour inputs 
        self.space_pressed = False
        self.enter_pressed = False
        self.redraft_pressed = False
        self.interact_pressed = False # si F appuyé - interaction avec item dans chambre
        self.counter_inventory = 0 # pour curseur objets

        # État musique
        self.music_play = params.PLAY_MUSIC_START # bool pour savoir si musique on quand début game
        self.music_level = params.MUSIC_LEVEL # volume musique

        # flags pour le son
        self.enter_room_play = False # sfx pour quand on rentre chambre
        self.click_play = False # sfx pour "grand" click 
        self.small_click_play = False # sfx pour "petit" click
        self.door_locked_play = False # sfx pour porte bloquée
        self.interact_play = False # sfx pour quand F appuyé
        self.room_redraft_play = False  #sfx pour quand dé utilisé
        self.shovel_play = False #sfx pêle
        self.mail_play = False #sfx pour colis
        self.trunk_play = False #sfx pour coffre
        self.hammer_play = False #sfx pour marteau
        self.locker_play = False #sfx pour ouverture casier
        self.lockpick_used_play = False # sfx pour utilisation lockpick

        # Sélection de salle (random draw)
        self.counter_room_selection_cursor = 0 # compteur pour curseur choix chambre choisie 0 = première chambre 2 = dernière (3ème)
        
        
        # Game over : [bool, type de gameover: 1 = plus de pas, 2 = victoire]
        self.game_over = [False,-1]


        # Texte pour UI
        self.history_text = "You enter a manor"


        # Effets globaux de salles
        self.dark_room_effect = False
        self.veranda_effect = True
        self.maid_chamber_effect = False
        self.green_house_effect = False
        self.furnace_effect = True



    def addPlayer(self,player):
        """
        Ajoute la référence vers l'objet Player.

        Args:
            player: Instance de Player.
        """
        self.player = player

    
    

    def updateDebugText(self,txt):
        """
        Met à jour le texte affiché dans la zone d'historique.

        Args:
            txt (str): Texte à afficher.
        """
        self.history_text = txt

    
    def updateHistory(self,what,q,verb=None):
        """
        Construit une phrase descriptive d’un événement (gain/perte d’objet).

        Utilisé pour informer le joueur.

        Args:
            what (str): Nom interne de l'objet.
            q (int): Quantité.
            verb (str or None): Verbe décrivant l'action (default = "use").
        """
        if verb  is None:
            verb = "use" #défaut
   
        descript_dict = params.ITEMS_DESCRIPTION_DICT.get(what)
        
        if q == 0:
            return
        
        txt  = "You " + verb + " "
        thing = descript_dict[0] # texte pour UI

        # Articles, déterminants, pluriels selon q et type d’objet
        if q == 1:
            # t = temporaire → article indéfini
            if descript_dict[2] == "t":
                txt += "one " # si objet temp. alors on préfixe par "un"
                txt += thing.lower()
            else:
                txt += " the " # Si objet important alors on préfixe par "the" = "le"
                txt += thing
        else:
            txt+= str(q) + " x " # sinon format q x
            txt += thing.lower()
            
        is_s = "s" if q > 1 else "" # ajoute s si plusieurs objets présents
        txt += is_s

        self.history_text = txt # mise à jour du text utilisé par UI

    def update(self):
        """
        Appelé à chaque frame. Met à jour :
            - détection des conditions de fin de partie
            - mise à jour de la state machine
            - mise à jour de la grille de pièces

        
        """

        # Condition 1 : joueur n'a plus de pas
        if(self.player.inventory.getItemQ("steps_left")==0):
            self.game_over = [True,1]
            self.state_machine.mode = -1
        
        # Condition 2 : joueur atteint l’Antechamber
        if(self.player.x==2 and self.player.y ==0):
            self.game_over = [True,2]
            self.state_machine.mode = -1
       
        # Mise à jour des systèmes secondaires
        self.state_machine.update()
        self.gridHandler.update()
