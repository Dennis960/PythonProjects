import urllib
import json
import requests
from myLogging import my_print as print

TOKEN = '****************************************'
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def get_url(url):
    """Gets the content of the Url in utf-8 format"""
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content
def get_json_from_url(url):
    """Returns the repsonse of the url get request in a json format."""
    content = get_url(url)
    js = json.loads(content)
    return js
def get_updates(offset=None):
    """Gets all messages that haven't been processed yet."""
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js
def get_last_update_id(updates):
    """Gets the id of the last message."""
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def send_message(text, chat_id):
    """Sends a message to the given chat"""
    try:
        text = urllib.parse.quote_plus(text)
        url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
        get_url(url)
    except Exception as e:
        print(str(e))