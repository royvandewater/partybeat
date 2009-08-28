import time
import unittest
import xmmsclient
from xmms2.xmms_controller import Xmms_controller
from xmms2.player_info import Player
from xmms2.song import Song

class XmmsControllerActive(unittest.TestCase):
    def setUp(self):
        self.xmms_controller = Xmms_controller()
        self.player = Player()
        self.song = Song(
                title="Title",
                artist="Artist",
                album="Album",
                error="Error",
                position=1)
        time.sleep(0.5)

    # Testing Song class functionality

    def testSong_init(self):
        song = Song(artist="test")
        self.assertEqual(song.title, "")
        self.assertEqual(song.artist, "test")

    def testSong_set_info(self):
        minfo = ["title"=>1]
                


    # Testing Player class functionality

    def testPlayer_init(self):
        player = Player()
        self.assertEqual(player.playlist, [])
        self.assert_(isinstance(player.current_song, Song))
        self.assertEqual(player.status, "")
        self.assertEqual(player.statusid, "")

    def testPlayer_set_status(self):
        player = self.player
        player.set_status(1)
        self.assertEqual(player.status, "Playing")
        self.assertEqual(player.statusid, 1)

    def testPlayer_is_playing(self):
        player = self.player
        player.set_status(1)
        self.assert_(player.is_playing())

    def testPlayer_add_to_playlist(self):
        pass

    # Testing Xmms_controller

    def testConnection(self):
        self.assert_(isinstance(self.xmms_controller.xmms, xmmsclient.XMMS))
        time.sleep(0.5)

    def testActions(self):
        self.assertEqual(self.xmms_controller.do_action("play"), "playback play run")
        self.assertEqual(self.xmms_controller.do_action("pause"), "playback pause run")

    def testXmmsPlayerStatus(self):
        player = self.xmms_controller.get_player_status()
        self.assertEqual(player.status, 'Paused')

    def testXmmsPlayerIsPlaying(self):
        player = self.xmms_controller.get_player_status()
        self.assertEqual(player.is_playing(), False)
