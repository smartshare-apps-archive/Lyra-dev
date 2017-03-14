import json, ast, re

from flask import Blueprint, render_template, abort, current_app, session, request


#ecomm module imports
from modules.db import *
import modules.database.config as config
import modules.database.product as product
import modules.database.resources as resources
import modules.database.customer as customer
import modules.database.order as order

from modules.decorators import *
from modules.auth.login import *


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

