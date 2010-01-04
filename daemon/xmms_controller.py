from django.core.management import setup_environ

import os
import sys

import xmmsclient.sync
from player_info import Player

# Needs to be relative to current dir
sys.path.append('/home/doppler/Projects/git/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'xmms2_django.settings'
from xmms2_django.xmms2.models import *

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
            return("playback %s returned error, %s" % (action, error))
        else:
            return("playback %s run" % (action)) 

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
            return self.do_action(self.tickle, "next", -1)

    def get_song_from_minfo(self, minfo):
            song = Song()

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
        self.player.set_status(status.value())
        return self.player

    def get_player_info(self):
        current_id = self.xmms.playback_current_id()
        
        if current_id:
            self.player.set_error("Playback current id returns error, %s" % result.get_error())
            return self.player

        id = result

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

        if result.iserror():
            self.player.set_error("medialib get info returns error, %s" % result.get_error())
            return None

        return result.value()


    def build_playlist(self):
        song_ids = self.xmms.playlist_list_entries()
        # song_ids = playlist_ids.value()
        position_in_playlist = self.player.current_song.position

        for song_id in song_ids:
            minfo = self.get_song_info_from_id(song_id)
            song = self.get_song_from_minfo(minfo)
            self.player.add_to_playlist(song)

    def delete(self, xmms_id):
        # Delete item from playlist 
        result = self.xmms.medialib_remove_entry(int(xmms_id))
        result.wait()
        return self.print_playback_error(result, "delete")
