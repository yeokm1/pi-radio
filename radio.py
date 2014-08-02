#!/usr/bin/python
import time
import os
import shlex
import re

from time import sleep
from subprocess import call
from subprocess import Popen, PIPE
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate


debounceTime = 150
stationFilename = "stations.txt"
startPlayer = "mplayer "
killPlayerCommand = ["killall mplayer"]
getMixerCommand = "amixer -sget PCM"
findVolumeRegex = ".*Playback (.*)\[(.*)%\] \[(.*)\] \[(.*)\]"
setVolumeCommand = "amixer -q set PCM "
toggleMuteCommand = "amixer -q set PCM toggle"


regex = re.compile(findVolumeRegex)

stationsList = []
lcd = Adafruit_CharLCDPlate()
stationIndex = 0
numStations = None


lcd.clear()


stationsFile = open(stationFilename, 'r')
lines = stationsFile.read().splitlines()
stationsFile.close()

numStations = len(lines)

for line in lines:
    splitLine = line.split(" | ")
    stationsList.append(splitLine)


def getTime():
  return int(round(time.time() * 1000))

def shouldIProcessThisPress():
  global previousPressedTime
  currentTime = getTime()
  timeDifference = currentTime - previousPressedTime
  if timeDifference > debounceTime:
    previousPressedTime = currentTime
    return True
  else:
    return False

def getStdout(cmd):
    args = shlex.split(cmd)
    proc = Popen(args, stdout=PIPE, stderr=PIPE, shell=True)
    out, err = proc.communicate()
    return out

def getVolume():
  amixerOutput = getStdout(getMixerCommand)
  r = regex.search(amixerOutput)
  volume = r.groups()[1]
  active = r.groups()[3]
  return volume, active

def setVolumePercent(newVolume):
  setVolumeStr = setVolumeCommand + str(newVolume) + "%"
  call(shlex.split(setVolumeStr))

def toggleMute():
  call(shlex.split(toggleMuteCommand))

def refreshLCD():

  volumePercent, soundStatus = getVolume()
  textToShow = stationsList[stationIndex][0] + "\n" + "Volume: "

  if soundStatus == 'on':
    textToShow += volumePercent + "%"
  else:
    textToShow += "Muted"

  lcd.clear()
  lcd.message(textToShow)

def setNewVolume(increment):
  global currentVolume
  if increment:
    currentVolume += 1
  else:
    currentVolume -= 1
  
  if currentVolume > 100:
    currentVolume = 100

  elif currentVolume < 0:
    currentVolume = 0

  setVolumePercent(currentVolume)


def setNextStation(increment):
  global stationIndex
  if increment:
    stationIndex += 1
  else:
    stationIndex -= 1

  stationIndex %= numStations




currentVolume = int(getVolume()[0])

previousPressedTime = getTime()
refreshLCD()


while True:
    if lcd.buttonPressed(lcd.UP) and shouldIProcessThisPress():
      setNewVolume(True)
      refreshLCD()
    elif lcd.buttonPressed(lcd.DOWN) and shouldIProcessThisPress():
      setNewVolume(False)
      refreshLCD()
    elif lcd.buttonPressed(lcd.SELECT) and shouldIProcessThisPress():
      toggleMute()
      refreshLCD()
    elif lcd.buttonPressed(lcd.LEFT) and shouldIProcessThisPress():
      setNextStation(False)
      refreshLCD()
    elif lcd.buttonPressed(lcd.RIGHT) and shouldIProcessThisPress():
      setNextStation(True)
      refreshLCD()




  