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


customerActions = Blueprint('customerActions', __name__, template_folder='templates')


@customerActions.before_request
def setup_session():
	sm = current_app.config['SessionManager']
	s_id = current_app.config['session_cookie_id']

	if s_id not in session:
		sm.open_session(current_app, session)
		print "Created: ", session[s_id]




@customerActions.route('/actions/bulkDeleteCustomers', methods=['POST'])
#@admin_required(current_app, session, login_redirect)
def bulkDeleteCustomers():
	customer_id_list = request.form['customer_id_list']
	customer_id_list = json.loads(customer_id_list)
	
	db = db_handle()
	database = db.cursor()
	
	customer.bulkDeleteCustomers(customer_id_list, database)

	db.commit()
	db.close()

	return json.dumps("success")



