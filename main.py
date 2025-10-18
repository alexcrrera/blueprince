import pygame
import sys
import os
import time

from src import player
from src import params
from src import ui
from src import sound
from src import inputs
from src import data
from src import manor
import json, random
from src.room import Room  # import the class Room from room.py

# Constants



class Game:
    def __init__(self):
        pygame.init()

        self.screenHandler = ui.HandleScreen()
        self.clock = pygame.time.Clock()
        self.dataHandler = data.HandleData()

        self.playerHandler = player.Player()

        self.textHandler = ui.HandleText(self.screenHandler.screen,self.clock,self.playerHandler)
        
     
        self.dataHandler = data.HandleData()
        self.backgroundHandler = ui.HandleBackground(self.screenHandler.screen)
        self.audioHandler = sound.HandleSound(self.dataHandler)
        self.inputHandler = inputs.HandleInputs(self.dataHandler)

        self.running = True

        self.gridHandler = manor.RoomGrid(self.dataHandler)
        self.dataHandler.manor = self.gridHandler.mansion  # synchronisation
        self.gridUIHandler = ui.HandleGridUI(self.dataHandler, self.screenHandler.screen, self.playerHandler)

        
    def update(self):
        
        self.backgroundHandler.update()
        
        self.playerHandler.update()
        self.running = self.dataHandler.keep_running
        self.screenHandler.update()
        self.textHandler.update()
        self.inputHandler.update()
        self.handle_player_direction_and_move()
         
        self.audioHandler.update()
        self.gridHandler.update()
        self.gridUIHandler.update()
        pygame.display.flip()

    # def handle_player_movement(self):
    #     """Déplace le joueur avec ZQSD et tire une nouvelle Room après chaque mouvement."""
    #     moved = False

    #     if self.inputHandler.is_pressed(pygame.K_z):
    #         self.playerHandler.move(0, -1)
    #         moved = True
    #     elif self.inputHandler.is_pressed(pygame.K_s):
    #         self.playerHandler.move(0, 1)
    #         moved = True
    #     elif self.inputHandler.is_pressed(pygame.K_q):
    #         self.playerHandler.move(-1, 0)
    #         moved = True
    #     elif self.inputHandler.is_pressed(pygame.K_d):
    #         self.playerHandler.move(1, 0)
    #         moved = True

    #     if moved:
    #         # Charger les rooms du JSON
    #         with open("src/rooms.json", "r", encoding="utf-8") as f:
    #             rooms_data = json.load(f)

    #         # Exclure les salles spéciales du tirage
    #         excluded_rooms = ["Entrance_Hall", "Antechamber"]
    #         possible_rooms = {k: v for k, v in rooms_data.items() if k not in excluded_rooms}

    #         # Tirer une salle aléatoire parmi les autres
    #         random_room_name = random.choice(list(possible_rooms.keys()))
    #         room_info = possible_rooms[random_room_name]

    #         # Créer la salle à la position du joueur
    #         new_room = Room(random_room_name, room_info, self.playerHandler.x, self.playerHandler.y)

    #         # L’ajouter dans la grille
    #         self.gridHandler.mansion[self.playerHandler.x][self.playerHandler.y] = new_room

    #         print(f"Nouvelle Room tirée : {random_room_name} à {self.playerHandler.position}")


    def handle_player_direction_and_move(self):
        """Gestion du pointeur (selector) et déplacement confirmé."""
        moved = False

        # Changement de direction
        if self.inputHandler.is_pressed(pygame.K_z):
            self.playerHandler.selector_direction = "N"
            self.playerHandler.selector_visible = True
        elif self.inputHandler.is_pressed(pygame.K_s):
            self.playerHandler.selector_direction = "S"
            self.playerHandler.selector_visible = True
        elif self.inputHandler.is_pressed(pygame.K_q):
            self.playerHandler.selector_direction = "W"
            self.playerHandler.selector_visible = True
        elif self.inputHandler.is_pressed(pygame.K_d):
            self.playerHandler.selector_direction = "E"
            self.playerHandler.selector_visible = True

        # Déplacement confirmé
        elif self.inputHandler.is_pressed(pygame.K_SPACE) and self.playerHandler.selector_visible:
            dx, dy = 0, 0
            direction = self.playerHandler.selector_direction

            if direction == "N": dy = -1
            elif direction == "S": dy = 1
            elif direction == "W": dx = -1
            elif direction == "E": dx = 1

            x, y = self.playerHandler.x, self.playerHandler.y
            current_room = self.gridHandler.mansion[x][y]

            # Vérifie si la pièce actuelle a une porte ouverte dans cette direction
            if not current_room.has_open_door(direction):
                print(f"Pas de porte vers {direction} depuis {current_room.name}")
                self.playerHandler.selector_visible = False
                return

            # Position de la pièce cible
            new_x, new_y = x + dx, y + dy
            target_room = self.gridHandler.mansion[new_x][new_y]

            # Charger le JSON
            with open("src/rooms.json", "r", encoding="utf-8") as f:
                rooms_data = json.load(f)

            excluded_rooms = ["Entrance_Hall", "Antechamber"]
            possible_rooms = {k: v for k, v in rooms_data.items() if k not in excluded_rooms}

            # Si la salle n’existe pas encore, on en tire une aléatoire
            if target_room is None:
                random_room_name = random.choice(list(possible_rooms.keys()))
                room_info = possible_rooms[random_room_name]
                target_room = Room(random_room_name, room_info, new_x, new_y)

                # Teste jusqu'à 4 orientations pour trouver une porte correspondante
                for i in range(4):
                    if target_room.is_compatible_with(direction):
                        print(f"Orientation trouvée pour {target_room.name} après {i * 90}°")
                        break
                    else:
                        target_room.rotate_doors_90()  # tourne les portes ET l’image
                else:
                    print(f"Aucune orientation valide trouvée pour {target_room.name}, pièce bloquée.")
                    self.playerHandler.selector_visible = False
                    return

                # Ajout dans la grille
                self.gridHandler.mansion[new_x][new_y] = target_room

            # Connecter les deux pièces
            current_room.connect(direction, target_room)

            # Déplace le joueur
            self.playerHandler.move(dx, dy)
            self.playerHandler.selector_visible = False
            print(f"Nouvelle Room connectée : {target_room.name} à {self.playerHandler.position}")



    def run(self):
        while self.running:
            self.update()
            
            self.clock.tick(params.TARGET_FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    time.sleep(1)
    sys.exit()
