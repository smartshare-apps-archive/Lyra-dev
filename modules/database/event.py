import sqlite3, sys, csv, json

# config current only has column/field mapping information, which will be specific to the import form (of the product csv), e.g. shopify
from config import *
from product import *
from customer import *


# from product_util import *


def loadEvent(eventID, productDatabase):
    currentQuery = "SELECT event_id, Time, Type, Message, Data FROM events WHERE event_id=%s";

    try:
        productDatabase.execute(currentQuery, (eventID,))
    except Exception as e:
        print e

    eventData = productDatabase.fetchone();
    if eventData:
        return eventData


def loadEvents(eventIDList, productDatabase):
    eventIDList = ','.join(str(eventID) for eventID in eventIDList)

    currentQuery = "SELECT event_id, Time, Type, Message, Data FROM events WHERE event_id IN (%s)" % eventIDList;

    try:
        productDatabase.execute(currentQuery)
    except Exception as e:
        print "Exception", e

    eventList = productDatabase.fetchall()

    if eventList:
        formattedEventList = []
        for i in range(len(eventList)):
            formattedEventList.append({})
            for j in range(len(eventColumnMappings)):
                formattedEventList[i][eventColumnMappings[j]] = eventList[i][j]

        return formattedEventList
