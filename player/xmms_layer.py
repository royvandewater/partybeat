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
        loop = True
        while loop:
            self.xmms2 = XmmsStatus.objects.get()
            player = Player()
            # Retrieves playlist from database
            all_songs = sorted(Song.objects.filter(active=True), key=song_sort)
            # If the length of all songs is not equal to the number of songs in 
            # status, the daemon is probably still writing to the db, so we
            # wait 50 milliseconds
            if len(all_songs) == self.xmms2.playlist_size:
                loop = False
            else:
                time.sleep(0.05)

        # Store the current song
        if(all_songs):
            player.set_status(4)
            player.current_song = all_songs[0]

        # load the rest in the playlist
        player.playlist = all_songs[1:]

        player.status = self.xmms2.current_action
        player.position = self.xmms2.current_position
        player.last_update = self.xmms2.last_update
        player.seek = self.xmms2.seek
        player.max_seek = self.xmms2.max_seek

        self.player = player

    def store_action(self, command):
        """
        Creates a new action and stores it in the db
        """
        command = command.lower()
        if command.startswith(("play", "stop", "pause", "next", "previous", "delete")):
            action = Action()
            action.command = command
            action.save()
