import sys, csv, json, collections

from product_util import *
from order_util import *
from dashboard_util import *

import config
import product
import event
import customer

from datetime import datetime


def saveMessage(data, database):
    q = """INSERT INTO messages(type,body,timestamp,session_id,ttl) VALUES(%s,%s,%s,%s,%s);"""

    try:
        database.execute(q, (data["type"], data["body"], data["timestamp"], data["session_id"], data["ttl"]))
    except Exception as e:
        print "Error inserting message: ", e
        return None


def getMessagesByTypeAndID(message_type, session_id, database):
    q = "SELECT COUNT(*) FROM messages WHERE type=%s AND session_id=%s;"

    try:
        database.execute(q, (message_type, session_id,))
    except Exception as e:
        print "Error retreiving messages: ", e
        return None

    count = database.fetchone()
    if count:
        count = count[0]
        return count


def getMessagesBySessionID(session_id, database):
    q = """SELECT type,body,timestamp,session_id,ttl FROM messages WHERE session_id=%s;"""

    try:
        database.execute(q, (session_id,))
    except Exception as e:
        print "Error retreiving messages: ", e
        return None

    messages = database.fetchall()
    messages = list(messages)

    if messages:
        for i, message in enumerate(messages):
            messages[i] = list(message)

    if messages:
        for i, message in enumerate(messages):
            for j, field in enumerate(message):
                if type(messages[i][j]) == datetime:
                    messages[i][j] = json_serial(messages[i][j])

    return messages


# live chat message helper functions

def getLiveChatUsers(database):
    q = """SELECT DISTINCT(session_id), timestamp, ttl FROM messages WHERE type='live_chat_init';"""

    try:
        database.execute(q)

    except Exception as e:
        print "Error retreiving users: ", e
        return None

    users = database.fetchall()
    users = list(users)

    for i, user in enumerate(users):
        users[i] = list(user)

    if users:
        for i, user in enumerate(users):
            for j, field in enumerate(user):
                if type(users[i][j]) == datetime:
                    users[i][j] = json_serial(users[i][j])

        return users


def deleteLiveChatLogs(usersToDelete, database):
    usersToDelete = [user[0] for user in usersToDelete]

    placeholders = ','.join(['%s' for _ in usersToDelete])

    q = "DELETE FROM messages WHERE session_id IN(%s)" % placeholders

    try:
        database.execute(q, usersToDelete)
    except Exception as e:
        print "Error deleting chat logs: ", e
        return False

    return True


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError("Type not serializable")
