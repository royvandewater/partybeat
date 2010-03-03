import os
import sys
import hashlib

from models import *

class Player():
    """
    This class is part of the xmms_controller interface. It's purpose is to abstract the information
    from xmms_controller (Such as current song information, player status, playlist info) from the
    player controls (Such as play, pause, stop, etc). This provides a safer mechanism for the Django
    Template class to get access information from the xmms2 player
    """
    def __init__(self):
        self.playlist = []
        self.current_song = Song()
        self.status = ""
        self.error = ""
        self.position = None

    def set_status(self, status):
        self.status = status

    def is_playing(self):
        return True if self.status == 1 else False

    def add_to_playlist(self, song):
        if isinstance(song, Song):
            self.playlist.append(song)
        else:
            return "Item was not a song and could not be added to playlist"

    def set_error(self, error):
        self.error = error

    def verbose_action(self):
        if self.status == 0:
            return "Stopped"
        elif self.status == 1:
            return "Playing"
        elif self.status == 2:
            return "Paused"
        else:
            return "Unknown"

    def clear_playlist(self):
        """ resets the current playlist """
        self.playlist = []

    def playlist_size(self):
        """ Returns the size of the playlist plus the currently playing item """
        return len(self.playlist) + 1

    def get_hash(self):
        hashable = "".join(str(song.xmms_id) for song in self.playlist) + str(self.position)
        return hashlib.md5(hashable).hexdigest()
