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

BOT_VERSION = 0.3
API_BASE = "https://api.telegram.org/bot121457064:AAG5bEZ2_8KBNYJMuY40HisuZaXluUNbmCg/"
UPDATES_OFFSET = "184803589" #FIXME: This should be retrieved during the first iteration.

def do_get_request(api, params={}):
    """Perform a get request to Telegram"""

    r = requests.get(API_BASE + api, params)
    return r.text

def send_message(msg, reply_to=""):
    """Send a message to the group the latest update came from"""
    do_get_request("sendMessage", params={"chat_id": GROUP_ID, "text": msg, "reply_to_message_id": reply_to})

def fetch_image_url(query):
    """Download a random image from Google image search."""
    BASE_URL = 'https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=' + query + '&start=%d&rsz=8'
    start = random.randint(0, 56)  # Take a random number for google pagination. Max is 56 when rsz is 8.

    try:
        r = requests.get(BASE_URL % start)
        image = json.loads(r.text)['responseData']['results'][random.randint(0, 7)]  # Take a random picture out of the 8 available.
        url = image['unescapedUrl']

    except:
        url = ""
        send_message("Nessuna immagine trovata :(", reply_to=message["message"]["message_id"])

    return url

def show_help():
    msg = """Il bot del FermoLUG - versione %s\n\nComandi disponibili:\n/milf <numero>: mostra <numero> foto random di MILF (massimo 5)\n/cameltoe: mostra una foto random di cameltoe\n/rustelle: mostra una foto random di rustelle\n/image <stringa>: Cerca <stringa> su google images e restituisce un risultato casuale\n/wiki <nome_pagina>: Genera un link alla pagina del wiki del LUG\n\nQuesto software è Software Libero: https://github.com/warp10/fermolugbot""" % str(BOT_VERSION)
    send_message(msg)

def send_image(query, iterations=1):
    if query:
        iterations = 5 if iterations > 5 else iterations
        for iteration in range(iterations):
            url = fetch_image_url(query)
            send_message(url)

def send_wiki_url(query):
    if query:
        url = "http://wiki.linuxfm.org/doku.php?id=" + query
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
                continue

            if message_text.startswith("@FermoLUGbot"):
                message_text = message_text[len("@FermoLUGbot "):]

            if message_text.lower().startswith("/milf"):
                try:
                    iterations = int(message_text[len("/milf "):])
                except:
                    iterations = 1
                send_image("milf", iterations)
            elif message_text.lower().startswith("/cameltoe"):
                send_image("cameltoe")
            elif message_text.lower().startswith("/rustelle"):
                send_image("arrosticini")
            elif message_text.lower().startswith("/help"):
                show_help()
            elif message_text.lower().startswith("/image"):
                send_image(message_text[len("/image "):])
            elif message_text.lower().startswith("/wiki"):
                send_wiki_url(message_text[len("/wiki "):])
            elif message_text.lower().startswith("/braccecorte"):
                send_message("@pxel_tk e cacciali 'sti cazzo di soldi!")
            else:
                send_message("Tsk tsk, RTFM!", reply_to=message["message"]["message_id"])

        sleep(1)
