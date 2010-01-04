from django.core.management.base import BaseCommand
from xmms_controller import Xmms_controller

import sys
import time

def main(argv):
    # perform initialization
    xmms_controller = Xmms_controller()
    
    # enter main loop
    try:
        while True:
            xmms_controller.get_player_info()
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nDaemon terminating")
        sys.exit(0)
