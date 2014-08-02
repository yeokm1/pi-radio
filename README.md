pi-radio
========

A Python program will use mplayer to play the correct audio stream based on your selection. Volume and radio stations can be changed via the buttons on the Pi plate.


Hardware
====
1. Raspberry Pi Model B (other models may also work)
2. Adafruit i2c 16x2 LCD Pi Plate with keypad

Dependencies
=====
1. Arch Linux ARM
2. Python
3. mplayer
4. alsa-utils


Setting up dependencies
=====

I use Arch Linux as it is stripped down and boots up far faster than Raspbian. With some modifications to the setup instructions, you can run this on Raspbian as well.

```bash
pacman -Syu python2 python2-pip base-devel mplayer alsa-utils
pip2 install smbus

modprobe i2c-dev
echo "i2c-dev" > /etc/modules-load.d/i2c-dev.conf
reboot

```

Running the app
=====

```bash
python2 radio.py
```

Radio stations
=====

Details on radio stations are kept in the stations.txt file.  Majority of radio stations in Singapore are supported except for 88.3 Jia and Power 98 as I cannot find their online streams.


References and Libraries
=====
1. [Adafruit Char Plate LCD](https://learn.adafruit.com/adafruit-16x2-character-lcd-plus-keypad-for-raspberry-pi/overview)
2. [i2c setup on Arch Linux](http://cfedk.host.cs.st-andrews.ac.uk/site/?q=2013-pi)







