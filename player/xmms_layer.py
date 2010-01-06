import datetime
import time

from xmms2_django.daemon.player_info import Player
from xmms2_django.daemon.models import *

def song_sort(song):
    return song.position 

class Xmms_layer:
    def __init__(self):
        self.xmms2 = XmmsStatus()

    def load_player_from_db(self):
        self.xmms2 = XmmsStatus.objects.get()
        player = Player()
        # Retrieves playlist from database
        all_songs = sorted(Song.objects.filter(active=True), key=song_sort)
        # If the length of all songs is not equal to the number of songs in 
        # status, the daemon is probably still writing to the db, so we
        # wait 50 milliseconds
        limit = 0
        if len(all_songs) != self.xmms2.playlist_size and limit < 3:
            time.sleep(0.05)
            limit += 1

        # Store the current song
        if(all_songs):
            player.set_status(4)
            player.current_song = all_songs[0]

        # load the rest in the playlist
        player.playlist = all_songs[1:]

        player.status = self.xmms2.current_action

        self.player = player

    def store_action(self, command):
        """
        Creates a new action and stores it in the db
        """
        print("store_action called with command: '{0}'".format(command))
        if command.lower() in ("play", "stop", "pause", "next", "previous"):
            action = Action()
            action.command = command
            action.save()
