import json, ast, re

from flask import Blueprint, render_template, abort, current_app, session, request

#ecomm module imports
from modules.db import *
from modules.decorators import *
import modules.database.config as config
import modules.database.product as product
import modules.database.customer as customer
import modules.database.order as order
import modules.database.user as user
import modules.auth.login as login

import pay_with_stripe

payment_routes = Blueprint('payment_routes', __name__, template_folder='templates')


@payment_routes.before_request
def setup_session():
	sm = current_app.config['SessionManager']
	s_id = current_app.config['session_cookie_id']

	if s_id not in session:
		sm.open_session(current_app, session)
		print "Created: ", session[s_id]



@payment_routes.route('/charge/', methods=['POST'])
@with_user_data(current_app, session)
def chargeCard(user_data = None):
	db = db_handle()
	db_cursor = db.cursor()

	token = request.form['token_id']
	token = (json.loads(token))

	customer_info = request.form['customer_info']
	customer_info = json.loads(customer_info)

	order_details = order.loadOrderByToken(token, db.cursor())

	charge = pay_with_stripe.submit_charge(token)

	if charge["status"] == "succeeded":
		if user_data:
			#user had created an account and made one more purchases, so we just need to update
			if "customer_id" in user_data:
				customer_id = user_data["customer_id"]
				user_id = user_data["user_id"]

				customer.updateCustomer(customer_id, order_details, db_cursor)
				user.updateUserOrders(user_id, order_details, db_cursor)
				order.set_OrderCustomerID(db_cursor, token, customer_id)

			#user had created an account, but never bought anything
			else:
				user_id = user_data["user_id"]

				#create a new customer record for him, and assign that customer id to his account
				customer_info["user_id"] = user_id
				customer_id = customer.createCustomer(customer_info, order_details, db_cursor, user_data=user_data)
				
				user.setCustomerID(user_id, customer_id, db_cursor)
				customer.updateCustomer(customer_id, order_details, db_cursor)
				user.updateUserOrders(user_id, order_details, db_cursor)
				order.set_OrderCustomerID(db_cursor, token, customer_id)

		else:
			#user isn't logged in, so create a new customer for one time purchase
			customer_id = customer.createCustomer(customer_info, order_details, db_cursor)
			customer.updateCustomer(customer_id, order_details, db_cursor)
			order.set_OrderCustomerID(db_cursor, token, customer_id)

	db.commit()
	db.close()

	return json.dumps(charge)



@payment_routes.route('/create_order/', methods=['POST'])
@with_user_data(current_app, session)
def createOrder(user_data = None):
	cart = current_app.config['CartManager']
	order_contents = cart.getCartContents(session)

	response = request.form['response']
	response = (json.loads(response))

	customer_info = request.form['customer_info']
	customer_info = (json.loads(customer_info))

	if user_data:
		if "user_id" in user_data:
			print "They aren't a guest:", user_data["user_id"],":", user_data["username"]

	response = pay_with_stripe.create_order(response, order_contents, customer_info)
	
	response["customer_info"] = customer_info	#include customer info object in the response as well

	return json.dumps(response)

