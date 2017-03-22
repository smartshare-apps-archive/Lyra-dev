import sqlite3, sys, csv, json, collections

#config current only has column/field mapping information, which will be specific to the import form (of the product csv), e.g. shopify
from config import *	
from product_util import *


def auth_user(login_info, db):
	db_cursor = db.cursor()
	username = login_info['username']
	password = login_info['password']

	currentQuery = "SELECT user_id, customer_id, username, level, is_active, last_login,created_on, order_list FROM users WHERE username=%s AND password=%s;"
	
	try:
		db_cursor.execute(currentQuery,(username, password, ))
	except Exception as e:
		print "Exception: ", e

	user_data = db_cursor.fetchone()

	db.close()

	if user_data:
		formatted_user_data = {}
		for i in range(len(userColumnMappings)):
			formatted_user_data[userColumnMappings[i]] = user_data[i]
		
		return formatted_user_data
	else:
		return False


def createNewUser(db_cursor):
	currentQuery = "INSERT INTO users(username, password, customer_id, level, is_active, last_login, created_on, order_list) VALUES(%s,%s,%s,%s,%s,%s,%s,%s);"

	
def setCustomerID(user_id, customer_id, db_cursor):
	currentQuery = "UPDATE users SET customer_id=%s WHERE user_id=%s;"

	try:
		db_cursor.execute(currentQuery, (customer_id, user_id, ))
	except Exception as e:
		print "Error: ", e
		return None


def updateUserOrders(user_id, order_details, db_cursor):
	currentQuery = "SELECT order_list from users WHERE user_id=%s;"

	try:
		db_cursor.execute(currentQuery,(user_id, ))
	except Exception as e:
		print "Error: ", e
		return None
		
	order_list = db_cursor.fetchone()
	if order_list:
		order_list = order_list[0]

		if type(order_list) == type(None):
			updated_order_list = []
		else:
			updated_order_list = sorted(set(filter(lambda o: o!='', order_list.split(','))))

		order_id = str(order_details["order_id"])
		updated_order_list.append(order_id)
		updated_order_list = ",".join(updated_order_list)

		currentQuery = "UPDATE users SET order_list=%s WHERE user_id=%s;"
		try:
			db_cursor.execute(currentQuery, (updated_order_list, user_id,))
		except Exception as e:
			print "Error: ", e
			return None

		return True





