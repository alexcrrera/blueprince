


from src import params
from src import room_library
from src import state_machine
from src import handler

class HandleData(handler.BaseHandler):
    
    def __init__(self,player,clock):
        super().__init__()
        
        self.keep_running = True
        self.player = player
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

        self.clock = clock

        self.redraft_pressed = False
        self.door_locked_play = False
        self.game_over = [False,-1,0]
        self.interact_pressed = False

        self.counter_inventory = 0

        self.debug_text = ""
    
       

    def update(self):
        if(self.player.inventory.steps_left==0):
            self.game_over = [True,1]
            self.state_machine.mode = -1
        
        if(self.player.x==2 and self.player.y ==0):
            self.game_over = [True,2]
            self.state_machine.mode = -1
       
        
        self.state_machine.update()
        self.gridHandler.update()