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


API_BASE = "https://api.telegram.org/bot121457064:AAG5bEZ2_8KBNYJMuY40HisuZaXluUNbmCg/"
UPDATES_OFFSET = "184803575" #FIXME: This needs to be updated every time the bot is added to a new group

def do_get_request(api, params={}):
    r = requests.get(API_BASE + api, params)
    return r.text

def fetch_image(query):
    """Download a random image from Google image search."""
    BASE_URL = 'https://ajax.googleapis.com/ajax/services/search/images?'\
               'v=1.0&q=' + query + '&start=%d'

    start = random.randint(0, 60)  # Take a random number for google pagination
    r = requests.get(BASE_URL % start)
    image = json.loads(r.text)['responseData']['results'][random.randint(0, 3)]  # Take a random picture out of the 4 available
    url = image['unescapedUrl']
    return url

def send_message(msg):
    do_get_request("sendMessage", params={"chat_id": GROUP_ID, "text": msg})

def send_milf():
    url = fetch_image("milf")
    send_message(url)

def send_cameltoe():
    url = fetch_image("cameltoe")
    send_message(url)

def send_rustelle():
    url = fetch_image("arrosticini")
    send_message(url)

def show_help():
    print("HELP!")
    msg = """Il bot del FermoLUG\n\nComandi disponibili:\n/milf: mostra una foto random di MILF\n/cameltoe: mostra una foto random di cameltoe\n/rustelle: mostra una foto random di rustelle"""
    send_message(msg)

while True:
    updates = do_get_request("getUpdates", params={"offset": UPDATES_OFFSET})
    data = json.loads(updates)

    for message in data["result"]:
        GROUP_ID = message["message"]["chat"]["id"]
        UPDATES_OFFSET = message["update_id"] + 1

        message_text = (message["message"]["text"])
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
    sleep(1)
