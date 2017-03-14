import json, ast, re

from flask import Blueprint, render_template, abort, current_app, session, request

#ecomm module imports
from modules.db import *
import modules.database.config
import modules.database.product as product
import modules.database.resources as resources
import modules.database.customer
from modules.decorators import *
from modules.auth.login import *


searchActions = Blueprint('searchActions', __name__, template_folder='templates')


@searchActions.before_request
def setup_session():
	sm = current_app.config['SessionManager']
	s_id = current_app.config['session_cookie_id']

	if s_id not in session:
		sm.open_session(current_app, session)
		print "Created: ", session[s_id]



@searchActions.route('/actions/filterProducts', methods=['POST'])
##@admin_required(current_app, session, login_redirect)
def filterProducts():
	searchTerm = request.form['searchTerm']
	searchFilter = request.form['searchFilter']

	searchTerm = (json.loads(searchTerm))["input"].lower()

	productData = request.form['productData']
	productData = json.loads(productData)

	if searchTerm == "":
		return json.dumps([product_id for product_id, product in productData.iteritems()])

	searchFilter = (json.loads(searchFilter))["filter"]

	#print "SEARCH FILTER: ", searchFilter

	#these search regex need to be improved, but they work for basic searches
	if searchFilter == "Title":
		searchRE = re.compile('.?'+searchTerm+'.?', flags = re.DOTALL)
	elif searchFilter == "Tags":
		searchRE = re.compile('.?'+searchTerm+'.?', flags = re.DOTALL)
	elif searchFilter == "Vendor":
		searchRE = re.compile('.?'+searchTerm+'.?', flags = re.DOTALL)


	matchIDList = []
	for product_id, product in productData.iteritems():
		product = ast.literal_eval(product)

		if searchFilter == "Title":
			search_field = product["Title"].lower()

		elif searchFilter == "Tags":
			if product["Tags"]:
				search_field = product["Tags"].lower()
			else:
				continue
		elif searchFilter == "Vendor":
			if product["Vendor"]:
				search_field = product["Vendor"].lower()
			else:
				continue
			

		m = re.search(searchRE, search_field)
		
		if m:
			#print "	MATCH: ", currentTitle, ":", searchTerm
			matchIDList.append(str(product["product_id"]))

		#print "MATCH LIST: ", matchIDList

	return json.dumps(matchIDList)




@searchActions.route('/actions/filterOrders', methods=['POST'])
##@admin_required(current_app, session, login_redirect)
def filterOrders():
	searchTerm = request.form['searchTerm']
	searchFilter = request.form['searchFilter']

	searchTerm = (json.loads(searchTerm))["input"].lower()

	orderData = request.form['orderData']
	orderData = json.loads(orderData)

	if searchTerm == "":
		return json.dumps([order_id for order_id, order in orderData.iteritems()])

	searchFilter = (json.loads(searchFilter))["filter"]

	print "SEARCH FILTER: ", searchFilter

	#these search regex need to be improved, but they work for basic searches
	if searchFilter == "order_id":
		searchRE = re.compile('.?'+searchTerm+'.?', flags = re.DOTALL)
	elif searchFilter == "customer_name":
		searchRE = re.compile('.?'+searchTerm+'.?', flags = re.DOTALL)


	matchIDList = []
	for order_id, order in orderData.iteritems():
		order = ast.literal_eval(order)

		if searchFilter == "order_id":
			search_field = str(order["order_id"])

		elif searchFilter == "customer_name":
			search_field = (order["ShippingFirstName"] + " " + order["ShippingLastName"]).lower()


		m = re.search(searchRE, search_field)
		
		if m:
			matchIDList.append(str(order["order_id"]))


	return json.dumps(matchIDList)




@searchActions.route('/actions/filterCustomers', methods=['POST'])
##@admin_required(current_app, session, login_redirect)
def filterCustomers():
	searchTerm = request.form['searchTerm']
	searchFilter = request.form['searchFilter']

	searchTerm = (json.loads(searchTerm))["input"].lower()

	customerData = request.form['customerData']
	customerData = json.loads(customerData)

	if searchTerm == "":
		return json.dumps([customer_id for customer_id, customer in customerData.iteritems()])

	searchFilter = (json.loads(searchFilter))["filter"]

	print "SEARCH FILTER: ", searchFilter

	#these search regex need to be improved, but they work for basic searches
	if searchFilter == "customer_id":
		searchRE = re.compile('.?'+searchTerm+'.?', flags = re.DOTALL)
	elif searchFilter == "customer_name":
		searchRE = re.compile('.?'+searchTerm+'.?', flags = re.DOTALL)


	matchIDList = []
	for customer_id, customer in customerData.iteritems():
		customer = ast.literal_eval(customer)

		if searchFilter == "customer_id":
			search_field = str(customer["customer_id"])

		elif searchFilter == "customer_name":
			search_field = (customer["ShippingFirstName"] + " " + customer["ShippingLastName"]).lower()


		m = re.search(searchRE, search_field)
		
		if m:
			matchIDList.append(str(customer["customer_id"]))


	return json.dumps(matchIDList)
