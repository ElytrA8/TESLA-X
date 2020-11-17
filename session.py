#!/usr/bin/env python3
# -*- coding: utf-8-*-
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
print(
    "go to my.telegram.org, sign in, click on api development tools. copy API_ID and API_HASH then come back here."
)
API_ID = int(input("enter the API_ID: "))
API_HASH = input("enter the API_HASH: ")
with TelegramClient(StringSession(), API_ID, API_HASH) as client:
	print(
	    "Check your Telegram Saved Messages to copy the STRING_SESSION value")
	session_str = client.session.save()
	msg = client.send_message("me", session_str)
	msg.reply("made by the Project TESLA-X Program")

print("all done,\n now check your telegram saved messages!")
