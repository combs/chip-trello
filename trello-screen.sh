#!/bin/bash
cd /home/chip
/usr/sbin/i2cset -f -y 0 0x34 0x93 0x0

until python3 trello-screen.py; do 
    echo "'trello-screen.py' crashed with exit code $?.  Respawning.." >&2
    sleep 1
done

