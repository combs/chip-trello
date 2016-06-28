#!/usr/bin/env python
#
# !!! Needs psutil (+ dependencies) installing:
#
#    $ sudo apt-get install python-dev
#    $ sudo pip install psutil
#

import RPi_I2C_driver
from time import *
import os
import sys
import time
if os.name != 'posix':
    sys.exit('platform not supported')
from trello import TrelloApi

from datetime import datetime

def trello(mylcd):
    ourkey = open('.trello-screen-api-key').read();
    ourtoken = open('.trello-screen-token').read();
    ourlist = open('.trello-screen-list').read();
    try:

        trello = TrelloApi(ourkey, token=ourtoken)
        cards = trello.lists.get_card(ourlist)
        index = 0
        mylcd.lcd_display_string("Working on " + str(len(cards)) + " things:", 1)

        while index < len(cards) and index < 3:
            thestring = " " + cards[index]['name'][:19]
            mylcd.lcd_display_string(thestring, index + 2)
            mylcd.lcd_display_string("", index + 2)
            mylcd.lcd_write_char(165)
            index = index + 1
    except HTTPError:
        print("Error fetching Trello list")
    except:
        print("Unexpected error: ", sys.exc_info()[0])


def main():

    mylcd = RPi_I2C_driver.lcd()

#    oled = ssd1306(port=2, address=0x3C)
    while True:
        trello(mylcd)
        time.sleep(60*10)

if __name__ == "__main__":
    main()
