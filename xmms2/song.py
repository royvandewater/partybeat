
class Song:
    def __init__(self, title="", artist="", album="", error="", position=0):
        self.title  = title
        self.artist = artist
        self.album  = album
        self.error  = error
        self.position = position

    def set_info(self, minfo, position=0):
        self.set_song(minfo)
        self.set_artist(minfo)
        self.set_album(minfo)
        self.set_position(position)

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

    def set_position(self, position)
        self.position = position
