# TODO: Gère la grille complète du manoir et la génération des pièces.
# -> Fonction generate_room()

from src.room import Room  # import the class Room from room.py

from src import params

import random


class RoomGrid():
    def __init__(self,data):

        self.data = data
        self.grid = [[None for _ in range(params.ROOM_GRID_SIZE_VERTICAL)] for _ in range(params.ROOM_GRID_SIZE_HORIZONTAL)]
        
        self.rooms_data  = params.DICT_ROOM_ATTRIBUTES #dict with room attributes
        self.remaining_rooms = list(self.rooms_data.keys())

        entranceHallPos = [2,8]
        entranceHall = Room("Entrance_Hall",self.rooms_data ,entranceHallPos[0],entranceHallPos[1],"")
        antechamberPos = [2,0]
        
        antechamber = Room("Antechamber",self.rooms_data ,antechamberPos[0],antechamberPos[1],"")

        testRoom = Room("Parlor",self.rooms_data,entranceHallPos[0]+1,entranceHallPos[1],"")
        self.grid[testRoom.x][testRoom.y] = testRoom
        self.grid[entranceHall.x][entranceHall.y] = entranceHall
        self.grid[antechamber.x][antechamber.y] = antechamber
        self.randomGeneratedRooms = []
        

    def draw_random_rooms(self, n=3):
        """Retourne n chambres tirées aléatoirement selon leur rareté."""
        pool = []
        for name, data in self.rooms_data.items():
            # Plus la rareté est élevée, moins la pièce apparaît
            weight = 1 / (3 ** data["rarity"])
            pool.append((name, weight))
        names = random.choices(
            [name for name, _ in pool],
            weights=[w for _, w in pool],
            k=n
        )
        return [name for name in names]


    def create_room_instance(self, name):
        out = self.data.player.next_room_position
        x = out[0]
        y = out[1]

        """Instancie une Room à partir du JSON."""
        return Room(name,self.rooms_data, x, y,"")

    def generateRandomRooms(self):
        if(self.data.state_machine.generate_random_rooms_flag):
            
            self.data.state_machine.generate_random_rooms_flag = False
            self.data.state_machine.room_selection_mode  = True

            rooms = self.draw_random_rooms()
            self.randomGeneratedRooms = [self.create_room_instance(r) for r in rooms]
            

    def __repr__(self):

        return "\n".join(room.__repr__() for row in self.grid for room in row if room)
    
    def update(self):
        self.generateRandomRooms()
        self.data.manor = self.grid
        x,y = self.data.player.next_room_position
        nextRoom = self.data.manor[x][y]
        if(nextRoom is None):
            self.data.player.next_room_status = 0

        else:
            self.data.player.next_room_status = 1
