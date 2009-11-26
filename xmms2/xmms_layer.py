import datetime
from xmms_controller import Xmms_controller
import models

class Xmms_layer:
    def __init__(self):
        xmmsStatus = XmmsStatus.objects.get()
        # If data is older than 2 seconds, refresh data
        time_diff = datetime.datetime.now() - xmmsStatus.last_update
        if(time_diff.seconds > 2):
            self.xmms2 = Xmms_controller()
            self.player = self.xmms2.player
        else:
            self.xmms2 = xmmsStatus
            load_player_from_db()


    def reload_data(self):
        self.xmms2 = Xmms_controller()
        self.player = xmms2.get_player_info()

    def load_player_from_db(self):
        player = Player()
        # Retrieves playlist from database
        all_songs = Song.objects.all()
        # Store the current song
        player.current_song = all_songs[0]
        # load the rest in the playlist
        player.playlist = all_songs[1:]

        player.status = self.xmms2.current_action

        this.player = player
