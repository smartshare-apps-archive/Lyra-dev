import sys,csv,json,collections	

from product_util import *
from order_util import *
from dashboard_util import *

import config
import product
import event
import customer


def saveMessage(data, database):
	q = """INSERT INTO messages(type,body,timestamp,session_id,ttl) VALUES(%s,%s,%s,%s,%s);"""
	
	try:
		database.execute(q, (data["type"], data["body"], data["timestamp"], data["session_id"], data["ttl"]))
	except Exception as e:
		print "Error inserting message: ", e
		return None

