"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase


class SimpleTest(TestCase):
    fixtures = ['daemon.yaml']


    def check_response_code(self, url, code):
        """
        Check the url to ensure it returns the proper response code
        """
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, code)

    # These tests check all urls in the urls.py file
    def test_info(self):
        self.check_response_code('/player/info/', 200)

    def test_playlist(self):
        self.check_response_code('/player/playlist/', 200)

    def test_player(self):
        self.check_response_code('/player/', 200)

    def test_action(self):
        self.check_response_code('/player/action/play/', 302)

    def test_delete(self):
        self.check_response_code('/player/delete/1/', 302)

