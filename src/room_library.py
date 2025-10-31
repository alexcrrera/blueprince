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
        entranceHall = Room("Entrance_Hall",self.rooms_data ,entranceHallPos[0],entranceHallPos[1])
        antechamberPos = [2,0]
        
        antechamber = Room("Antechamber",self.rooms_data ,antechamberPos[0],antechamberPos[1])
        # testRoom3 =  Room("Parlor",self.rooms_data,entranceHallPos[0]+2,entranceHallPos[1],0)
        # testRoom2 = Room("Parlor",self.rooms_data,entranceHallPos[0]-1,entranceHallPos[1],0)
        # testRoom = Room("Parlor",self.rooms_data,entranceHallPos[0]+1,entranceHallPos[1],0)
        # self.grid[testRoom2.x][testRoom2.y] = testRoom2
        # self.grid[testRoom3.x][testRoom3.y] = testRoom3
        # self.grid[testRoom.x][testRoom.y] = testRoom
        self.grid[entranceHall.x][entranceHall.y] = entranceHall
        self.grid[antechamber.x][antechamber.y] = antechamber
        self.gridImages = [[None for _ in range(params.ROOM_GRID_SIZE_VERTICAL)] for _ in range(params.ROOM_GRID_SIZE_HORIZONTAL)]
        self.randomGeneratedRooms = []


        self.current_room = self.grid[self.data.player.x][self.data.player.y]
        self.next_room = self.grid[self.data.player.next_room_position[0]][self.data.player.next_room_position[1]]
    
        self.next_room_status = -1
        #  -1 = empty, 0 = wall, 1 = unlocked, 2 = locked, 3 = locked twice

    def checkRoomConnection(self,next_room=2):
#               ↑                      
#               N (1)                      
#               |                      
#     W (2) ← - ● - → E (0)            
#               |                        
#               S (3)                    
#               ↓         
        if(next_room==2):
            next_room = self.next_room  # si aucun argument passe alors on check room connection avec next room
        #sinon on compare avec la chambre passee en argument
            
        current_room = self.current_room
        if(current_room is None) :
            return -2
        
        dir =  self.data.player.direction
        
        if next_room is None:
            if(current_room.doors[self.data.player.direction]==1):
                
                if(current_room.door_status[dir]==1):
                    return -1 # we can generate it 
                else:
                    return current_room.door_status[dir]
                
            else:
                return 0 #wall of 2nd type


        

        # check s'il y a une porte existente
        
        dir_opposed = (dir+2)%4
        if(current_room.doors[dir] ==1 and  next_room.doors[dir_opposed]==1):
                return(current_room.door_status[dir])
      

        return 0


    def draw_random_room(self, initial_rotation,exclusions):

        """
        Retourne UNE seule chambre tirée aléatoirement selon sa rareté,
        en excluant certaines pièces (par défaut : Antechamber, Entrance_Hall).
        """
        excluded_rooms = ["Antechamber", "Entrance_Hall"]
        #print("Exclusions: ", exclusions)
        pool = []
        for name, data in self.rooms_data.items():
            # Ignore les pièces interdites
            if name in excluded_rooms or name in exclusions:
                continue
            q = self.rooms_data[name]["q"]
            if(q<1): # chambre plus dispo
              #  print("no q  ", name)
                continue

            condition = data["placement_condition"]
            x,y = self.data.player.next_room_position[0],self.data.player.next_room_position[1]

            if not((self.checkPlacememtCondition(x0=x,y0=y,cond=condition)==1)):
               #@ print("pas boonne post POUR ", name)
                continue

           
            # Plus la rareté est élevée, moins la pièce apparaît
            weight = 1 / (3 ** data["rarity"])
            pool.append((name, weight))


        print("Pool: ",pool)
        if not pool:
            raise ValueError("Aucune pièce disponible pour le tirage (toutes exclues).")

        # Tirage d'une seule pièce
        name = random.choices(
            [name for name, _ in pool],
            weights=[w for _, w in pool],
            k=1
        )[0]

        room = self.create_room_instance(name,initial_rotation) # -1 car les images sont orientées vers le haut (N) par défaut
        return [room,name]



    def openDoor(self):
        current_room  = self.current_room
        dir = self.data.player.direction
        current_room.door_status[dir] += -1



    def create_room_instance(self, name,rotation=0):
        out = self.data.player.next_room_position
        x = out[0]
        y = out[1]
        

        """Instancie une Room à partir du JSON."""
        return Room(name,self.rooms_data, x, y,rotation)


    def checkPlacememtCondition(self,room=None,x0=-1,y0=-1,cond=-1):
        """Vérifie si nous respectons les conditions de placement
        0: Aucune condition
        1: Si dans coins
        2: si dans extrêmités


        """

        if(room==None):
            x = x0
            y = y0
            condition = cond
        else:

            x,y = room.x,room.y
            condition = room.placement_condition
        if(condition==0):
            return 1
        
        if(condition==1):
            c1 = x== 0 and y ==0 #coin haut gauche
            c2 = x== 0 and y == params.ROOM_GRID_SIZE_VERTICAL-1  #coin bas gauche
            c3 = x == params.ROOM_GRID_SIZE_HORIZONTAL-1 and y == 0 #coin droite haut
            c4 = x == params.ROOM_GRID_SIZE_HORIZONTAL-1 and y == params.ROOM_GRID_SIZE_VERTICAL-1 #coin droite bas
            
            if(c1 or c2 or c3 or c4):
                return 1
            

        return -1

        
    def generateRandomRooms(self):
        if(self.data.state_machine.generate_random_rooms_flag):
            
            self.data.state_machine.generate_random_rooms_flag = False
            self.data.state_machine.room_selection_mode  = True

            r_out =    list()
            index = 0
            gem_cost_0 = False
            exclude = set() # rooms a temp. exclure pour eviter doublons
            print("Starting room generation COMPLETE============")
            while(index<3):

                intra_good = False
                attemps = 0
                prev_room = ""
             #   print("START GEN OOMS")
                while(not intra_good):
                        rt = 0

                        
                        r,name = self.draw_random_room(self.data.player.direction,exclude)
                        attemps +=1
                        #print("New room: ",name)
                        if(attemps>200):
                            raise TypeError("Not enough rooms included oops")
                        if(r is None):
                            raise TypeError("Ooops you generated an empty room")
                        print("STARTING CHECK FOR ",name," - rot: ",r.room_rotation)

                        for i in range(3): # faire max 3 rotations
                           # print(i, " - Rotation ", rt, " is there a door?", self.checkRoomConnection(r)==1,r.doors)
                            x,y = self.data.player.next_room_position
                            if self.checkRoomConnection(r)==1:
                                print("Door connection, i: ", i)
                                intra_good = True

                            if(x==0 and r.doors[2]==1): #cote gauche
                                intra_good = False
                               # print("door west not good")
                            if(y==params.ROOM_GRID_SIZE_VERTICAL-1 and r.doors[3]==1): #cote gauche 
                                intra_good = False
                               # print("door south not good")
                            if(x==params.ROOM_GRID_SIZE_HORIZONTAL-1 and r.doors[0]==1):
                                intra_good = False
                              #  print("door east not good")
                            if(y==0 and r.doors[1]==1): #cote gauche 
                                intra_good = False
                              #  print("door north not good")
                           
         
                           

                            if(index==2 and not(gem_cost_0)):
                                print("Need a 0 cost room")
                                intra_good = False # il faut au moins une pièce avec un coût de 0 gèmmes
                                    


                            if(not intra_good):
                                rt +=1
                                #print("turning room outside of creation")
                               
                                r.rotate_90_trigo()
                                
                                
                            if(intra_good):
                                break # room suits us
                        print("Turned twice no good")
                        if(not intra_good):
                            print("Removing from pool: ",name)


                            exclude.add(name)
                            

                print("added: ",name,r.room_rotation,index)
                            
                exclude.add(name)
                r_out.append(r)
                
                if(r.cost<1):
                    gem_cost_0 = True

                print(r.__repr__())
                index +=1
            

        
            self.randomGeneratedRooms = r_out
            

    def updateDoors(self):

        current_room  = self.current_room
        next_room = self.next_room
        if(next_room is None):
            return

        dir = self.data.player.direction
        current_room_door_status = current_room.door_status[dir]
        dir_opposed = (dir +2)%4
        next_room_door_status = next_room.door_status[dir_opposed]



        if(current_room_door_status == 1):
            current_room_door_status == 1
             
        else:
            current_room_door_status = max(current_room_door_status,next_room_door_status)

        current_room.door_status[dir] = current_room_door_status
        next_room.door_status[dir_opposed] = current_room_door_status



    def __repr__(self):

        return "\n".join(room.__repr__() for row in self.grid for room in row if room)
    


    def handlenewRoom(self,x,y):
        
        self.grid[x][y] = self.randomGeneratedRooms[self.data.counter_room_selection_cursor]
        newRoom = self.grid[x][y]
        print("q b4: ",self.rooms_data[newRoom.name]["q"])
        self.rooms_data[newRoom.name]["q"] +=-1 
        print("q ater: ",self.rooms_data[newRoom.name]["q"])
        items_room = self.rooms_data[newRoom.name]["items"]
        

    
            
        





    def update(self):
        self.updateDoors()

        self.generateRandomRooms()
        self.data.manor = self.grid

        self.current_room = self.grid[self.data.player.x][self.data.player.y]

        self.next_room = self.grid[self.data.player.next_room_position[0]][self.data.player.next_room_position[1]]
       
        self.data.player.next_room_status = self.checkRoomConnection()
