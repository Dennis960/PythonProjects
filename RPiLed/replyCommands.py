from telegramBot import send_message
import controlLed
from myLogging import my_print as print
import re
import vars
import json

# a dictionary of commands with layout 'command' : helpText
commandDict = {
    '/help' : "shows this information",
    '/on' : "turns on all lights",
    '/off' : "turns off all lights",
    '/syncFade' : "Sync fade effects for all stripes",
    '/dumpLedSettingsJson' : "Dumbs the settings json file as message"
}

def reply_help(update, chat_id):
    help = ""# help = open(vars.pathToScript + 'botHelp', 'r').read() + '\n'
    for key in commandDict:
        value = commandDict.get(key)
        help += '\n' + key + ' - ' + value
    send_message(help, chat_id)
def reply_on(update, chat_id):
    controlLed.turn_on_all()
def reply_off(update, chat_id):
    controlLed.turn_off_all()
def reply_syncFade(update, chat_id):
    controlLed.sync_all_fadeColor()
def reply_dumpLedSettingsJson(update, chat_id):
    with open(vars.PATH_TO_SETTINGS_JSON, 'r+') as jsonFile:
        try:
            jsonString = json.dumps(json.load(jsonFile), indent=4)
        except:
            jsonString = "Could not read json file."
        send_message(jsonString, chat_id)

def reply__command_not_found(update, chat_id):
    send_message('command not found', chat_id)

def get_color_data(text):
    matches = re.findall('[0-3][0-2][0-2][0-9][0-9]', text)
    settings = []
    for match in matches:
        stripeIndex = int(match[0])
        colorIndex = int(match[1])
        alpha = int(match[2:5])
        if alpha > 255:
            alpha = 255
        settings.append((stripeIndex, colorIndex, alpha))
    return settings
def get_fade_data(text):
    matches = re.findall('F[0-3][0-2][0-9][0-9][0-9][0-9]', text)
    settings = []
    for match in matches:
        stripeIndex = int(match[1])
        colorIndex = int(match[2])
        duration = int(match[3:7])
        settings.append((stripeIndex, colorIndex, duration))
    return settings

def reply__text(update, chat_id):
    try:
        text = update["message"]["text"]
        if 'F' in text:
            settings = get_fade_data(text)
            if len(settings) == 0:
                send_message("It is so nice to text with you but I don't know what you want me to do!", chat_id)
                return
            for setting in settings:
                stripeIndex, colorIndex, duration = setting
                controlLed.start_color_fade(stripeIndex, colorIndex, duration)
                send_message('settings' + str((stripeIndex, colorIndex, duration)), chat_id)
        else:
            settings = get_color_data(text)
            if len(settings) == 0:
                send_message("It is so nice to text with you but I don't know what you want me to do!", chat_id)
                return
            for setting in settings:
                stripeIndex, colorIndex, alpha = setting
                controlLed.set_light(stripeIndex, colorIndex, alpha)
                send_message('settings' + str((stripeIndex, colorIndex, alpha)), chat_id)
    except Exception as e:
        print(str(e))