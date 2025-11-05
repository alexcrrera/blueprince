from src import params
from src import handler
class StateMachineHandler(handler.BaseHandler):

    def __init__(self,data):
        super().__init__(data)
    
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




    def cursorSpacePressed(self):
        self.data.space_pressed = False
        if(self.data.player.next_room_status ==-1): #VIDE
           
            self.data.state_machine.generate_random_rooms_flag = True
            self.data.gridHandler.generateRandomRooms()
            self.mode = 1 
       

        elif(self.data.player.next_room_status ==1): # OUVERT
            self.data.enter_room_play = True
      
            self.mode = 0
            self.data.player.next_room_status =0
            self.data.player.x = self.data.player.next_room_position[0]
            self.data.player.y =self.data.player.next_room_position[1]
            self.nextRoomCursor()
            self.data.gridHandler.updateRoomAndNextRoom()

            self.data.player.inventory.removeItems("steps_left",1,self.data)
            self.data.counter_inventory = 0

            
           # self.data.gridHandler.update()
                    
        elif(self.data.player.next_room_status ==2): 

                if(self.data.player.inventory.getItemQ("keys")>0):
                    if(not self.data.player.inventory.getItemQ("lockpick")>0):
                        self.data.player.inventory.removeItems("keys",1,self.data)
                        
                    self.data.door_locked_play = True
                    self.data.gridHandler.openDoor()
        
        elif(self.data.player.next_room_status ==3): 

                if(self.data.player.inventory.getItemQ("keys")>0):
                        self.data.player.inventory.removeItems("keys",1,self.data)
                       
                        self.data.door_locked_play = True
                        self.data.gridHandler.openDoor()
            
           
    def handleRedraft(self):
        self.data.room_redraft_play = True
        self.data.redraft_pressed = False
        self.data.player.inventory.removeItems("dice",1,self.data,keep_item=True)
        self.data.state_machine.generate_random_rooms_flag = True
        self.data.gridHandler.generateRandomRooms() 

    
    def handleRoomSelectedWithEnter(self):
        self.data.enter_pressed = False
        room = self.data.gridHandler.randomGeneratedRooms[self.data.counter_room_selection_cursor]
        cost = room.cost
        if(self.data.player.inventory.getItemQ("gems")-cost<0):
            return
        self.data.player.inventory.removeItems("gems",cost,self.data,keep_item=True)

        x = self.data.player.next_room_position[0]
        y = self.data.player.next_room_position[1]

        self.data.gridHandler.handlenewRoom(x,y)

        self.room_selection_mode = False
        self.cursor_selection_mode = True
        self.mode = 0




    def handleInteraction(self):
        if(not self.data.interact_pressed):
            return

        #self.data.interact_play = True
        self.data.interact_pressed =  False
        current_room = self.data.gridHandler.current_room
        count_items = len(current_room.inventory.items) + len(current_room.inventory.actions)

        if(count_items==0):
            return

        cursor_pos = self.data.counter_inventory


        if(cursor_pos > len(current_room.inventory.actions)-1):
            cursor_pos_rel = cursor_pos - len(current_room.inventory.actions)
            self.interactWithItem(current_room,cursor_pos_rel)
        else:

            self.interactWithAction(current_room,cursor_pos)
            

    def interactWithItem(self,current_room,cursor_pos):
        ind = 0
        items_dict = current_room.inventory.items.copy()
        for key,val in items_dict.items():
            print(ind,cursor_pos)
            if ind == cursor_pos:
                self.data.player.inventory.addItem(key,val)
                current_room.inventory.removeItems(key,val,self.data)
                return
            ind+=1

    def interactWithAction(self,current_room,cursor_pos):
        ind = 0
        actions_dict = current_room.inventory.actions.copy()
        for action,val in actions_dict.items():
            print(ind,cursor_pos)

            if ind == cursor_pos:
                reply = self.data.gridHandler.checkIsInteractionPossible(action)
                if(reply=="ok"):
                    
                    self.data.gridHandler.doAction(action)
                    current_room.inventory.removeActions(action,1)
                else:
                    self.data.updateDebugText(reply)
                return
            ind+=1
            


    def update(self):

        if(self.mode ==0): # cursor mode
            self.nextRoomCursor() # place le curseur tel que la prochaine chambre est choisie

            if(self.data.space_pressed):
                self.cursorSpacePressed()
            else:
                self.handleInteraction()
                
        elif(self.mode==1): # mode selection chambre
            # 
            if(self.data.redraft_pressed ):
                  self.handleRedraft()
                
            elif(self.data.enter_pressed):
                self.handleRoomSelectedWithEnter()
                

        elif(self.mode ==2):
            pass

            pass




