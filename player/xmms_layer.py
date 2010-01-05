import datetime
from xmms_controller import Xmms_controller
from player_info import Player
from models import *

def song_sort(song):
    return song.position 

class Xmms_layer:
    def __init__(self, force_refresh=False):
        xmmsStatus = XmmsStatus.objects.get()
        # If data is older than 2 seconds, refresh data
        time_diff = datetime.datetime.now() - xmmsStatus.last_update
        self.timer = time_diff.seconds
        milliseconds = (time_diff.seconds * 1000) + (time_diff.microseconds / 1000)
        if milliseconds > xmmsStatus.timeout or force_refresh:
            print(milliseconds)
            self.xmms2 = Xmms_controller()
            self.xmms2.get_xmmsclient()
            self.player = self.xmms2.get_player_info()
            # save it in the database as well
            self.save_in_db(xmmsStatus, self.player)
        else:
            self.xmms2 = xmmsStatus
            self.load_player_from_db()


    def reload_data(self):
        self.xmms2 = Xmms_controller()
        self.player = xmms2.get_player_info()


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

    def save_in_db(self, xmms2Status, player):
        # We need to convert the xmms_controller object to an xmms2 status object for saving
        xmms2Status.current_action = player.status
        xmms2Status.last_update = datetime.datetime.now()
        xmms2Status.save()
        # We also need to save all the player's songs
        # First clear out the old songs
        Song.objects.all().delete()
        # Start with the current song
        song = Song()
        song = self.player.current_song
        song.position = 0
        song.save()

        # Now the other songs
        for song in self.player.playlist:
            song.save()
