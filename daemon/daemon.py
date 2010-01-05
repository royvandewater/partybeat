from django.core.management.base import BaseCommand

import sys
import os
import time
import datetime

from models import *
from xmms_controller import Xmms_controller

def main(argv):
    # perform initialization
    xmms_controller = Xmms_controller()

    print("Daemon Initialized")
    
    # enter main loop
    try:
        while True:
            # clear existing player attribute
            xmms_controller.clear_player()
            xmms_controller.get_player_info()
            print('.')
            # We need to update the db with the relevant info
            timeout = update_status(xmms_controller.player)
            save_songs(xmms_controller.player)

            time.sleep(timeout/1000)
    except KeyboardInterrupt:
        print("\nDaemon terminating")
        sys.exit(0)

def update_status(player):
    """ 
    Updates the XmmsStatus object in the db with current xmms2 status 
    Expects an up-to-date Player() object from player_info.py
    """
    # Start by retrieving the status object
    xmmsStatus = XmmsStatus.objects.get()
    # Set the current action
    xmmsStatus.current_action = player.status
    # Set update time
    xmmsStatus.last_update = datetime.datetime.now()
    # Save back to db
    xmmsStatus.save()
    return xmmsStatus.timeout

def save_songs(player):
    """
    Saves all the songs in the playelist into the db
    (First removes all the existing songs)
    """
    # Delete all the songs
    Song.objects.all().delete()
    
    # Save the current song
    song = player.current_song
    song.position = 0
    song.save()
    
    # # Now save the other songs
    for song in player.playlist:
        song.save()
