#!/usr/bin/env python
#
# !!! Needs psutil (+ dependencies) installing:
#
#    $ sudo apt-get install python-dev
#    $ sudo pip install psutil
#

import os
import sys
import time
if os.name != 'posix':
    sys.exit('platform not supported')
import psutil
from trello import TrelloApi

from datetime import datetime
from oled.device import ssd1306, sh1106
from oled.render import canvas
from PIL import ImageDraw, ImageFont

# TODO: custom font bitmaps for up/down arrows
# TODO: Load histogram

def bytes2human(n):
    """
    >>> bytes2human(10000)
    '9K'
    >>> bytes2human(100001221)
    '95M'
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i+1)*10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = int(float(n) / prefix[s])
            return '%s%s' % (value, s)
    return "%sB" % n

def cpu_usage():
    # load average, uptime
    uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
    av1, av2, av3 = os.getloadavg()
    return "Ld:%.1f %.1f %.1f Up: %s" \
            % (av1, av2, av3, str(uptime).split('.')[0])

def mem_usage():
    usage = psutil.virtual_memory()
    return "Mem: %s %.0f%%" \
            % (bytes2human(usage.used), 100 - usage.percent)


def disk_usage(dir):
    usage = psutil.disk_usage(dir)
    return "SD:  %s %.0f%%" \
            % (bytes2human(usage.used), usage.percent)

def network(iface):
    stat = psutil.net_io_counters(pernic=True)[iface]
    return "%s: Tx%s, Rx%s" % \
           (iface, bytes2human(stat.bytes_sent), bytes2human(stat.bytes_recv))

def stats(oled):
    font = ImageFont.load_default()
    font2 = ImageFont.truetype('redalert.ttf', 12)
    with canvas(oled) as draw:
        draw.text((0, 0), cpu_usage(), font=font2, fill=255)
        draw.text((0, 14), mem_usage(), font=font2, fill=255)
        draw.text((0, 26), disk_usage('/'), font=font2, fill=255)
        draw.text((0, 38), network('wlan0'), font=font2, fill=255)

def trello(oled):
    ourkey = open('.trello-screen-api-key').read();
    ourtoken = open('.trello-screen-token').read();
    ourlist = open('.trello-screen-list').read();
    trello = TrelloApi(ourkey, token=ourtoken)
    cards = trello.lists.get_card(ourlist)
    index = 0
    font2 = ImageFont.truetype('redalert.ttf', 12)
    with canvas(oled) as draw:
        draw.text((0,0), "Working on " + str(len(cards)) + " things:", font=font2, fill=255)
        while index < len(cards) and index < 4:
            draw.text((12,13+(index*13)),cards[index]['name'], font=font2, fill=255)
            index = index + 1

def main():

    oled = ssd1306(port=2, address=0x3C)
    while True:
        trello(oled)
        time.sleep(60*10)

if __name__ == "__main__":
    main()
