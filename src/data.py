


from src import params

from src import state_machine

class HandleData:
    
    def __init__(self,player):
        self.keep_running = True
        self.state_machine =  state_machine.StateMachineHandler(self)
        self.music_play = params.PLAY_MUSIC_START
        self.music_level = params.MUSIC_LEVEL
        self.update_tiles = True
        self.roomX = 2
        self.roomY = 8

        self.player = player

        self.click_play = False
        self.small_click_play = False
        self.toggle_up = False
        self.space_pressed = False
        self.cursor_visible = True

        self.manor = [[None for _ in range(params.ROOM_GRID_SIZE_VERTICAL)] for _ in range(params.ROOM_GRID_SIZE_HORIZONTAL)]

    def update(self):
        self.state_machine.update()