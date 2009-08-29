
class Song:
    def __init__(self, title="", artist="", album="", error="", position=0):
        self.title  = title
        self.artist = artist
        self.album  = album
        self.error  = error
        self.position = position

    def __str__(self):
        return ("{0}: {1}".format(self.position, self.title))

    def set_title(self, minfo):
        try:
            self.title = minfo["title"]
        except KeyError:
            self.title = "unknown"

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

    def set_error(self, error):
        self.error = error

    def set_position(self, position):
        self.position = position

    def set_info(self, minfo, position=0):
        self.set_title(minfo)
        self.set_artist(minfo)
        self.set_album(minfo)
        self.set_position(position)
