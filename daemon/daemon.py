from django.core.management.base import BaseCommand
from xmms_controller import Xmms_controller

import sys
import os
import time
import datetime

sys.path.append('/home/doppler/Projects/git/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'xmms2_django.settings'
from xmms2_django.xmms2.models import *

def main(argv):
    # perform initialization
    xmms_controller = Xmms_controller()

    print("Daemon Initialized")
    
    # enter main loop
    try:
        while True:
            xmms_controller.get_player_info()
            print('.')
            # We need to update the db with the relevant info
            timeout = update_status(xmms_controller.player)

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
