import xmmsclient
import os

class Xmms_controller:
    def __init__(self):
        self.xmms = self.get_xmmsclient()

    def do_action(self, action):
        if action == "play":
            return self.play()
        elif action == "stop":
            return self.stop()
        elif action == "pause":
            return self.pause()

    def pause(self):
        result = self.xmms.playback_pause()
        result.wait()
        return self.print_playback_error(result, "pause")


    def play(self):
        result = self.xmms.playback_start()
        result.wait()
        return self.print_playback_error(result, "play")


    def stop(self):
        result = self.xmms.playback_stop()
        result.wait()
        return self.print_playback_error(result, "stop")


    def print_playback_error(self, result, action):
        if result.iserror():
            return("playback %s returned error, %s" % (action, result.get_error()))
        else:
            return("playback %s run" % (action)) 


    def get_xmmsclient(self):
        xmms = xmmsclient.XMMS("xmms2")

        try:
            xmms.connect(os.getenv("XMMS_PATH"))
            return xmms
        except IOError, detail:
            return ("Connection failed: %s" % detail)

    def get_player_status(self, player): 
        status = self.xmms.playback_status()
        status.wait()
        player.set_status(status.value())
        return player

    def get_player_info(self, player):
        result = self.xmms.playback_current_id()
        result.wait()

        
        if result.iserror():
            player.set_error("Playback current id returns error, %s" % result.get_error())
            return player

        id = result.value()
        if id == 0:
            player.set_error("Nothing is playing")
            return player

        result = self.xmms.medialib_get_info(id)
        result.wait()

        if result.iserror():
            player.set_error("medialib get info returns error, %s" % result.get_error())
            return player

        minfo = result.value()
        player.set_info(minfo)
        return player



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
