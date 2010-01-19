"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client

class SimpleTest(TestCase):
    fixtures = ['library.yaml']

    def check_response_code(self, url, code):
        """
        Check the url to ensure it returns the proper response code
        """
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, code)

    # Test all urls
    def test_library(self):
        self.check_response_code('/library/', 200)

    def test_add(self):
        self.check_response_code('/library/add/1/', 302)

    def test_artists(self):
        self.check_response_code('/library/artists/', 200)

    def test_albums(self):
        self.check_response_code('/library/albums/', 200)
        self.check_response_code('/library/albums/Phil_Collins/', 200)

    def test_songs(self):
        self.check_response_code('/library/songs/', 200)

    def test_edit(self):
        self.check_response_code('/library/edit/1/', 200)

    def test_upload(self):
        self.check_response_code('/library/upload/', 200)
