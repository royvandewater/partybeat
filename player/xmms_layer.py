import datetime
import time

from daemon.player_info import Player
from daemon.models import *

def song_sort(song):
    return song.position

class Xmms_layer:
    def __init__(self):
        self.xmms2 = XmmsStatus()

    def load_player_from_db(self):
        player = Player()
        loop = True
        while(loop):
            self.xmms2 = XmmsStatus.objects.get()
            # Retrieves playlist from database
            all_songs = sorted(Song.objects.all(), key=song_sort)
            # If the length of all songs is not equal to the number of songs in 
            # status, the daemon is probably still writing to the db, so we
            # wait 50 milliseconds
            loop = self.xmms2.playlist_size != len(all_songs)
            if loop:
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
        player.timeout = self.xmms2.timeout
        player.seek = self.xmms2.seek
        player.max_seek = self.xmms2.max_seek
        player.volume = self.xmms2.volume

        self.player = player

    def store_action(self, command):
        """
        Creates a new action and stores it in the db
        """
        command = command.lower()
        if command.startswith(("play", "stop", "pause", "next", "previous", "delete", "seek", "skip", "shuffle", "volume", "move")):
            action = Action()
            action.command = command
            action.save()
