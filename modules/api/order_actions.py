import json, ast, re

from flask import Blueprint, render_template, abort, current_app, session, request


#ecomm module imports
from modules.db import *
import modules.database.config as config
import modules.database.product as product
import modules.database.resources as resources
import modules.database.customer as customer
import modules.database.order as order
import modules.database.shipment as shipment

from modules.decorators import *
from modules.auth.login import *

import shippo

orderActions = Blueprint('orderActions', __name__, template_folder='templates')


@orderActions.before_request
def setup_session():
	sm = current_app.config['SessionManager']
	s_id = current_app.config['session_cookie_id']

	if s_id not in session:
		sm.open_session(current_app, session)
		print "Created: ", session[s_id]


@orderActions.route('/actions/markOrderFulfillment', methods=['POST'])
#@admin_required(current_app, session, login_redirect)
def markOrderFulfillment():
	order_id = request.form['order_id']
	order_id = json.loads(order_id)

	sku_fulfilled = request.form['sku_fulfilled']
	sku_fulfilled = json.loads(sku_fulfilled)
	
	db = db_handle()
	database = db.cursor()
	
	order.updateOrderFulfillment(sku_fulfilled, order_id, database)

	db.commit()
	db.close()

	return json.dumps(order_id)


@orderActions.route('/actions/bulkMarkOrderFulfillment', methods=['POST'])
#@admin_required(current_app, session, login_redirect)
def bulkMarkOrderFulfillment():
	order_id_list = request.form['order_id_list']
	order_id_list = json.loads(order_id_list)

	fulfillment_status = request.form['fulfillment_status']
	fulfillment_status = json.loads(fulfillment_status)
	

	db = db_handle()
	database = db.cursor()
	
	order.bulkMarkFulfillment(fulfillment_status, order_id_list, database)

	db.commit()
	db.close()

	return json.dumps("success")



@orderActions.route('/actions/bulkMarkOrderPaymentStatus', methods=['POST'])
#@admin_required(current_app, session, login_redirect)
def bulkMarkOrderPaymentStatus():
	order_id_list = request.form['order_id_list']
	order_id_list = json.loads(order_id_list)

	payment_status = request.form['payment_status']
	payment_status = json.loads(payment_status)
	
	db = db_handle()
	database = db.cursor()
	
	order.bulkMarkPaymentStatus(payment_status, order_id_list, database)

	db.commit()
	db.close()

	return json.dumps("success")



@orderActions.route('/actions/bulkDeleteOrders', methods=['POST'])
#@admin_required(current_app, session, login_redirect)
def bulkDeleteOrders():
	order_id_list = request.form['order_id_list']
	order_id_list = json.loads(order_id_list)

	db = db_handle()
	database = db.cursor()
	
	order.bulkDeleteOrders(order_id_list, database)

	db.commit()
	db.close()

	return json.dumps("success")



#order fulfillment routes

@orderActions.route('/actions/createShipmentObject', methods=['POST'])
#@admin_required(current_app, session, login_redirect)
def createShipmentObject():
	order_id = request.form['order_id']
	order_id = json.loads(order_id)

	shipping_address_to = request.form['shipping_address_to']
	shipping_address_to = json.loads(shipping_address_to)

	shipping_address_from = request.form['shipping_address_from']
	shipping_address_from = json.loads(shipping_address_from)

	parcel_data = request.form['parcel_data']
	parcel_data = json.loads(parcel_data)

	shippo.api_key = "shippo_test_0c91f05a81b1168a9e24f494b064a3ff5be3ebff"

	print parcel_data

	address_from = {
		"name": shipping_address_from["ShippingFirstName"] + " " + shipping_address_from["ShippingLastName"],
		"street1": shipping_address_from["ShippingAddress1"],
		"city": shipping_address_from["ShippingCity"],
		"state": shipping_address_from["ShippingState"],
		"zip": shipping_address_from["ShippingPostalCode"],
		"country": shipping_address_from["ShippingCountry"],
		"phone": "+1 555 341 9393",
		"email": "mrhippo@goshippo.com"
	}

	address_to = {
		"name": shipping_address_to["ShippingFirstName"] + " " + shipping_address_to["ShippingLastName"],
		"street1": shipping_address_to["ShippingAddress"],
		"city": shipping_address_to["ShippingCity"],
		"state": shipping_address_to["ShippingState"],
		"zip": shipping_address_to["ShippingPostalCode"],
		"country": shipping_address_to["ShippingCountry"],
		"phone": "+1 555 341 9393",
		"email": "mrhippo@goshippo.com"
	}


	parcel = {
		"length": "5",
		"width": "5",
		"height": "5",
		"distance_unit": "in",
		"weight": parcel_data["Weight"],
		"mass_unit": "kg"
	}

	shipment = shippo.Shipment.create(
	    address_from = address_from,
	    address_to = address_to,
	    parcels = [parcel],
	    async = False
	)


	return json.dumps(shipment)




#order fulfillment routes

@orderActions.route('/actions/generateShippingLabel', methods=['POST'])
#@admin_required(current_app, session, login_redirect)
def generateShippingLabel():
	order_id = request.form['order_id']
	order_id = json.loads(order_id)

	shipment_obj = request.form['shipment_obj']
	shipment_obj = json.loads(shipment_obj)

	selected_option = request.form['selected_option']
	selected_option = int(json.loads(selected_option))

	

	shippo.api_key = "shippo_test_0c91f05a81b1168a9e24f494b064a3ff5be3ebff"

	#select the rate specified by the user
	rate = shipment_obj["rates"][selected_option]

	# Purchase the desired rate. 
	transaction = shippo.Transaction.create( 
	rate=rate["object_id"], 
	label_file_type="PDF", 
	async=False )

	# Retrieve label url and tracking number or error message

	shipping_label = {}

	if transaction.status == "SUCCESS":
		shipping_label["label_url"] = transaction.label_url
		shipping_label["tracking_number"] = transaction.tracking_number
	else:
		shipping_label["error_messages"] = transaction.messages



	return json.dumps(shipping_label)



@orderActions.route('/actions/saveOrderShipment', methods=['POST'])
#@admin_required(current_app, session, login_redirect)
def saveOrderShipment():
	order_id = request.form['order_id']
	order_id = json.loads(order_id)

	shipment_data = request.form['shipment_data']
	shipment_data = json.loads(shipment_data)


	db = db_handle()
	database = db.cursor()
	
	parcelData = shipment_data["parcel_data"]

	SKU_List = ""
	for field, value in parcelData.iteritems():
		if field == "Weight":
			shipment_data["Weight"] = value
		elif field == "ItemCount":
			shipment_data["ItemCount"] = value
		else:
			SKU_List += field + ":" + str(value) + ";"

	shipment_data["SKU_List"] = SKU_List

	print shipment_data

	shipment.createNewShipment(order_id, shipment_data, database)

	db.commit()
	db.close()


	return json.dumps("success")
