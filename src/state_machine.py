
class StateMachineHandler():

    def __init__(self,data):
        self.data = data
        self.room_selection_mode = False
        self.cursor_selection_mode = True
        self.inventory_mode = False

    
    def update(self):

        if(self.cursor_selection_mode):
         
            if(self.data.space_pressed):
                direction = self.data.player.direction
                
                
                dx,dy = 0,0
                if(direction==0):
                    dx = 1
                elif(direction==1):
                    dy = -1
                elif(direction==2):
                    dx = +1
                elif(direction==3):
                    dy = -1
                self.data.player.x += dx
                self.data.player.y += dy
                self.data.player.y = min(8, self.data.player.y)
                
                self.data.player.inventory.steps_left += -1
                print(self.data.player.x,self.data.player.y)
                self.cursor_selection_mode = False
                self.room_selection_mode = True