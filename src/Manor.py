# TODO: Gère la grille complète du manoir et la génération des pièces.
# -> Fonction generate_room()

from room import Room  # import the class Room from room.py

from src import params


class RoomGrid():
    def __init__(self,data):
        self.grid_vertical = params.ROOM_GRID_SIZE_VERTICAL
        self.grid_horizontal = params.ROOM_GRID_SIZE_HORIZONTAL
    
  
        self.mansion = [[Room() for _ in range( self.grid_horizontal)] for _ in range(self.grid_vertical)]

        entranceHallPos = [2,0]
        entranceHall = Room("Etrance Hall","blue",entranceHallPos[0],entranceHallPos[1], rarity = 0, cost = 0)

        self.mansion.append(entranceHall)
        


    def __repr__(self):
        for room in self.mansion:
            room.__repr__
    def update(self):   
        pass