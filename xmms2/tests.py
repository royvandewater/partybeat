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

    # Testing Song class functionality

    def testSong_init(self):
        song = Song(artist="test")
        self.assertEqual(song.title, "")
        self.assertEqual(song.artist, "test")

    def testSong_setters(self):


        def testSong_set_title(song, minfo):
            song.set_title(minfo)
            self.assertEqual(song.title, minfo['title'])
            song.set_title({})
            self.assertEqual(song.title, 'unknown')

        def testSong_set_artist(song, minfo):
            song.set_artist(minfo)
            self.assertEqual(song.artist, minfo['artist'])
            song.set_artist({})
            self.assertEqual(song.artist, 'unknown')

        def testSong_set_album(song, minfo):
            song.set_album(minfo)
            self.assertEqual(song.album, minfo['album'])
            song.set_album({})
            self.assertEqual(song.album, 'unknown')

        def testSong_set_error(song, error):
            song.set_error(error)
            self.assertEqual(song.error, error)

        def testSong_set_position(song, position):
            song.set_position(position)
            self.assertEqual(song.position, position)

        song = Song()
        minfo = {'title':'test', 'artist':'test', 'album':'test'}
        testSong_set_title(song, minfo)
        testSong_set_artist(song, minfo)
        testSong_set_album(song, minfo)
        testSong_set_error(song, "test")
        testSong_set_position(song, 0)

    def testSong_set_info(self):
        minfo = {'title':'test', 'artist':'test'}
        self.song.set_info(minfo)
        self.assertEqual(self.song.title, 'test')
        self.assertEqual(self.song.album, 'unknown')


    # Testing Player class functionality

    def testPlayer_init(self):
        player = Player()
        self.assertEqual(player.playlist, [])
        self.assert_(isinstance(player.current_song, Song))
        self.assertEqual(player.status, "")

    def testPlayer_set_status(self):
        player = self.player
        player.set_status(1)
        self.assertEqual(player.status, "Playing")

    def testPlayer_is_playing(self):
        player = self.player
        player.set_status(1)
        self.assert_(player.is_playing())

    def testPlayer_add_to_playlist(self):
        if not self.player.add_to_playlist(self.song) is None:
            self.fail()
        self.assertEqual(len(self.player.playlist), 1)

    # Testing Xmms_controller

    def testXmms_init(self):
        xc = Xmms_controller()
        self.assert_(isinstance(xc.xmms, xmmsclient.XMMS))
        self.assert_(isinstance(xc.player, Player))

    def testXmms_Connection(self):
        self.assert_(isinstance(self.xmms_controller.xmms, xmmsclient.XMMS))

    def testXmms_Actions(self):
        self.assertEqual(self.xmms_controller.do_action("play"), "playback play run")
        self.assertEqual(self.xmms_controller.do_action("pause"), "playback pause run")

    def testXmms_get_player_status(self):
        self.xmms_controller.do_action("pause")
        player = self.xmms_controller.get_player_status()
        self.assertEqual(player.status, 'Paused')

    def testXmms_get_player_status(self):
        self.xmms_controller.build_playlist()
