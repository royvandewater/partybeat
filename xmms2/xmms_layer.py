import datetime
from xmms_controller import Xmms_controller
from models import *

class Xmms_layer:
    def __init__(self):
        self.last_update = LastUpdate()
        # If data is older than 1 second, refresh data
        time_diff = datetime.datetime.now() - self.last_update
        if(time_diff.seconds > 2)
            self.xmms2 = Xmms_controller
        else
            self.xmms2 = None

        self.player = None

    def reload_data(self):
        self.xmms2 = Xmms_controller()
        self.player = xmms2.get_player_info()
