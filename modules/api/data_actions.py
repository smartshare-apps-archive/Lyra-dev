import ast, re

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

import numpy as np
import json 


dataActions = Blueprint('dataActions', __name__, template_folder='templates')


@dataActions.before_request
def setup_session():
	sm = current_app.config['SessionManager']
	s_id = current_app.config['session_cookie_id']

	if s_id not in session:
		sm.open_session(current_app, session)
		print "Created: ", session[s_id]




@dataActions.route('/actions/test_endpoint', methods=['GET'])
#@admin_required(current_app, session, login_redirect)
def getSampleData():
	
	a = np.arange(10).reshape(2,5) # a 2 by 5 array
	b = a.tolist() # nested lists with same data, indices
	
	return json.dumps(b)



