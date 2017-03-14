import json, ast, re

from flask import Blueprint, render_template, abort, current_app, session, request


#ecomm module imports
from modules.db import *
import modules.database.config as config
import modules.database.product as product
import modules.database.resources as resources
import modules.database.customer as customer

from modules.decorators import *
from modules.auth.login import *


settingsActions = Blueprint('settingsActions', __name__, template_folder='templates')


@settingsActions.before_request
def setup_session():
	sm = current_app.config['SessionManager']
	s_id = current_app.config['session_cookie_id']

	if s_id not in session:
		sm.open_session(current_app, session)
		print "Created: ", session[s_id]



@settingsActions.route('/actions/saveStripeAPIKeys', methods=['POST'])
#@admin_required(current_app, session, login_redirect)
def saveStripeAPIKeys():
	stripe_api_keys = request.form['stripe_api_keys']
	stripe_api_keys = json.loads(stripe_api_keys)
	
	db = db_handle()
	productDatabase = db.cursor()
	
	config.setStripeAPIKeys(stripe_api_keys, productDatabase)

	db.commit()
	db.close()

	return json.dumps("success")


