#!/usr/bin/env python3

# FermoLUGbot
#
# Copyright (C) 2015 Andrea Colangelo
#
# Author: Andrea Colangelo <warp10@debian.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA.


import requests
import json
from time import sleep
import random

BOT_VERSION = 0.1
API_BASE = "https://api.telegram.org/bot121457064:AAG5bEZ2_8KBNYJMuY40HisuZaXluUNbmCg/"
UPDATES_OFFSET = "184803589" #FIXME: This should be retrieved during the first iteration.

def do_get_request(api, params={}):
    """Perform a get request to Telegram"""

    r = requests.get(API_BASE + api, params)
    return r.text

def send_message(msg):
    """Send a message to the group the latest update came from"""
    do_get_request("sendMessage", params={"chat_id": GROUP_ID, "text": msg})

def fetch_image_url(query):
    """Download a random image from Google image search."""
    BASE_URL = 'https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=' + query + '&start=%d'
    start = random.randint(0, 60)  # Take a random number for google pagination

    r = requests.get(BASE_URL % start)
    image = json.loads(r.text)['responseData']['results'][random.randint(0, 3)]  # Take a random picture out of the 4 available
    url = image['unescapedUrl']

    return url

def send_milf():
    url = fetch_image_url("milf")
    send_message(url)

def send_cameltoe():
    url = fetch_image_url("cameltoe")
    send_message(url)

def send_rustelle():
    url = fetch_image_url("arrosticini")
    send_message(url)

def show_help():
    msg = """Il bot del FermoLUG - versione %s\n\nComandi disponibili:\n/milf: mostra una foto random di MILF\n/cameltoe: mostra una foto random di cameltoe\n/rustelle: mostra una foto random di rustelle\n\nQuesto software è Software Libero: https://github.com/warp10/fermolugbot""" % str(BOT_VERSION)
    send_message(msg)

def send_image(query):
    if query:
        url = fetch_image_url(query)
        send_message(url)

#Entry point
if __name__ == '__main__':
    while True:
        updates = do_get_request("getUpdates", params={"offset": UPDATES_OFFSET})
        data = json.loads(updates)

        for message in data["result"]:
            GROUP_ID = message["message"]["chat"]["id"]
            UPDATES_OFFSET = message["update_id"] + 1
            try:
                message_text = (message["message"]["text"])
            except:
                message_text = ""

            if message_text.startswith("@FermoLUGbot"):
                message_text = message_text[len("@FermoLUGbot "):]

            if message_text.startswith("/milf"):
                send_milf()
            if message_text.startswith("/cameltoe"):
                send_cameltoe()
            if message_text.startswith("/rustelle"):
                send_rustelle()
            if message_text.startswith("/help"):
                show_help()
            if message_text.startswith("/image"):
                send_image(message_text[len("/image "):])

        sleep(1)
