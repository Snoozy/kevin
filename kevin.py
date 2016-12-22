#!/usr/bin/env python

from cleverbot import Cleverbot
import subprocess
import sqlite3
import time

conn = sqlite3.connect("/Users/dli/Library/Messages/chat.db")

cur = conn.cursor()

cb = Cleverbot()

friend = "Andrew J Daley"
phone = "+17039154898"
last_msg = None

def send(msg):
    cmd = u'''tell application "Messages" to send "{}" to buddy "{}" of (service 1 whose service type is iMessage)'''.format(msg, phone)
    process = subprocess.Popen(['osascript', '-e', cmd], stdout=subprocess.PIPE)
    output, error = process.communicate()

def getMostRecent():
    cur.execute("""select is_from_me,text,date from message where handle_id=( select handle_id from chat_handle_join where chat_id=( select ROWID from chat where guid='iMessage;-;{}') ) and is_from_me = 0 order by date desc limit 1""".format(phone))
    rows = cur.fetchall()
    return rows[0][1]

while (True):
    print("tick")
    msg = getMostRecent()
    print(msg)
    if not last_msg or last_msg != msg:
        try:
            resp = cb.ask(msg).encode('utf8').replace(u'.', u'').replace(',', '').lower()
            print(resp)
            send(resp)
            last_msg = msg
        except:
            cb = Cleverbot()
    time.sleep(5)
