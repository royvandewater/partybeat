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
        if time_diff.seconds > 2 or force_refresh:
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
            cur_song = all_songs[0]
            player.current_song.title = cur_song.title 
            player.current_song.artist = cur_song.artist 
            player.current_song.album = cur_song.album 

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
        songs = Song.objects.all()
        for song in songs:
            song.delete()
        # Start with the current song
        song = Song()
        song.position = 0
        song.title = self.player.current_song.title
        song.artist = self.player.current_song.artist
        song.album = self.player.current_song.album
        song.save()

        # Now the other songs
        for song_item in self.player.playlist:
            song = Song()
            song.title = song_item.title
            song.artist = song_item.artist
            song.album = song_item.album
            song.error = song_item.error
            song.position = song_item.position
            song.save()
