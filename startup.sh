#!/bin/sh
#ping until reach WAN then start pi radio
for i in {1..50}; do ping -c1 www.google.com.sg &> /dev/null && break;
cd /root/pi-radio
/usr/bin/python2 radio.py &
