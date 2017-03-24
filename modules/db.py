#import sqlite3
import MySQLdb


#DEFAULT_db = "ecomm.db"
REMOTE_HOST = "smartshare-core.chpryfodqoop.us-east-1.rds.amazonaws.com"
REMOTE_PORT = 3306
USERNAME = "llom2600"
PASSWORD = "S0v1ndiv!#!"
default_db = "smartshare-site"

def db_handle():
	try:
		conn=MySQLdb.connect(host=REMOTE_HOST,port=REMOTE_PORT,user=USERNAME,passwd=PASSWORD, db=default_db, use_unicode=True, charset="utf8")
		#conn.text_factory = str
	except Exception as e:
		print "Exception connecting: ", e

	return conn
