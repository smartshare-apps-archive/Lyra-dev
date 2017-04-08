import sys,csv,json,collections

#config current only has column/field mapping information, which will be specific to the import form (of the product csv), e.g. shopify
from config import *	
from customer import *
from event import *
import product
from product_util import *
from order_util import *

import shippo

def loadOrderShipments(orderID, database):
	currentQuery = "SELECT shipment_id,order_id,TrackingNumber,ShipmentDate,Carrier,SKU_List FROM shipping WHERE order_id=%s;"

	try:
		database.execute(currentQuery,(orderID,))
	except Exception as e:
		return None

	order_shipments = database.fetchall()

	if order_shipments:
		formattedShipmentData = {}
		for i in range(len(order_shipments)):
			currentShipmentID = str(order_shipments[i][0])
			formattedShipmentData[currentShipmentID] = {}

			for j in range(len(shipmentColumnMappings)):
				formattedShipmentData[currentShipmentID][shipmentColumnMappings[j]] = order_shipments[i][j]
			return formattedShipmentData	
	else:
		return None


