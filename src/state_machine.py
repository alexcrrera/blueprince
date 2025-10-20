from src import params

class StateMachineHandler():

    def __init__(self,data):
        self.data = data
        self.room_selection_mode = False
        self.cursor_selection_mode = True
        self.inventory_mode = False
        self.generate_random_rooms_flag = False

    
    def update(self):



        if(self.cursor_selection_mode):
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


            out[0] = min(out[0],params.ROOM_GRID_SIZE_HORIZONTAL-1)
            out[0] = max(0,out[0])

            out[1] = min(out[1],params.ROOM_GRID_SIZE_VERTICAL-1)
            out[1] = max(0,out[1])
           
            self.data.player.next_room_position = out
            
            if(self.data.space_pressed):
                self.data.state_machine.generate_random_rooms_flag = True

                self.data.player.x = self.data.player.next_room_position[0]
                self.data.player.y =self.data.player.next_room_position[1]
                
                self.data.player.inventory.steps_left += -1
                self.cursor_selection_mode = False
           
        elif(self.room_selection_mode):
            
            pass
