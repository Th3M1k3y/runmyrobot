import requests
import json

# Auth token, do not share with anyone!
authToken = ''

# Robot ID for the robot you want to modify
robotID = 0

# JSON for custom panels
panels = '[]'

panels = json.dumps(panels)

json_output = '{"public":"true","anonymous_control":"false","profanity_filter":"true","non_global_chat":"false","no_exclusive_control_button":"false","mute_text-to-speech":"false","mic_enabled":"true","dev_mode":"false","custom_panels":"true","panels":' + panels + "}"

url = 'https://api.letsrobot.tv/api/v1/robots/' + str(robotID)
response = requests.post(url, data=json_output, headers={"Content-Type": "application/json", "Authorization": "Bearer " + authToken})

#print(response)
print(response.text)
