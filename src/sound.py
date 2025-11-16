import pygame
from src import params
import random

class HandleSound:
    """
    Gère toute la partie audio du jeu :
        - musique de fond (loop)
        - effets sonores (SFX)
        - lecture conditionnelle de sons selon des flags HandleData

    Ce gestionnaire fonctionne entièrement par signaux :
        - chaque action déclenche un flag dans HandleData (ex: click_play)
        - HandleSound lit ces flags dans update()
        - puis joue le son correspondant et remet le flag à False

    Cette approche permet :
        - un découplage total entre gameplay et audio
        - un contrôle simple du mix audio
        - une extensibilité facile (ajout de nouveaux sons)
    """

    def __init__(self,data):
        """
        Initialise le gestionnaire audio.

        Args:
            data: Instance HandleData contenant les flags audio.
        """
        self.data = data
        # dir des fichirers
        self.music_path = params.MUSIC_TRACK_DIR
        self.sfx_folder_path = params.SFX_DIR # lié au json du son
        self.sfx_volume = params.SFX_LEVEL

        # Contiendra les sons individuels
        self.sfx = {}

        # Démarre la musique à un offset aléatoire, évite répétitivité 
        self.randomStartMusic = random.uniform(0,3500)
        self.playMusic() 

        # Dictionnaire des sons défini dans params
        self.sounds = params.SFX_DICT



    # ----------------- Music -----------------
    def playMusic(self):
        """
        Lance la musique principale en boucle (loop = -1),
        en commençant à un offset aléatoire.
        """
        pygame.mixer.music.load(params.MUSIC_TRACK_DIR)
        pygame.mixer.music.set_volume(self.data.music_level)
        pygame.mixer.music.play(loops=-1, start=self.randomStartMusic)

    def stopMusic(self):
        """
        Coupe la musique en mettant le volume à 0 (pas un vrai arrêt techniquement)
        """
        self.data.music_level = 0
        pygame.mixer.music.set_volume(self.data.music_level)
     

    def setMusicVolume(self):
        """
        Applique la valeur actuelle du volume de la musique.
        """
        volume = self.data.music_level
        self.music_volume = volume
        pygame.mixer.music.set_volume(volume)




    def playSFX(self, name):
        """
        Joue un effet sonore

        Args:
            name (str): Nom du son dans self.sounds.
        """
        sound = pygame.mixer.Sound(self.sounds.get(name))
        sound.play()
    


    def update(self):
        """
        Appelé à chaque frame.

        Vérifie tous les flags audio dans self.data et joue les sons associés.
        Chaque flag est remis à False après lecture.

        Les sons gérés :
            - longclick (choix principal)
            - click1/2/3 (petits clics UI)
            - door_lock_1/2
            - lockpick
            - grab
            - shovel
            - redraft
            - package
            - hammer
            - trunk
            - locker
        """

        # ---- Gestion musique ----
        if not self.data.music_play:
            self.stopMusic()
        else:
            self.data.music_level = params.MUSIC_LEVEL
            self.setMusicVolume()


        # ---- Gros clic (validation) ----
        if self.data.click_play:
            self.data.click_play = False
            self.playSFX("longclick")
             
        # ---- Petits clics (déplacement curseur) ----
        if self.data.small_click_play:
            self.data.small_click_play = False
            i = random.randint(1, 3)
            rand_audio = "click" + str(i)
            self.playSFX(rand_audio)

        # ---- Porte verrouillée ----
        if self.data.door_locked_play:
            self.data.door_locked_play = False
            # il y a deux sons disponibles pour éviter répétition son donc tirage aléatoire
            i = random.randint(1, 2)
            rand_audio = "door_lock_" + str(i)
            self.playSFX(rand_audio)
            
        # ---- Entrée dans une pièce ----
        if self.data.enter_room_play:
            self.data.enter_room_play = False
            # Aucun son car embêtant 


        # ---- Lockpick ----
        if self.data.lockpick_used_play:  
            self.data.lockpick_used_play = False
            self.playSFX("lockpick")
            pass

        # ---- Interactions d’objets (ramasser) ----
        if self.data.interact_play:
            self.data.interact_play = False
            self.playSFX("grab")

        # ---- Creuser ----
        if self.data.shovel_play:
            self.data.shovel_play = False
            self.playSFX("shovel")

        # ---- Redraft ----
        if self.data.room_redraft_play:
            self.data.room_redraft_play = False
            self.playSFX("redraft")

        # ---- Package (Mail Room) ----
        if self.data.mail_play:
            self.data.mail_play = False
            self.playSFX("package")

        # ---- Marteau ----
        if self.data.hammer_play:
            self.data.hammer_play = False
            self.playSFX("hammer")

        # ---- Coffre ----
        if self.data.trunk_play:
            self.data.trunk_play = False
            self.playSFX("trunk")

        # ---- Casier (Locker Room) ----
        if self.data.locker_play:
            self.data.locker_play = False
            self.playSFX("locker")
