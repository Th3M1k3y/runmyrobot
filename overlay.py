IMAGEDIR = "/home/pi/runmyrobot/overlay/"
DESTDIR = "/dev/shm/"

import time
import subprocess
from multiprocessing import Queue, Process
from ina219 import INA219
from shutil import copyfile

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

SHUNT_OHMS = 0.01
MAX_EXPECTED_AMPS = 4
LAST_BAT_LEVEL = 11

def readVoltage():
    global LAST_BAT_LEVEL

    ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS)
    ina.configure(ina.RANGE_32V)

    while True:
        currentVolt = ina.voltage()
        if currentVolt < 8.1:
            print(bcolors.FAIL + "Low voltage, shutting down!" + bcolors.ENDC)
            subprocess.Popen("sudo shutdown -P now", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        if currentVolt >= 11.26:
            if LAST_BAT_LEVEL != 4:
                LAST_BAT_LEVEL = 4
                print(bcolors.OKGREEN + "Updating battery icon, level 4" + bcolors.ENDC)
                copyfile(IMAGEDIR + "/battery_4.png", DESTDIR + "/battery.png")
        elif currentVolt >= 10.52:
            if LAST_BAT_LEVEL != 3:
                LAST_BAT_LEVEL = 3
                print(bcolors.OKGREEN + "Updating battery icon, level 3" + bcolors.ENDC)
                copyfile(IMAGEDIR + "/battery_3.png", DESTDIR + "/battery.png")
        elif currentVolt >= 9.78:
            if LAST_BAT_LEVEL != 2:
                LAST_BAT_LEVEL = 2
                print(bcolors.OKGREEN + "Updating battery icon, level 2" + bcolors.ENDC)
                copyfile(IMAGEDIR + "/battery_2.png", DESTDIR + "/battery.png")
        elif currentVolt >= 9.04:
            if LAST_BAT_LEVEL != 1:
                LAST_BAT_LEVEL = 1
                print(bcolors.WARNING + "Updating battery icon, level 1" + bcolors.ENDC)
                copyfile(IMAGEDIR + "/battery_1.png", DESTDIR + "/battery.png")
        elif currentVolt >= 8.3:
            if LAST_BAT_LEVEL != 0:
                LAST_BAT_LEVEL = 0
                print(bcolors.WARNING + "Updating battery icon, level 0" + bcolors.ENDC)
                copyfile(IMAGEDIR + "/battery_0.png", DESTDIR + "/battery.png")

        print("Battery Voltage: %.3f V" % ina.voltage())
        time.sleep(1)

readBat = Process(target=readVoltage)
readBat.start()


LAST_WIFI_LEVEL = 11

def readWifiStrength():
    global LAST_WIFI_LEVEL

    while True:
        wifiStrength = int(subprocess.Popen("/sbin/iwconfig wlan0 | grep Link | grep -oE -- '-[0-9]{2}'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.readlines()[0].strip())

        if wifiStrength <= -90:
            if LAST_WIFI_LEVEL != 1:
                LAST_WIFI_LEVEL = 1
                print(bcolors.OKGREEN + "Updating wifi icon, level 1" + bcolors.ENDC)
                copyfile(IMAGEDIR + "/wifi_1.png", DESTDIR + "/wifi.png")
        elif wifiStrength <= -80:
            if LAST_WIFI_LEVEL != 2:
                LAST_WIFI_LEVEL = 2
                print(bcolors.OKGREEN + "Updating wifi icon, level 2" + bcolors.ENDC)
                copyfile(IMAGEDIR + "/wifi_2.png", DESTDIR + "/wifi.png")
        elif wifiStrength <= -70:
            if LAST_WIFI_LEVEL != 3:
                LAST_WIFI_LEVEL = 3
                print(bcolors.OKGREEN + "Updating wifi icon, level 3" + bcolors.ENDC)
                copyfile(IMAGEDIR + "/wifi_3.png", DESTDIR + "/wifi.png")
        elif wifiStrength <= -65:
            if LAST_WIFI_LEVEL != 4:
                LAST_WIFI_LEVEL = 4
                print(bcolors.OKGREEN + "Updating wifi icon, level 4" + bcolors.ENDC)
                copyfile(IMAGEDIR + "/wifi_4.png", DESTDIR + "/wifi.png")
        elif wifiStrength <= -30:
            if LAST_WIFI_LEVEL != 5:
                LAST_WIFI_LEVEL = 5
                print(bcolors.OKGREEN + "Updating wifi icon, level 5" + bcolors.ENDC)
                copyfile(IMAGEDIR + "/wifi_5.png", DESTDIR + "/wifi.png")

        print("Wifi level: %d dBm" % wifiStrength)
        time.sleep(1)

readWifi = Process(target=readWifiStrength)
readWifi.start()


def readTemperature():
    while True:
        cpuTemp = int(subprocess.Popen("vcgencmd measure_temp | grep -oE -- '[0-9]{2}.[0-9]'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.readlines()[0].strip())
        print("CPU temperature: %d C" % cpuTemp)

readTemp = Process(target=readTemperature)
#readTemp.start()
