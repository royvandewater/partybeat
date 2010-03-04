import os
import sys

import xmmsclient.sync

from models import *
from player_info import Player

class Xmms_controller:
    def __init__(self):
        self.xmms = self.get_xmmsclient()
        self.player = Player()

    def do_action(self, action, action_text, amount=None):
        """
        action is expected to be a xmms action function
        # ex: do_action(self.xmms.playback_stop, "stop")
        """
        try:
            if amount:
                action(amount)
            else:
                action()
            return self.print_playback_error(action_text)
        except xmmsclient.sync.XMMSError as e:
            return self.print_playback_error(action_text, e.message)


    def print_playback_error(self, action, error=None):
        if error:
            return("action '{0}' returned error: '{1}'".format(action, error))
        else:
            return("action '{0}' executed".format(action)) 

    def tickle(self, amount):
        """ Amount = 1 for next, -1 for previous """
        self.xmms.playlist_set_next_rel(amount)
        self.xmms.playback_tickle()


    def action(self, action):
        if action == "play":
            return self.do_action(self.xmms.playback_start, "play")
        elif action == "stop":
            return self.do_action(self.xmms.playback_stop, "stop")
        elif action == "pause":
            return self.do_action(self.xmms.playback_pause, "pause")
        elif action == "next":
            return self.do_action(self.tickle, "next", 1)
        elif action == "previous":
            return self.do_action(self.tickle, "previous", -1)
        elif action == "shuffle":
            return self.do_action(self.xmms.playlist_shuffle, "shuffle")

    def enqueue(self, filepath):
        filepath = "file://" + filepath
        error = self.xmms.playlist_add_url(filepath)

    def delete(self, id):
        error = self.xmms.playlist_remove_entry(id)
        if error:
            return self.print_playback_error("delete_{0}".format(id), error)
        else:
            return self.print_playback_error("delete_{0}".format(id))

    def seek(self, seek_time):
        try:
            self.xmms.playback_seek_ms(seek_time)
            return self.print_playback_error("seek")
        except xmmsclient.sync.XMMSError as e:
            return self.print_playback_error("seek", e.message)

    def skip_to(self, id):
        try:
            self.xmms.playlist_set_next(int(id)-1)
            self.xmms.playback_tickle()
            return self.print_playback_error("skip")
        except xmmsclient.sync.XMMSError as e:
            return self.print_playback_error("skip", e.message)

    def get_song_from_minfo(self, minfo):
            song = Song()
            if minfo == "Could not retrieve info for that entry!":
                song.position = 0
                song.name = "Unknown"
                song.artist = "Unknown"
                song.album = "Unknown"
                song.xmms_id = -1
                return song
            try:
                song.name = minfo["title"]
            except KeyError:
                song.name = "Unknown"

            if song.name == "Unknown":
                try:
                    song.name = minfo["url"].rpartition("/")[2]
                except KeyError:
                    print("Caught")
                    song.name = "Unknown"

            try:
                song.artist = minfo["artist"]
            except KeyError:
                song.artist = "unknown"
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
        xmms = xmmsclient.sync.XMMSSync("xmms2_django_daemon")

        try:
            xmms.connect(os.getenv("XMMS_PATH"))
            return xmms
        except IOError, detail:
            return ("Connection failed: %s" % detail)

    def get_player_status(self): 
        status = self.xmms.playback_status()
        self.player.set_status(status)
        return self.player

    def get_player_info(self):
        try:
            current_id = self.xmms.playback_current_id()
            position = self.xmms.playlist_current_pos()
        except xmmsclient.sync.XMMSError as e: 
            self.player.set_error("Playback current id returns error, %s" % e.message)
            return self.player


        if current_id == 0:
            self.player.set_error("Nothing is playing")
            return self.player

        minfo = self.get_song_info_from_id(current_id)
        self.player.current_song = self.get_song_from_minfo(minfo)
        try: 
            self.player.position = position['position'] + 1 
        except:
            self.player.position = 0
        self.player.seek = self.xmms.playback_playtime()
        self.player.max_seek = minfo["duration"]
        del(minfo)
        self.get_player_status()
        self.build_playlist()
        return self.player

    def get_song_info_from_id(self, id):
        try:
            return self.xmms.medialib_get_info(id)

        except xmmsclient.sync.XMMSError as e:
            self.player.set_error("medialib get info returns error, {0}".format(e.message))
            return None

    def build_playlist(self):
        self.player.clear_playlist()
        song_ids = self.xmms.playlist_list_entries()
        position_in_playlist = self.player.current_song.position

        for song_id in song_ids:
            minfo = self.get_song_info_from_id(song_id)
            song = self.get_song_from_minfo(minfo)
            self.player.add_to_playlist(song)

    def clear_player(self):
        """ Re inits the player object """
        # del(self.player)
        # self.player = Player()
