#!/usr/bin/env python

from cleverbot import Cleverbot
import subprocess
import sqlite3
import time
import sys

# Put path to the db containing past messages here
conn = sqlite3.connect("/Users/ADaley/Library/Messages/chat.db")

cur = conn.cursor()

cb = Cleverbot()

# Friend's name and phone number that the bot will autoreply to
friend = sys.argv[1] if len(sys.argv) >= 3 else "Default Name"
phone  = sys.argv[2] if len(sys.argv) >= 3 else "+19998887777"
print(friend)
print(phone)

# sends msg over Messages application to the specified 'phone'
def send(msg):
    cmd = u'''tell application "Messages" to send "{}" to buddy "{}" of (service 1 whose service type is iMessage)'''.format(msg, phone)
    process = subprocess.Popen(['osascript', '-e', cmd], stdout=subprocess.PIPE)
    output, error = process.communicate()

# returns a 2D array where 1st index gives a db tuple (is_from_me, text, date) 
#   and the 2nd indexes into that tuple. The function returns a max of 3 tuples
def getMostRecent():
    cur.execute("""select is_from_me,text,date from message where handle_id=( select handle_id from chat_handle_join where chat_id=( select ROWID from chat where guid='iMessage;-;{}') ) order by date desc limit 3""".format(phone))
    rows = cur.fetchall()
    return rows

# returns the concatenation of multiple received msgs.
def combineReceivedMsgs(msgs):
    msg = msgs[0][1]
    i = 1
    while i < len(msgs) and msgs[i][0] == 0:
        msg = msgs[i][1] + '. ' + msg
        i += 1
    return msg

while (True):
    print("tick")
    msgs = getMostRecent()
    if msgs and msgs[0][0] == 0: # most recent msg is from other person
        msg = combineReceivedMsgs(msgs)
        print("Last message: " + msg)
        try:
            resp = cb.ask(msg).encode('utf8').replace(u'.', u'').replace(',', '').lower()
            print("Cleverbot response: " + resp)
            send(resp)
        except:
            cb = Cleverbot()
    time.sleep(60)
