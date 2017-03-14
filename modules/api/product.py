import json

from flask import Blueprint, render_template, abort, current_app, session, request

#ecomm module imports
from modules.db import *
import modules.database.config
from modules.database.product import *
from modules.decorators import *
from modules.auth.login import *

productActions = Blueprint('productActions', __name__, template_folder='templates')


@productActions.before_request
def setup_session():
	sm = current_app.config['SessionManager']
	s_id = current_app.config['session_cookie_id']

	if s_id not in session:
		sm.open_session(current_app, session)
		print "Created: ", session[s_id]


@productActions.route('/actions/bulkPublish', methods=['POST'])
#@admin_required(current_app, session, login_redirect)
def bulkAction_Publish():
	value = request.form['published']

	product_id_list = request.form['product_id_list']
	product_id_list = json.loads(product_id_list)

	db = db_handle()
	productDatabase = db.cursor()

	bulkPublish(value, product_id_list, productDatabase)

	db.commit()
	db.close()

	return json.dumps("success")



@productActions.route('/actions/bulkDelete', methods=['POST'])
#@admin_required(current_app, session, login_redirect)
def bulkAction_Delete():

	product_id_list = request.form['product_id_list']
	product_id_list = json.loads(product_id_list)

	db = db_handle()
	productDatabase = db.cursor()

	bulkDelete(product_id_list, productDatabase)

	db.commit()
	db.close()

	return json.dumps("success")



@productActions.route('/actions/bulkUpdateProducts', methods=['POST'])
#@admin_required(current_app, session, login_redirect)
def bulkAction_Update():
	productData = request.form['productData']
	productData = json.loads(productData)

	variantData = request.form['variantData']
	variantData = json.loads(variantData)

	db = db_handle()
	productDatabase = db.cursor()

	bulkUpdateProducts(productData, productDatabase)
	bulkUpdateVariants(variantData, productDatabase)

	db.commit()
	db.close()

	return json.dumps("success")



@productActions.route('/actions/bulkUpdateCollections', methods=['POST'])
#@admin_required(current_app, session, login_redirect)
def bulkAction_UpdateCollections():
	collectionData = request.form['collectionData']
	collectionData = json.loads(collectionData)

	db = db_handle()
	productDatabase = db.cursor()

	bulkUpdateCollections(collectionData, productDatabase)

	db.commit()
	db.close()

	return json.dumps("success")
