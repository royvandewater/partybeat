import datetime
from xmms2_django.daemon.player_info import Player
from xmms2_django.daemon.models import *

def song_sort(song):
    return song.position 

class Xmms_layer:
    def __init__(self):
        self.xmms2 = XmmsStatus.objects.get()
        self.load_player_from_db()


    def load_player_from_db(self):
        player = Player()
        # Retrieves playlist from database
        all_songs = sorted(Song.objects.all(), key=song_sort)
        # Store the current song
        if(all_songs):
            player.set_status(4)
            player.current_song = all_songs[0]

        # load the rest in the playlist
        player.playlist = all_songs[1:]

        player.status = self.xmms2.current_action

        self.player = player
