# TODO: Gère la grille complète du manoir et la génération des pièces.
# -> Fonction generate_room()

from src.room import Room  # import the class Room from room.py

from src import params

import random


class RoomGrid():
    def __init__(self,data):
        self.space_counter = 0
        self.data = data
        self.grid = [[None for _ in range(params.ROOM_GRID_SIZE_VERTICAL)] for _ in range(params.ROOM_GRID_SIZE_HORIZONTAL)]
        
        self.rooms_data  = params.DICT_ROOM_ATTRIBUTES #dict with room attributes
        self.remaining_rooms = list(self.rooms_data.keys())

        entranceHallPos = [2,8]
        entranceHall = Room("Entrance_Hall",self.rooms_data ,entranceHallPos[0],entranceHallPos[1],0)
        antechamberPos = [2,0]
        
        antechamber = Room("Antechamber",self.rooms_data ,antechamberPos[0],antechamberPos[1],0)
        testRoom3 =  Room("Parlor",self.rooms_data,entranceHallPos[0]+2,entranceHallPos[1],0)
        testRoom2 = Room("Parlor",self.rooms_data,entranceHallPos[0]-1,entranceHallPos[1],0)
        testRoom = Room("Parlor",self.rooms_data,entranceHallPos[0]+1,entranceHallPos[1],0)
        self.grid[testRoom2.x][testRoom2.y] = testRoom2
        self.grid[testRoom3.x][testRoom3.y] = testRoom3
        self.grid[testRoom.x][testRoom.y] = testRoom
        self.grid[entranceHall.x][entranceHall.y] = entranceHall
        self.grid[antechamber.x][antechamber.y] = antechamber
        self.randomGeneratedRooms = []


        self.current_room = self.grid[self.data.player.x][self.data.player.y]
        self.next_room = self.grid[self.data.player.next_room_position[0]][self.data.player.next_room_position[1]]
    
        self.next_room_status = -1
        # -1 = empty, 0 = wall, 1 = unlocked, 2 = locked, 3 = locked twice

    def checkRoomConnection(self):
        if(self.next_room is None):
            return(-1)
        if(self.data.player.direction == 1): # Nord
            if(self.next_room.doors[3] == 1):
                return(1)

        if(self.data.player.direction == 2): # Ouest
            if(self.next_room.doors[0] == 1):
                return(1)

        if(self.data.player.direction == 3): # Sud
            if(self.next_room.doors[1] == 1):
                return(1)

        if(self.data.player.direction == 0): # Est
            if(self.next_room.doors[2] == 1):
                return(1)
        return(0)

        #curr_room = self.current

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


    def create_room_instance(self, name,rotation=0):
        out = self.data.player.next_room_position
        x = out[0]
        y = out[1]

        """Instancie une Room à partir du JSON."""
        return Room(name,self.rooms_data, x, y,rotation)

    def generateRandomRooms(self):
        if(self.data.state_machine.generate_random_rooms_flag):
            
            self.data.state_machine.generate_random_rooms_flag = False
            self.data.state_machine.room_selection_mode  = True

            rooms = self.draw_random_rooms()
            # il fqut remplacer create_room_instance out impleme
            self.randomGeneratedRooms = [self.create_room_instance(r) for r in rooms]
            

    def __repr__(self):

        return "\n".join(room.__repr__() for row in self.grid for room in row if room)
    
    def update(self):

        self.generateRandomRooms()
        self.data.manor = self.grid

        self.current_room = self.grid[self.data.player.x][self.data.player.y]

        self.next_room = self.grid[self.data.player.next_room_position[0]][self.data.player.next_room_position[1]]
       
        self.data.player.next_room_status = self.checkRoomConnection()
