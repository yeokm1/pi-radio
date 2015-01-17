pi-radio
========

Raspberry Pi internet radio streamer for Singapore. Can be modified to stream other internet radio stations. A Python program will use mplayer to play the correct audio stream based on your button selection. 

## Why?

Problems of my FM radio set at my house's living room

1. Occasional poor reception
2. Hassle of having to constantly adjust the antenna
3. Bulky
4. Poor sound quality

## So my solution!

![Screen](/photos/typical.jpg)
Currently selected station and volume level. With a 3D printed case.

![Screen](/photos/muted.jpg)
Muting is possible by pressing the "Select" button. Old picture of the previous blue case.

![Screen](/photos/ipaddress.jpg)
Hate the complication of configuring static IP address and remembering it. Just get it to display on demand! Useful for SSH purposes. Old picture of the previous blue case.


## Features
1. Supports most Singaporean radio stations with online audio streams
2. Volume control
3. Shows IP address when left and right buttons are pressed
4. Better sound quality compared to a typical FM radio
6. (Optional) Starts on boot, waits for internet connection before playing. Ready to play in about 30 seconds.
7. (Optional) Don't need to shutdown properly. Read-only file system prevents data corruption when powered off incorrectly.


## Hardware

1. Raspberry Pi Model B (other models may also work)
2. Adafruit i2c 16x2 LCD Pi Plate with keypad

## Dependencies

1. Arch Linux ARM
2. Python
3. mplayer
4. alsa-utils


### Setting up dependencies

I use Arch Linux as it is stripped down and boots up far faster than Raspbian. With some modifications to the setup instructions, you can run this on Raspbian as well.

```bash
pacman -Syu python2 base-devel git mplayer alsa-utils i2c-tools

modprobe i2c-dev
echo "i2c-dev" > /etc/modules-load.d/i2c-dev.conf
reboot
```

##Use USB adapter instead of default audio output (optional)

"Since the built-in audio out of the raspberry pi is only good for deaf people, it makes sense to remove it. Raspbian has a sysem that makes any usb audio the default one but arch linux doesn’t. Since we want it to work with anything we would plug into it, we’ll just get rid of the bcm2835 so it doesn’t get in our way. To do so, edit the file /etc/modules-load.d/raspberrypi.conf and remove / comment the bcm2835 related modules (bcm2708-rng, snd-bcm2835)"

From [here](http://www.marc-nostromo.com/installing-archlinux-on-raspberry-pi-for-headless-audio/)

## Running the app

```bash
git clone https://github.com/yeokm1/pi-radio.git
cd pi-radio
python2 radio.py
```

## Radio stations

Details on radio stations are kept in the `stations.txt` file.  Majority of radio stations in Singapore are supported except for 88.3 Jia and Power 98 as I cannot find their online streams. You can modify `stations.txt` to include your own stations.


## Start on boot (Optional)

We need to write a systemd service for Arch Linux to launch this app. 

```bash
nano /etc/systemd/system/pi-radio.service

#Add the following lines to pi-radio.service till but not including #end
[Unit]
Description=To start pi-radio on startup
After=network-online.target

[Install]
WantedBy=multi-user.target

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/root/pi-radio/startup.sh
#end

systemctl enable pi-radio.service
```


## Convert to a read-only file system (Optional)
Consult my [gist](https://gist.github.com/yeokm1/8b0ffc03e622ce011010). Volume changes do not persist if a read-only file system is used. To change volume permanently, set to read-write, change to desired volume then reboot.


## References and Libraries

1. [Adafruit Char Plate LCD](https://learn.adafruit.com/adafruit-16x2-character-lcd-plus-keypad-for-raspberry-pi/overview)
2. [i2c setup on Arch Linux](http://cfedk.host.cs.st-andrews.ac.uk/site/?q=2013-pi)
3. [3D case design](http://www.thingiverse.com/thing:101837)
4. [Headless audio for Raspberry Pi](http://www.marc-nostromo.com/installing-archlinux-on-raspberry-pi-for-headless-audio/)
