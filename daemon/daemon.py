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
    # Start xmms2 and immediatly pause
    os.system("xmms2 play")
    os.system("xmms2 pause")
    # perform initialization
    xmms_controller = Xmms_controller()

    print("Daemon Initializing...")
    # Check for active connection
    print("Waiting for xmms2...")

    fail_count = 0
    while True:
        try:
            connected = False
            while not connected:
                if fail_count > 5:
                    print("starting xmms2 manually")
                    print("If nothing happnes, try adding a song to the queue manually")
                    os.system("xmms2 play")
                    fail_count = 0
                connected = check_for_connection(xmms_controller)
                fail_count += 1
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
                        time.sleep(timeout/1000.0)
                        fail_count = 0
            except KeyboardInterrupt:
                print("\nDaemon terminating")
                sys.exit(0)

        except (AttributeError, TypeError,):
            os.system("xmms2 quit")
            if fail_count == 2:
                print("Two restarts failed, I give up")
                sys.exit(-1)
            elif fail_count:
                os.system("xmms2 clear")
                fail_count = 2
            else:
                fail_count = 1
            os.system("xmms2 play")
            os.system("xmms2 pause")

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
    # Set position of current song in playlist
    xmmsStatus.current_position = player.position
    xmmsStatus.volume = player.volume
    # Set seek time of song
    xmmsStatus.seek = player.seek
    xmmsStatus.max_seek = player.max_seek
    # Save back to db
    xmmsStatus.save()
    return xmmsStatus.timeout

def save_songs(player):
    """
    Saves all the songs in the playelist into the db
    then removes all the old songs
    """
    # Reference to see if anything has changed
    Song.objects.all().delete()

    # Build current song list
    new_songs = []
    new_songs.append(player.current_song)
    new_songs[0].position = 0

    for song in player.playlist:
        new_songs.append(song)

    for song in new_songs:
        song.save()

def execute_action_queue(xmms_controller):
    """
    Retrieves the queue of actions from the db, executes each item in the queue
    and delete those items immediately after execution
    """
    number_of_deletes = 0
    for action in Action.objects.all():
        if action.command.lower().startswith("delete"):
            s_command = list(action.command.partition("_"))
            s_command[2] = str(int(s_command[2]) + number_of_deletes)
            number_of_deletes += 1
            action.command = "".join(s_command)
        execute_action(xmms_controller, action.command)
        action.delete()

def execute_action(xmms_controller, command):
    """
    Executes the provided command
    """
    # Make command matching case insensitive
    if command.lower() in ("play", "stop", "pause", "next", "previous", "shuffle"):
        xmms_controller.action(command)
    # Double parenthesis are because add and delete are in a tuple
    elif command.lower().startswith(("add", "delete", "seek", "skip", "volume")):
        # explode the command, it will be in the form of "add_path/to/file.mp3"
        split_command = command.partition("_")
        if split_command[2]:
            xmmsStatus = XmmsStatus.objects.get()
            if split_command[0].lower() == "add":
                xmms_controller.enqueue(split_command[2])
            elif split_command[0] == "delete":
                song_number = int(split_command[2])
                try:
                    song = Song.objects.get(position=song_number)
                    song.delete()
                    xmmsStatus.playlist_size -= 1
                    xmms_controller.delete(song_number)
                except Exception:
                    pass
            elif split_command[0] == "seek":
                seek_time = int(split_command[2])
                xmms_controller.seek(seek_time)
                xmmsStatus.seek = seek_time
            elif split_command[0] == "skip":
                xmms_controller.skip_to(int(split_command[2]))
            elif split_command[0] == "volume":
                volume = int(split_command[2])
                xmms_controller.volume(volume)
                xmmsStatus.volume = volume
            xmmsStatus.save()
    elif command.lower().startswith("move",):
        # explode the command, it will be in the form of move_from_to
        split_command = command.split("_")
        if split_command[0] == "move":
            start = int(split_command[1])
            end = int(split_command[2])
            xmms_controller.move(start, end)

def check_for_connection(xmms_controller):
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
