from socketIO_client import SocketIO, LoggingNamespace
import requests
from thread import start_new_thread
import time
import subprocess as sub
import datetime
import json
from jsonmerge import merge

update_last_json = ''


# Robot ID for the robot you want to modify
robotID = '56250484'

# Auth token, do not share with anyone!
authToken = ''


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Handle commands received
def on_command(*args):
    commandData = args[0]
    #print commandData
    # If we received the smoke command on key down
    if commandData['command'] == 'smoke' and commandData['key_position'] == 'down':
        # Try calling the smoke machine to activate it
        try:
            r  = requests.get('http://192.168.1.5/go?smoke=250', timeout=0.5)
            print('\t' + r.text)
        except requests.exceptions.RequestException as e:
            print bcolors.FAIL + '\t' + str(e) + bcolors.ENDC

# Thread for connecting to controls server
def connect_controls():
    controlSocketInfo = requests.get('https://letsrobot.tv/get_control_host_port/' + robotID)
    print controlSocketInfo.json()

    if controlSocketInfo.json()['port'] == 8022:
        print 'Wrong port, retrying...'
        time.sleep(5)
        connect_controls()
    else:
        socketIO = SocketIO(controlSocketInfo.json()['host'], controlSocketInfo.json()['port'], LoggingNamespace)
        socketIO.on('command_to_robot', on_command)
        socketIO.on('disconnect', connect_controls)
        socketIO.wait()

#Thread for updating buttons
def update_buttons():
    global robotID, authToken, update_last_json
    button_count = 0

    while 1:
        now = datetime.datetime.now()
        print bcolors.HEADER + now.strftime("%Y-%m-%d %H:%M:%S") + bcolors.ENDC

        aux_buttons = {}
        panels = []

        # Try calling the smoke machine to see if it is turned on
        try:
            r  = requests.get('http://192.168.1.5/status.txt', timeout=0.75)
            returned = json.loads(r.text)
            print('\t' + r.text)
            # If the smoke machine is un, pumpstatus needs to be above 0, if it is 0 the smoke machine is still heating up
            if returned['pumpstatus'] > 0:
                # On every 00, 15, 30 and 45 minute mark, we are making the smoke command free
                if now.minute % 15 == 0:
                    button = {"label":"smoke machine","command":"smoke"}
                else:
                    button = {"label":"smoke machine","command":"smoke","premium":True,"price":25}
                    
                #Actually, if Ged fills the room with smoke over and over, we cheat and make it permanently premium ;)
                button = {"label":"smoke machine","command":"smoke","premium":True,"price":25}
                
                aux_buttons = merge(aux_buttons, button)
        except requests.exceptions.Timeout:
            print bcolors.OKBLUE + '\tSmoke machine offline' + bcolors.ENDC
        except requests.exceptions.RequestException as e:
            print bcolors.FAIL + '\t' + str(e) + bcolors.ENDC

        # Hold the buttons for the aux panel
        aux_panel = {"button_panel_label":"auxiliary controls", "buttons": aux_buttons}

        # If we got more than zero buttons, we need to use the json with the aux panel in
        if len(aux_buttons) > 0:
            panels = [{"button_panels":[{"button_panel_label":"movement controls","buttons":[{"label":"left","command":"L"},{"label":"right","command":"R"},{"label":"forward","command":"F"},{"label":"backward","command":"B"},{"label":"loud_for_10sec","command":"LOUD","premium":True,"price":50}]},{"button_panel_label":"led controls","buttons":[{"label":"brighter","command":"brightness_up"},{"label":"dimmer","command":"brightness_down"},{"label":"white","command":"leds ffffff"},{"label":"red","command":"leds ff0000"},{"label":"green","command":"leds 00ff00"},{"label":"blue","command":"leds 0000ff"}]}, aux_panel]}]
        else:
            panels = [{"button_panels":[{"button_panel_label":"movement controls","buttons":[{"label":"left","command":"L"},{"label":"right","command":"R"},{"label":"forward","command":"F"},{"label":"backward","command":"B"},{"label":"loud_for_10sec","command":"LOUD","premium":True,"price":50}]},{"button_panel_label":"led controls","buttons":[{"label":"brighter","command":"brightness_up"},{"label":"dimmer","command":"brightness_down"},{"label":"white","command":"leds ffffff"},{"label":"red","command":"leds ff0000"},{"label":"green","command":"leds 00ff00"},{"label":"blue","command":"leds 0000ff"}]}]}]

        # The json we are going to send to the server
        json_output = {"public":True,"anonymous_control":False,"profanity_filter":True,"non_global_chat":True,"no_exclusive_control_button":False,"mute_text-to-speech":False,"mic_enabled":True,"dev_mode":False,"custom_panels":True,"panels": json.dumps(panels)}

        # If the current json is different from the last, we are going to post it
        if update_last_json != json_output:
            update_last_json = json_output
            url = 'https://api.letsrobot.tv/api/v1/robots/' + str(robotID)
            #print json.dumps(json_output)
            try:
                response = requests.post(url, data=json.dumps(json_output), headers={"Content-Type": "application/json", "Authorization": "Bearer " + authToken})
                print('\t' + response.text)
            except requests.exceptions.RequestException as e:
                print '\t' + str(e)

        # Calculate the delay until next 10th second tick
        now = datetime.datetime.now()
        sleep_time = 10 - (now.second % 10)
        if sleep_time == 0:
            sleep_time = 10
        time.sleep(sleep_time)


try:
    start_new_thread(connect_controls, ())
    start_new_thread(update_buttons, ())
except:
    print "Error: unable to start threads"
    exit()

while 1:
    time.sleep(10)
