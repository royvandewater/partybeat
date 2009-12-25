"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from models import *

class SimpleTest(TestCase):
    def setUp(self):
        songFile = SongFile()
        songFile.file = None
        songFile.name = "In the Air Tonight"
        songFile.artist = "Phil Collins"
        songFile.album = "Hits..."
        songFile.supersave()

    def test_name(self):
        """
        Tests that a new songFile can be accessed by name
        """
        songFile = SongFile.objects.get(name="In the Air Tonight")
        self.assertEqual(songFile.artist, "Phil Collins")

    def test_artist(self):
        """
        Tests that a new songFile can be accessed by artist
        """
        songFile = SongFile.objects.get(artist="Phil Collins")
        self.assertEqual(songFile.album, "Hits...")

    def test_album(self):
        """
        Tests that a new songFile can be accessed by album
        """
        songFile = SongFile.objects.get(album="Hits...")
        self.assertEqual(songFile.artist, "Phil Collins")

    def test_unicode(self):
        """
        Tests that the output string is correct
        """
        songFile = SongFile.objects.get(name="In the Air Tonight")
        self.assertEqual(songFile.__unicode__(), u"Phil Collins - Hits... - In the Air Tonight")

    def test_print_list(self):
        """
        Tests that the print list funciton works right
        """
        list = ["a", "b", "c"]
        self.assertEqual(SongFile().print_list(list), "a - b - c")

