#!/usr/bin/env python
import sys
import time
import unittest
import xmmsclient
from daemon import Xmms_daemon

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.xlayer = Xmms_layer()

    def testLayer_init(self):
        xlayer = Xmms_layer()
        self.assertTrue(isinstance(xlayer.xmms,xmmsclient.XMMS))

    def testLayer_print_playback_error(self):
        class Result:
            def __init__(self, value=False):
                self.value = value
            def iserror(self):
                return self.value
            def get_error(self):
                return "fail"

        self.assertEqual(self.xlayer.print_playback_error(Result(), "play"), "playback play run")
        self.assertEqual(self.xlayer.print_playback_error(Result(True), "play"), "playback play returned error, fail")

    def testLayer_pause(self):
        self.assertEqual(self.xlayer.pause(), "playback pause run")

    def testLayer_play(self):
        self.assertEqual(self.xlayer.play(), "playback play run")

    def testLayer_stop(self):
        self.assertEqual(self.xlayer.stop(), "playback stop run")

    def testLayer_next(self):
        self.assertEqual(self.xlayer.next(), "playback next run")

    def testLayer_previous(self):
        self.assertEqual(self.xlayer.previous(), "playback previous run")

    def testLayer_do_action(self):
        actions = ["play","stop","pause","next","previous"]
        for action in actions:
            self.assertEqual(self.xlayer.do_action(action), "playback {0} run".format(action))
            time.sleep(0.2)

    # def testLayer_get_player_status(self):
        # test

if __name__=="__main__":
    unittest.main()
