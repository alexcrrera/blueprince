


from src import params
from src import room_library
from src import state_machine
from src import handler

class HandleData(handler.BaseHandler):
    
    def __init__(self,clock):
        super().__init__()
        
        self.keep_running = True
        self.player = None
        self.clock = clock


    def secondaryInit(self):
        self.state_machine =  state_machine.StateMachineHandler(self)
        self.gridHandler = room_library.RoomGrid(self)

        self.music_play = params.PLAY_MUSIC_START
        self.music_level = params.MUSIC_LEVEL
        self.update_tiles = True
       

       

        self.click_play = False
        self.small_click_play = False
        self.toggle_up = False
        self.space_pressed = False
 
        self.cursor_visible = True

        self.counter_room_selection_cursor =0
        self.enter_pressed = False
        self.enter_room_play = False

        

        self.redraft_pressed = False
        self.door_locked_play = False
        self.game_over = [False,-1,0]
        self.interact_pressed = False
        self.interact_play = False
        self.counter_inventory = 0

        self.debug_text = ""
        self.history_text = "You enter a manor"
        self.room_redraft_play = False
        self.shovel_play = False


        self.mail_play = False


        self.dark_room_effect = False
        self.trunk_play = False
        self.hammer_play = False
        self.locker_play = False


        self.veranda_effect = True
        self.maid_chamber_effect = False

        self.green_house_effect = False
        self.furnace_effect = True


    def addPlayer(self,player):
        self.player = player

    
    def cleanNameRemoveS(self,name):
        if name.endswith("s"):
            return name[:-1]
        return name
    

    def updateDebugText(self,txt):
        self.history_text =txt
    
    def updateHistory(self,what,q,verb=None):
        if verb  is None:
            verb = "use"
   
            

        descript_dict = params.ITEMS_DESCRIPTION_DICT.get(what)
        
        if q == 0:
            return
        
        

        txt  = "You " + verb + " "
        thing = self.cleanNameRemoveS(descript_dict[0])

        if q == 1:

            
            if descript_dict[2] == "t":
                
                txt += "one "
                txt +=thing.lower()
            else:
                txt += " the "
                txt +=thing
        else:
            txt+= str(q) + " x"  + " "
            txt +=thing.lower()
            
        
        
        
        is_s = "s" if q > 1 else ""
        txt +=is_s
        self.history_text =txt

    def update(self):
        if(self.player.inventory.getItemQ("steps_left")==0):
            self.game_over = [True,1]
            self.state_machine.mode = -1
        
        if(self.player.x==2 and self.player.y ==0):
            self.game_over = [True,2]
            self.state_machine.mode = -1
       
        
        self.state_machine.update()
        self.gridHandler.update()