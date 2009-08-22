import xmmsclient
import os
from player_info import Player

class Xmms_controller:
    def __init__(self):
        self.xmms = self.get_xmmsclient()
        self.player = Player()

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

    def get_player_status(self): 
        status = self.xmms.playback_status()
        status.wait()
        self.player.set_status(status.value())
        return self.player

    def get_player_info(self):
        result = self.xmms.playback_current_id()
        result.wait()

        
        if result.iserror():
            self.player.set_error("Playback current id returns error, %s" % result.get_error())
            return self.player

        id = result.value()

        if id == 0:
            self.player.set_error("Nothing is playing")
            return self.player

        result = self.xmms.medialib_get_info(id)
        result.wait()

        if result.iserror():
            self.player.set_error("medialib get info returns error, %s" % result.get_error())
            return self.player

        minfo = result.value()
        self.player.set_info(minfo)
        self.get_player_status()
        return self.player
