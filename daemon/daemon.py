from django.core.management.base import BaseCommand

import sys
import os
import time
import datetime

from models import *
from xmms_controller import Xmms_controller

def song_sort(song):
    return song.position 

def main(argv):
    # perform initialization
    xmms_controller = Xmms_controller()

    print("Daemon Initializing...")
    # Check for active connection
    print("Waiting for xmms2...")

    connected = False
    while not connected:
        connected = check_for_connetion(xmms_controller)
        time.sleep(1)

    print("xmms2 found")
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
            timeout = 100
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
    
    # Reference to see if anything has changed
    old_songs = sorted(Song.objects.filter(active=True), key=song_sort)

    # Build current song list
    new_songs = []
    new_songs.append(player.current_song)
    new_songs[0].position = 0

    for song in player.playlist:
        new_songs.append(song)

    if not all_the_same(old_songs, new_songs):
        for song in new_songs:
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
    if command.lower() in ("play", "stop", "pause", "next", "previous"):
        xmms_controller.action(command)
    # Double parenthesis are because add and delete are in a tuple
    elif command.lower().startswith(("add", "delete",)):
        # explode the command, it will be in the form of "add_path/to/file.mp3"
        split_command = command.partition("_")
        if split_command[2]:
            if split_command[0].lower() == "add":
                xmms_controller.enqueue(split_command[2])
            elif split_command[0] == "delete":
                print( xmms_controller.delete(int(split_command[2])) )

def check_for_connetion(xmms_controller):
    """ Returns true if the xmms connection is valid """
    xmms_controller.get_player_info()
    if xmms_controller.player.status or xmms_controller.player.status == 0:
        return True
    else:
        return False

def all_the_same(old_songs, new_songs):
    if len(old_songs) != len(new_songs):
        return False
    for old, new in zip(old_songs, new_songs):
        if old.xmms_id != new.xmms_id:
            return False
    return True
