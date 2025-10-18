# TODO: Gère la grille complète du manoir et la génération des pièces.
# -> Fonction generate_room()

from src.room import Room  # import the class Room from room.py

from src import params


class RoomGrid():
    def __init__(self,data):

  
        self.mansion = [[None for _ in range(params.ROOM_GRID_SIZE_VERTICAL)] for _ in range(params.ROOM_GRID_SIZE_HORIZONTAL)]

        entranceHallPos = [2,8]
        entranceHall = Room("Etrance Hall","blue",entranceHallPos[0],entranceHallPos[1], rarity = 0, cost = 0)

        self.mansion[entranceHall.x][entranceHall.y] = entranceHall
        


    def __repr__(self):
        
        return "\n".join(room.__repr__() for room in self.mansion)
        
            
    def update(self):   
        pass