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
            # Execute existing actions in queue
            execute_action_queue(xmms_controller)

            # clear existing player attribute
            xmms_controller.clear_player()
            xmms_controller.get_player_info()
            # We need to update the db with the relevant info
            timeout = update_status(xmms_controller.player)
            save_songs(xmms_controller.player)
            time.sleep(timeout/1000.0)
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
    # Set number of songs in playlist
    xmmsStatus.playlist_size = player.playlist_size()
    # Save back to db
    xmmsStatus.save()
    return xmmsStatus.timeout

def save_songs(player):
    """
    Saves all the songs in the playelist into the db
    then removes all the old songs
    """
    
    # Save the current song
    song = player.current_song
    song.position = 0
    song.active = False
    song.save()
    
    # # Now save the other songs
    for song in player.playlist:
        song.active = False
        song.save()

    # Delete all the old songs
    Song.objects.filter(active=True).delete()
    Song.objects.all().update(active=True)


def execute_action_queue(xmms_controller):
    """
    Retrieves the queue of actions from the db, executes each item in the queue 
    and delete those items immediately after execution
    """
    for action in Action.objects.all():
        execute_action(xmms_controller, action.command)
        action.delete()

def execute_action(xmms_controller, command):
    """
    Executes the provided command
    """
    # Make command matching case insensitive
    command = command.lower()
    if command in ("play", "stop", "pause", "next", "previous"):
        xmms_controller.action(command)
    # Double parenthesis are because add and delete are in a tuple
    elif command.startswith(("add", "delete",)):
        # explode the command, it will be in the form of "add_path/to/file.mp3"
        split_command = command.partition("_")
        if split_command[2]:
            if split_command[0] == "add":
                xmms_controller.enqueue(split_command[2])
            elif split_command[0] == "delete":
                print( xmms_controller.delete(int(split_command[2])) )
