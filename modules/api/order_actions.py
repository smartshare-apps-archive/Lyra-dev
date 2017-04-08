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

	print "HEY LOADED: ", shipping_address_to

	shippo.api_key = "shippo_test_0c91f05a81b1168a9e24f494b064a3ff5be3ebff"

	address_from = {
		"name": "Shawn Ippotle",
		"street1": "215 Clayton St.",
		"city": "San Francisco",
		"state": "CA",
		"zip": "94117",
		"country": "US",
		"phone": "+1 555 341 9393",
		"email": "shippotle@goshippo.com"
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
		"weight": "2",
		"mass_unit": "lb"
	}

	shipment = shippo.Shipment.create(
	    address_from = address_from,
	    address_to = address_to,
	    parcels = [parcel],
	    async = False
	)

	rate = shipment.rates[0]

	# Purchase the desired rate. 
	transaction = shippo.Transaction.create( 
	rate=rate.object_id, 
	label_file_type="PDF", 
	async=False )

	# Retrieve label url and tracking number or error message
	if transaction.status == "SUCCESS":
		print transaction.label_url
		print transaction.tracking_number
	else:
		print transaction.messages

	db = db_handle()
	database = db.cursor()
	

	db.commit()
	db.close()

	return json.dumps(shipment)
