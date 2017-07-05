IMAGEDIR = "/home/pi/runmyrobot/overlay/"
DESTDIR = "/dev/shm/"

import time
import subprocess
import argparse
import requests
from multiprocessing import Queue, Process
from shutil import copyfile

parser = argparse.ArgumentParser (description='overlay controls')
parser.add_argument('--battery', dest='batt', action='store_true')
parser.set_defaults(batt=False)
parser.add_argument('--wifi', dest='wifi', action='store_true')
parser.set_defaults(wifi=False)
parser.add_argument('--pushover-user', help='User token for sending messages with pushover', default='')
parser.add_argument('--pushover-robot', help='Robot name, used when sending messages with pushover', default='Robot')


args = parser.parse_args()


if args.batt == False and args.wifi == False:
    print("Use --battery and --wifi to enable script")
    exit()


if args.batt:
    from ina219 import INA219


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
AVG_BAT_LEVEL = 0.0

LAST_WIFI_LEVEL = 11

if len(args.pushover_user) > 0:
    if len(args.pushover_user) != 30:
        print(bcolors.FAIL + "There is something wrong with your pushover user token, please check it again" + bcolors.ENDC)
        exit()

def sendPushmessage(str):
    global PUSHOVER_ROBOT
    global PUSHOVER_SOUND
    global PUSHOVER_USER
    print("Sending message")
    r = requests.post("https://api.pushover.net/1/messages.json", data={'user': args.pushover_user, 'token': 'a2fceei5fpoetcc9eu3191ckjbavkg', 'title': args.pushover_robot, 'sound': 'pushover', 'message': str})
    print(r.status_code, r.reason)

def readValues():
    global LAST_BAT_LEVEL
    global AVG_BAT_LEVEL
    global LAST_WIFI_LEVEL

    if args.batt:
        ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS)
        ina.configure(ina.RANGE_32V)

    while True:
        if args.batt:
            currentVolt = ina.voltage()

            if abs(AVG_BAT_LEVEL-currentVolt) > 1.5:
                AVG_BAT_LEVEL = currentVolt
            else:
                AVG_BAT_LEVEL = (AVG_BAT_LEVEL * 0.75) + (currentVolt * 0.25)

            currentVolt = AVG_BAT_LEVEL

            if currentVolt < 8.75:
                print(bcolors.FAIL + "Low voltage, shutting down!" + bcolors.ENDC)
                sendPushmessage("Battery low, shutting down\n%.2fV" % currentVolt)
                subprocess.Popen("sudo shutdown -P now", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            if currentVolt <= 8.75:
                if LAST_BAT_LEVEL != 0:
                    LAST_BAT_LEVEL = 0
                    print(bcolors.OKGREEN + "Updating battery icon, level 0 (0%)" + bcolors.ENDC)
                    copyfile(IMAGEDIR + "/battery_0.png", DESTDIR + "/battery.png")
            elif currentVolt <= 9.4:
                if LAST_BAT_LEVEL != 1:
                    LAST_BAT_LEVEL = 1
                    print(bcolors.OKGREEN + "Updating battery icon, level 1 (25%)" + bcolors.ENDC)
                    copyfile(IMAGEDIR + "/battery_1.png", DESTDIR + "/battery.png")
            elif currentVolt <= 10.35:
                if LAST_BAT_LEVEL != 2:
                    LAST_BAT_LEVEL = 2
                    print(bcolors.OKGREEN + "Updating battery icon, level 2 (50%)" + bcolors.ENDC)
                    copyfile(IMAGEDIR + "/battery_2.png", DESTDIR + "/battery.png")
            elif currentVolt <= 10.9:
                if LAST_BAT_LEVEL != 3:
                    LAST_BAT_LEVEL = 3
                    print(bcolors.WARNING + "Updating battery icon, level 3 (75%)" + bcolors.ENDC)
                    copyfile(IMAGEDIR + "/battery_3.png", DESTDIR + "/battery.png")
            else:
                if LAST_BAT_LEVEL != 4:
                    LAST_BAT_LEVEL = 4
                    print(bcolors.WARNING + "Updating battery icon, level 4 (100%)" + bcolors.ENDC)
                    copyfile(IMAGEDIR + "/battery_4.png", DESTDIR + "/battery.png")

            print("Battery Voltage: %.2f V" % currentVolt)

        if args.wifi:
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
            elif wifiStrength <= -50: #-65
                if LAST_WIFI_LEVEL != 4:
                    LAST_WIFI_LEVEL = 4
                    print(bcolors.OKGREEN + "Updating wifi icon, level 4" + bcolors.ENDC)
                    copyfile(IMAGEDIR + "/wifi_4.png", DESTDIR + "/wifi.png")
            else:
                if LAST_WIFI_LEVEL != 5:
                    LAST_WIFI_LEVEL = 5
                    print(bcolors.OKGREEN + "Updating wifi icon, level 5" + bcolors.ENDC)
                    copyfile(IMAGEDIR + "/wifi_5.png", DESTDIR + "/wifi.png")

            print("Wifi level: %d dBm" % wifiStrength)
        
        time.sleep(1)

readVal = Process(target=readValues)
readVal.start()
