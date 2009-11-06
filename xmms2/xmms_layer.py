import datetime
from xmms_controller import Xmms_controller
import models

class Xmms_layer:
    def __init__(self):
        self.xmms_status = XmmsStatus.objects.
        # self.last_update = XmmsStatus.get
        # If data is older than 2 seconds, refresh data
        time_diff = datetime.datetime.now() - self.last_update
        if(time_diff.seconds > 2):
            self.xmms2 = Xmms_controller()
        else:
            self.xmms2 = load_from_db()

        self.player = None

    def reload_data(self):
        self.xmms2 = Xmms_controller()
        self.player = xmms2.get_player_info()

    def load_from_db(self):
        

