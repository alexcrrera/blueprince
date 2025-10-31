from src import params
from src import handler
class StateMachineHandler(handler.BaseHandler):

    def __init__(self,data):
        super().__init__(data)
        self.room_selection_mode = False
        self.cursor_selection_mode = True
        self.inventory_mode = False
        self.generate_random_rooms_flag = False

        self.mode = 0 # 0 cursor selection, 1 random room generation

    def nextRoomCursor(self):
        direction = self.data.player.direction
        dx,dy = 0,0

        if(direction==0):
            dx = 1
        elif(direction==1):
            dy = -1
        elif(direction==2):
            dx = -1
        elif(direction==3):
            dy = +1

        out =[self.data.player.x+dx,self.data.player.y+dy]

        x,y = out[0],out[1]
        if(x<0): # côté gauche
            out[0] = out[0]+2
            self.data.player.direction = 0
            
        if(x>params.ROOM_GRID_SIZE_HORIZONTAL-1):
            out[0] = out[0]-2
            self.data.player.direction = 2

        if(y<0):
            out[1] += 2
            self.data.player.direction =3


        if(y>params.ROOM_GRID_SIZE_VERTICAL-1):
            out[1] +=-2
            self.data.player.direction =1


        out[0] = min(out[0],params.ROOM_GRID_SIZE_HORIZONTAL-1)
        out[0] = max(0,out[0])

        out[1] = min(out[1],params.ROOM_GRID_SIZE_VERTICAL-1)
        out[1] = max(0,out[1])
        
        self.data.player.next_room_position = out

        self.data.gridHandler.update() #mettre a jour 

    def cursorHandler(self):
        if( self.data.player.next_room_status ==-1): #VIDE
            self.data.state_machine.generate_random_rooms_flag = True
            self.data.gridHandler.generateRandomRooms()
            self.mode = 1 
       

        elif(self.data.player.next_room_status ==1): # OUVERT
            self.mode = 0
            self.data.player.next_room_status =0
            self.data.player.x = self.data.player.next_room_position[0]
            self.data.player.y =self.data.player.next_room_position[1]
            self.data.player.inventory.steps_left += -1
                    
        elif(self.data.player.next_room_status ==2 or self.data.player.next_room_status ==3): 
            if(self.data.player.inventory.keys>0):
                self.data.player.inventory.keys += -1
                print("Used one key")
                self.data.door_locked_play = True
                self.data.gridHandler.openDoor()
            
           





    def update(self):

        if(self.mode ==0): # cursor mode
            self.nextRoomCursor() # place le curseur tel que la prochaine chambre est choisie

            if(self.data.space_pressed):
                self.data.space_pressed = False
                self.cursorHandler()
                
        elif(self.mode==1): # mode selection chambre

            if(self.data.redraft_pressed ):
                self.data.redraft_pressed = False
                self.data.player.inventory.dice +=-1
                self.data.state_machine.generate_random_rooms_flag = True
                self.data.gridHandler.generateRandomRooms()   
                print("tf")

            elif(self.data.enter_pressed):
                self.data.enter_pressed = False
                room = self.data.gridHandler.randomGeneratedRooms[self.data.counter_room_selection_cursor]
                cost = room.cost
                if(self.data.player.inventory.gems-cost<0):
                    return
                self.data.player.inventory.gems+=-cost

                x = self.data.player.next_room_position[0]
                y = self.data.player.next_room_position[1]

                self.data.gridHandler.handlenewRoom(x,y)

                self.room_selection_mode = False
                self.cursor_selection_mode = True
                self.mode = 0

        elif(self.mode ==2):
            pass

            pass




