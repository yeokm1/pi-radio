pi-radio
========

A Python program will use mplayer to play the correct audio stream based on your selection. Volume and radio stations can be changed via the buttons on the Pi plate.


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
pacman -Syu python2 python2-pip base-devel git mplayer alsa-utils
pip2 install smbus

modprobe i2c-dev
echo "i2c-dev" > /etc/modules-load.d/i2c-dev.conf
reboot
```

## Running the app

```bash
git clone https://github.com/yeokm1/pi-radio.git
cd pi-radio
python2 radio.py
```

## Radio stations

Details on radio stations are kept in the `stations.txt` file.  Majority of radio stations in Singapore are supported except for 88.3 Jia and Power 98 as I cannot find their online streams. You can modify `stations.txt` to include your own stations.


## Start on boot

We need to write a systemd service for Arch Linux to launch this app. 

```bash
nano /etc/systemd/system/pi-radio.service

#Add the following lines to pi-radio.service till but not including #end
[Unit]
Description=To start pi-radio on startup
After=network.target

[Install]
WantedBy=multi-user.target

[Service]
Type=idle
RemainAfterExit=yes
ExecStart=python2 /root/radio.py
#end

systemctl enable pi-radio.service
```


## Convert to a read-only file system (Optional)

Unlike your typical computer where you usually shutdown properly, I cannot rely on this during the use of a Raspberry Pi. If the Raspberry Pi is improperly shutdown too many times, data corruption in the file system leading to unbootable SD card may result. So we should use a read-only file system.

Full instructions and explanations are obtained from this [link](http://ruiabreu.org/2013-06-02-booting-raspberry-pi-in-readonly.html) but you can run this commands directly. I modified some of the instructions for personal convenience.

```bash
#Change timezone.
rm /etc/localtime
ln -s /usr/share/zoneinfo/Asia/Singapore /etc/localtime

#Update everything first, remove cache then reboot to detect problems
pacman -Syu  
pacman -Sc
reboot

#Relocate DNS cache
rm /etc/resolv.conf
ln -s /tmp/resolv.conf /etc/resolv.conf

#Adjust /etc/fstab, add/modify to the following hashed lines. Mount certain directories to RAM disk.
nano /etc/fstab
#/dev/mmcblk0p1  /boot   vfat    defaults,ro,errors=remount-ro        0       0
#tmpfs   /var/log    tmpfs   nodev,nosuid    0   0
#tmpfs   /var/tmp    tmpfs   nodev,nosuid    0   0

#To mount / partition as read-only
nano /boot/cmdline.txt
#Add an ro flag right after the root= parameter.

#Disable systemd services
systemctl disable systemd-readahead-collect
systemctl disable systemd-random-seed
systemctl disable ntpd

#Put shortcut shell scripts to re-enable read-write temporarily if needed
printf "mount -o remount,rw /" > readwrite.sh
printf "mount -o remount,ro /" > readonly.sh
chmod 500 readwrite.sh
chmod 500 readonly.sh

#Remove history
history -c -w

reboot
```


To enable read-write temporarily to do say an update, just run `./readwrite.sh` .



## References and Libraries

1. [Adafruit Char Plate LCD](https://learn.adafruit.com/adafruit-16x2-character-lcd-plus-keypad-for-raspberry-pi/overview)
2. [i2c setup on Arch Linux](http://cfedk.host.cs.st-andrews.ac.uk/site/?q=2013-pi)







