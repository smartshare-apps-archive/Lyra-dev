import sqlite3,sys,csv,json,collections

#config current only has column/field mapping information, which will be specific to the import form (of the product csv), e.g. shopify
from config import *	
from customer import *
from event import *
import product
from product_util import *
from order_util import *

def loadOrder(orderID, database):
	currentQuery = """SELECT order_id,Date,customer_id,PaymentInfo,PaymentStatus,FulfillmentStatus,SKU_List,SKU_Fulfilled,OrderTotal,TaxTotal,ShippingTotal,SubTotal,OrderEvents,Currency,ShippingAddress,ShippingAddress2,ShippingCity,ShippingPostalCode,ShippingCountry,Company,
					ShippingFirstName,ShippingLastName,Email,ShippingState,PhoneNumber,Note,BillingAddress,BillingAddress2,BillingCity,BillingPostalCode,BillingCountry,BillingFirstName,BillingLastName,BillingState,token_id,charge_id,order_creation_method FROM orders WHERE order_id = ?;"""
	
	try:
		database.execute(currentQuery,(orderID,))
	except Exception as e:
		return None

	order = database.fetchone()

	
	if order:
		formattedOrderData = {}
		for i in range(len(orderColumnMappings)):
			formattedOrderData[orderColumnMappings[i]] = order[i]
		return formattedOrderData
	else:
		return None




def loadOrderByToken(tokenID, database):
	currentQuery = """SELECT order_id,Date,customer_id,PaymentInfo,PaymentStatus,FulfillmentStatus,SKU_List,SKU_Fulfilled,OrderTotal,TaxTotal,ShippingTotal,SubTotal,OrderEvents,Currency,ShippingAddress,ShippingAddress2,ShippingCity,ShippingPostalCode,ShippingCountry,Company,
					ShippingFirstName,ShippingLastName,Email,ShippingState,PhoneNumber,Note,BillingAddress,BillingAddress2,BillingCity,BillingPostalCode,BillingCountry,BillingFirstName,BillingLastName,BillingState,token_id,charge_id,order_creation_method FROM orders WHERE token_id = ?;"""
	
	try:
		database.execute(currentQuery,(tokenID,))
	except Exception as e:
		return None

	order = database.fetchone()

	if order:
		formattedOrderData = {}
		for i in range(len(orderColumnMappings)):
			formattedOrderData[orderColumnMappings[i]] = order[i]

		return formattedOrderData



def loadOrderByCharge(chargeID, database):
	currentQuery = """SELECT order_id,Date,customer_id,PaymentInfo,PaymentStatus,FulfillmentStatus,SKU_List,SKU_Fulfilled,OrderTotal,TaxTotal,ShippingTotal,SubTotal,OrderEvents,Currency,ShippingAddress,ShippingAddress2,ShippingCity,ShippingPostalCode,ShippingCountry,Company,
					ShippingFirstName,ShippingLastName,Email,ShippingState,PhoneNumber,Note,BillingAddress,BillingAddress2,BillingCity,BillingPostalCode,BillingCountry,BillingFirstName,BillingLastName,BillingState,token_id,charge_id,order_creation_method FROM orders WHERE charge_id = ?;"""
	
	try:
		database.execute(currentQuery,(chargeID,))
	except Exception as e:
		return None

	order = database.fetchone()

	if order:
		formattedOrderData = {}
		for i in range(len(orderColumnMappings)):
			formattedOrderData[orderColumnMappings[i]] = order[i]

		return formattedOrderData



#load all the products in an order
def loadOrderProducts(SKU_List, database):
	products = {}
	
	SKU_List = [SKU.split(';') for SKU in SKU_List.split(',')]
	
	for SKU in SKU_List:
		productQuantity = SKU[1] 			#SKU[1] is the product quantity

		currentProduct = product.loadProductBySKU(SKU[0], database)
		currentProduct["quantity"] = productQuantity
		products[currentProduct["product_id"]] = currentProduct

	return products



def loadAllOrders(database):
	formattedOrderList = collections.OrderedDict()

	currentQuery = """SELECT order_id,Date,customer_id,PaymentInfo,PaymentStatus,FulfillmentStatus,SKU_List,SKU_Fulfilled,OrderTotal,TaxTotal,ShippingTotal,SubTotal,OrderEvents,Currency,ShippingAddress,ShippingAddress2,ShippingCity,ShippingPostalCode,ShippingCountry,Company,
					ShippingFirstName,ShippingLastName,Email,ShippingState,PhoneNumber,Note,BillingAddress,BillingAddress2,BillingCity,BillingPostalCode,BillingCountry,BillingFirstName,BillingLastName, BillingState,token_id,charge_id,order_creation_method FROM orders ORDER BY order_id DESC;"""
	
	try:
		database.execute(currentQuery)
	except Exception as e:
		print "Exception:", e
		return None

	orderList = database.fetchall()

	if orderList:
		for i in range(len(orderList)):
			currentOrderID = str(orderList[i][0])
			formattedOrderList[currentOrderID] = {}

			for j in range(len(orderColumnMappings)):
				formattedOrderList[currentOrderID][orderColumnMappings[j]] = orderList[i][j]

		return formattedOrderList




def loadAllDraftOrders(database):
	formattedOrderList = collections.OrderedDict()

	currentQuery = """SELECT order_id,Date,customer_id,PaymentInfo,PaymentStatus,FulfillmentStatus,SKU_List,SKU_Fulfilled,OrderTotal,TaxTotal,ShippingTotal,SubTotal,OrderEvents,Currency,ShippingAddress,ShippingAddress2,ShippingCity,ShippingPostalCode,ShippingCountry,Company,
					ShippingFirstName,ShippingLastName,Email,ShippingState,PhoneNumber,Note,BillingAddress,BillingAddress2,BillingCity,BillingPostalCode,BillingCountry,BillingFirstName,BillingLastName, BillingState,token_id,charge_id,order_creation_method FROM orders WHERE order_creation_method="manual" ORDER BY order_id DESC;"""
	
	try:
		database.execute(currentQuery)
	except Exception as e:
		print "Exception:", e
		return None

	orderList = database.fetchall()

	if orderList:
		for i in range(len(orderList)):
			currentOrderID = str(orderList[i][0])
			formattedOrderList[currentOrderID] = {}

			for j in range(len(orderColumnMappings)):
				formattedOrderList[currentOrderID][orderColumnMappings[j]] = orderList[i][j]

		return formattedOrderList



def loadCustomerOrders(customer_id, database):
	formattedOrderList = collections.OrderedDict()

	currentQuery = """SELECT order_id,Date,customer_id,PaymentInfo,PaymentStatus,FulfillmentStatus,SKU_List,SKU_Fulfilled,OrderTotal,TaxTotal,ShippingTotal,SubTotal,OrderEvents,Currency,ShippingAddress,ShippingAddress2,ShippingCity,ShippingPostalCode,ShippingCountry,Company,
	ShippingFirstName,ShippingLastName,Email,ShippingState,PhoneNumber,Note,BillingAddress,BillingAddress2,BillingCity,BillingPostalCode,BillingCountry,BillingFirstName,BillingLastName,BillingState,token_id,charge_id,order_creation_method FROM orders WHERE customer_id = ? ORDER BY order_id DESC; """
	

	try:
		database.execute(currentQuery, (customer_id, ))
	except Exception as e:
		print "Error: ", e
		return None

	orderList = database.fetchall()

	if orderList:
		for i in range(len(orderList)):
			currentOrderID = str(orderList[i][0])
			formattedOrderList[currentOrderID] = {}

			for j in range(len(orderColumnMappings)):
				formattedOrderList[currentOrderID][orderColumnMappings[j]] = orderList[i][j]

		return formattedOrderList
	else:
		return None



def createOrder(database, order_details):
	print "Order details:", order_details
	currentQuery = """INSERT into orders(Date,SKU_List,SKU_Fulfilled,OrderTotal,TaxTotal,ShippingTotal,SubTotal,ShippingAddress,ShippingAddress2,ShippingCity,ShippingPostalCode,ShippingCountry,Company,
					ShippingFirstName,ShippingLastName,Email,ShippingState,PhoneNumber,BillingAddress,BillingAddress2,BillingCity,BillingPostalCode,BillingCountry,BillingFirstName,BillingLastName, BillingState, token_id, PaymentInfo) 
					VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"""

	try:
		database.execute(currentQuery, order_details)
	except Exception as e:
		print "Exception:", e
		return None

	return True



# update order functions


def set_OrderPaymentStatus(database, token_id, payment_status):
	currentQuery = "UPDATE orders SET PaymentStatus=? WHERE token_id=?;"

	try:
		database.execute(currentQuery, (payment_status, token_id, ))
	except Exception as e:
		print e



def set_OrderChargeID(database, token_id, charge_id):
	currentQuery = "UPDATE orders SET charge_id=? WHERE token_id=?;"

	try:
		database.execute(currentQuery, (charge_id, token_id, ))
	except Exception as e:
		print e



def set_OrderCustomerID(database, token_id, customer_id):
	currentQuery = "UPDATE orders SET customer_id=? WHERE token_id=?;"

	try:
		database.execute(currentQuery, (customer_id, token_id, ))
	except Exception as e:
		print "Error: ", e
		return None



def deleteOrder(database, token_id):
	currentQuery = "DELETE FROM orders WHERE token_id=?;"
	try:
		database.execute(currentQuery, (token_id, ))
	except Exception as e:
		print e



def updateOrderFulfillment(SKU_Fulfilled, order_id, database):
	order_data = loadOrder(order_id, database)

	if (order_data["SKU_List"] == SKU_Fulfilled):
		currentQuery = """UPDATE orders SET SKU_Fulfilled=?, FulfillmentStatus="fulfilled" WHERE order_id=?;"""
		try:
			database.execute(currentQuery, (SKU_Fulfilled, order_id, ))
		except Exception as e:
			print "Error: ", e
			return False
	else:
		currentQuery = """UPDATE orders SET SKU_Fulfilled=?, FulfillmentStatus="unfulfilled" WHERE order_id=?;"""
		try:
			database.execute(currentQuery, (SKU_Fulfilled, str(order_id), ))
		except Exception as e:
			print "Error: ", e
			return False

	return True




def bulkMarkFulfillment(fulfillment_status, order_id_list, database):
	order_id_list = map(int, order_id_list)

	placeholder = '?'
	placeholders = ','.join(placeholder for unused in order_id_list)

	currentQuery = 'UPDATE orders SET FulfillmentStatus = ? WHERE order_id IN (%s);' % placeholders

	values = [fulfillment_status] + order_id_list

	try:
		database.execute(currentQuery, values)
	except Exception as e:
		print e




def bulkMarkPaymentStatus(payment_status, order_id_list, database):
	order_id_list = map(int, order_id_list)

	placeholder = '?'
	placeholders = ','.join(placeholder for unused in order_id_list)

	currentQuery = 'UPDATE orders SET PaymentStatus = ? WHERE order_id IN (%s);' % placeholders

	values = [payment_status] + order_id_list

	try:
		database.execute(currentQuery, values)
	except Exception as e:
		print e


def bulkDeleteOrders(order_id_list, database):
	order_id_list = map(int, order_id_list)

	placeholder = '?'
	placeholders = ','.join(placeholder for unused in order_id_list)

	currentQuery = 'DELETE FROM orders WHERE order_id IN (%s);' % placeholders


	try:
		database.execute(currentQuery, order_id_list)
	except Exception as e:
		print e




		