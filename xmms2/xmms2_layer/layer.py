#!/usr/bin/env python
import sys
import os
import xmmsclient

def main():
    pass

class Xmms_layer:
    def __init__(self):
        self.xmms = self.get_xmmsclient()
        pass

    def get_xmmsclient(self):
        xmms = xmmsclient.XMMS("xmms2")

        try:
            xmms.connect(os.getenv("XMMS_PATH"))
            return xmms
        except IOError, detail:
            return ("Connection failed: %s" % detail)

    def print_playback_error(self, result, action):
        if result.iserror():
            return("playback %s returned error, %s" % (action, result.get_error()))
        else:
            return("playback %s run" % (action)) 

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

    def next(self):
        result = self.xmms.playlist_set_next_rel(1)
        result.wait()
        result = self.xmms.playback_tickle()
        result.wait()
        return self.print_playback_error(result, "next")

    def previous(self):
        result = self.xmms.playlist_set_next_rel(-1)
        result.wait()
        result = self.xmms.playback_tickle()
        result.wait()
        return self.print_playback_error(result, "previous")

    def do_action(self, action):
        if action == "play":
            return self.play()
        elif action == "stop":
            return self.stop()
        elif action == "pause":
            return self.pause()
        elif action == "next":
            return self.next()
        elif action == "previous":
            return self.previous()


if __name__=="__main__":
    main(argv[1:])
