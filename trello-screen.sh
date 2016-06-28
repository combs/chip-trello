#!/bin/bash
cd /home/chip
/usr/sbin/i2cset -f -y 0 0x34 0x93 0x0
python trello-screen.py
