import os, stripe, datetime
from flask import Flask, render_template, request

from modules.database.product import *
import modules.database.order as order
import modules.database.config as config

from modules.db import *

db = db_handle()

#grab stripe api key settings from database
stripe_keys = config.getStripeAPIKeys(db.cursor())
stripe.api_key = stripe_keys['secret_key']


def create_order(response, order_contents, customer_info):
	order_details = []

	#format order items into sku_list for storage
	formatted_sku_list = ""
	formatted_sku_fulfillment = ""
	for sku, quantity in order_contents.iteritems():
		formatted_sku_list += (sku + ";" + quantity + ",")
		formatted_sku_fulfillment += (sku + ";" + "0" + ",")

	#calculate order_total
	subtotal = calculate_subtotal(order_contents)

	order_details.append(datetime.date.today())
	order_details.append(formatted_sku_list[:-1])
	order_details.append(formatted_sku_fulfillment[:-1])
	order_details.append(float(subtotal))
	order_details.append(0.00)
	order_details.append(0.00)
	order_details.append(float(subtotal))
	order_details.append(customer_info["ShippingAddress1"])
	order_details.append(customer_info["ShippingAddress2"])
	order_details.append(customer_info["ShippingCity"])
	order_details.append(customer_info["ShippingPostalCode"])
	order_details.append(customer_info["ShippingCountry"])
	order_details.append(customer_info["Company"])
	order_details.append(customer_info["ShippingFirstName"])
	order_details.append(customer_info["ShippingLastName"])
	order_details.append(customer_info["Email"])
	order_details.append(customer_info["ShippingState"])
	order_details.append(customer_info["Phone"])
	order_details.append(response["card"]["address_line1"])
	order_details.append(response["card"]["address_line2"])
	order_details.append(response["card"]["address_city"])
	order_details.append(response["card"]["address_zip"])
	order_details.append(response["card"]["address_country"])
	order_details.append(customer_info["BillingFirstName"])
	order_details.append(customer_info["BillingLastName"])
	order_details.append(response["card"]["address_state"])
	order_details.append(response["id"])
	order_details.append("cc:"+response["card"]["last4"])
	
	db = db_handle()

	order_id = order.createOrder(db.cursor(), order_details)

	db.commit()
	db.close()

	return response



def submit_charge(token_id):
	db = db_handle()
	order_details = loadOrderByToken(token_id, db.cursor())

	subtotal = int(order_details["SubTotal"] * 100)
	
	charge = stripe.Charge.create(
		amount=subtotal,
		currency="usd",
		description="Example charge",
		source=token_id
	)

	if charge["status"] == "succeeded":
		order.set_OrderChargeID(db.cursor(), token_id, charge["id"])
		order.set_OrderPaymentStatus(db.cursor(), token_id, "pending")
		db.commit()
		db.close()
		return charge
	else:	
		deleteOrder(db.cursor(), token_id) #deletes the order associated with this token
		db.commit()
		db.close()
		return charge



def calculate_subtotal(order_contents):
	db = db_handle()
	total_cost = 0.00

	for item_sku, quantity in order_contents.iteritems():
		try:
			quantity = float(quantity)

			productData = loadProductBySKU(item_sku, db.cursor())
			total_cost += (float(productData["VariantPrice"]) * quantity)

		except Exception as e:
			print e
	
	return total_cost



def calculate_shipping_cost(order_contents, shipping_method):
	pass



