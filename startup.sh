#!/bin/sh
#ping until reach WAN then start pi radio
while true; do ping -c1 www.google.com.sg &> /dev/null && break; done
cd /root/pi-radio
/usr/bin/python2 radio.py &
