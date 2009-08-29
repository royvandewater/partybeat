# This class is part of the xmms_controller interface. It's purpose is to abstract the information
# from xmms_controller (Such as current song information, player status, playlist info) from the 
# player controls (Such as play, pause, stop, etc). This provides a safer mechanism for the Django
# Template class to get access information from the xmms2 player

from song import Song

class Player(Song):
    def __init__(self):
        self.playlist = []
        self.current_song = Song()
        self.status = ""
        self.statusid = ""
    
    def set_status(self, statusid):
        status_types = ("Stopped", "Playing", "Paused")
        self.status = status_types[statusid]
        self.statusid = statusid

    def is_playing(self):
        return True if self.statusid == 1 else False

    def add_to_playlist(self, song):
        if isinstance(song, Song):
            self.playlist.append(song)
        else:
            return "Item was not a song and could not be added to playlist"
