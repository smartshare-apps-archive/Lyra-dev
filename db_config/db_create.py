import MySQLdb

REMOTE_HOST = "smartshare-core.chpryfodqoop.us-east-1.rds.amazonaws.com"
REMOTE_PORT = 3306
USERNAME = "llom2600"
PASSWORD = "S0v1ndiv!#!"

conn=MySQLdb.connect(host=REMOTE_HOST,port=REMOTE_PORT,user=USERNAME,passwd=PASSWORD)

print conn.get_host_info()

conn.close()
