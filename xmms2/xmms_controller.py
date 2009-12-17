import os
import xmmsclient
from player_info import Player
from models import Song

class Xmms_controller:
    def __init__(self):
        self.xmms = self.get_xmmsclient()
        self.player = Player()

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
        result2 = self.xmms.playback_tickle()
        result2.wait()
        return self.print_playback_error(result2, "next")

    def previous(self):
        result = self.xmms.playlist_set_next_rel(-1)
        result.wait()
        result2 = self.xmms.playback_tickle()
        result2.wait()
        return self.print_playback_error(result2, "previous")

    def print_playback_error(self, result, action):
        if result.iserror():
            return("playback %s returned error, %s" % (action, result.get_error()))
        else:
            return("playback %s run" % (action)) 

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

    def get_song_from_minfo(self, minfo):
            # print(minfo) # uncomment to get detailed info on xmms return object printed to console
            song = Song()
            # song.set_info(minfo, position=len(self.player.playlist))
            # song.set_position(song.position + 1)

            try:
                song.title = minfo["title"]
            except KeyError:
                song.title = "Unknown"
            try:
                self.artist = minfo["artist"]
            except KeyError:
                self.artist = "unknown"
            try:
                song.album = minfo["album"]
            except KeyError:
                song.album = "Unknown"

            try:
                song.xmms_id = minfo["id"]
            except KeyError:
                song.xmms_id = -1

            song.position = len(self.player.playlist) + 1
            return song

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

        minfo = self.get_song_info_from_id(id)
        self.player.current_song = self.get_song_from_minfo(minfo)
        self.get_player_status()
        self.build_playlist()
        return self.player

    def get_song_info_from_id(self, id):
        result = self.xmms.medialib_get_info(id)
        result.wait()

        if result.iserror():
            self.player.set_error("medialib get info returns error, %s" % result.get_error())
            return None

        return result.value()


    def build_playlist(self):
        playlist_ids = self.xmms.playlist_list_entries()
        playlist_ids.wait()
        song_ids = playlist_ids.value()
        # song_ids = playlist_ids.value()
        position_in_playlist = self.player.current_song.position

        for song_id in song_ids:
            minfo = self.get_song_info_from_id(song_id)
            song = self.get_song_from_minfo(minfo)
            self.player.add_to_playlist(song)
