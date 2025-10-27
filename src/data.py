


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
        self.roomX = 2
        self.roomY = 8

       

        self.click_play = False
        self.small_click_play = False
        self.toggle_up = False
        self.space_pressed = False
        self.cursor_visible = True

        self.counter_room_selection_cursor =0
        self.enter_pressed = False

        self.clock = clock

        self.game_over = [False,-1]
    
       
        self.manor = [[None for _ in range(params.ROOM_GRID_SIZE_VERTICAL)] for _ in range(params.ROOM_GRID_SIZE_HORIZONTAL)]

    def update(self):
        if(self.player.inventory.steps_left==0):
            self.game_over = [True,1]
       
        
        self.state_machine.update()
        self.gridHandler.update()