# This class is part of the xmms_controller interface. It's purpose is to abstract the information
# from xmms_controller (Such as current song information, player status, playlist info) from the 
# player controls (Such as play, pause, stop, etc). This provides a safer mechanism for the Django
# Template class to get access information from the xmms2 player

class Player:
    def __init__(self):
        self.song   = ""
        self.artist = ""
        self.album  = ""
        self.error  = ""
        self.status = ""
        self.statusid = ""
    
    def set_info(self, minfo):
        self.set_song(minfo)
        self.set_artist(minfo)
        self.set_album(minfo)

    def set_error(self, error):
        self.error = error

    def set_song(self, minfo):
        try:
            self.song = minfo["title"]
        except KeyError:
            self.song = "unknown"

    def set_artist(self, minfo):
        try:
            self.artist = minfo["artist"]
        except KeyError:
            self.artist = "unknown"

    def set_album(self, minfo):
        try:
            self.album = minfo["album"]
        except KeyError:
            self.album = "unknown"

    def set_status(self, statusid):
        status_types = ("Stop", "Play", "Pause")
        self.status = status_types[statusid]
        self.statusid = statusid

    def is_playing(self):
        return True if self.statusid == 1 else False
