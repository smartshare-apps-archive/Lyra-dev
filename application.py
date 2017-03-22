from __future__ import print_function 
import os, sys, re, requests, prices, time, json

reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask, render_template, url_for, abort, request, Response, make_response, g, current_app, session

#module imports 
from modules.database.product import *
from modules.control_views import *
from modules.store_views import *
from modules.auth_views import *
from modules.db import *


#api endpoints
from modules.api import product_actions
from modules.api import resource_actions
from modules.api import settings_actions
from modules.api import store_actions
from modules.api import order_actions
from modules.api import customer_actions
from modules.api import search_actions

#control panel rendering sections, which route to specific parts of the control panel
from modules.control_panel import products
from modules.control_panel import orders
from modules.control_panel import customers
from modules.control_panel import store_settings
from modules.control_panel import settings


#store rendering sections
from modules.store import store
from modules.store import cart

from modules.payment import payment

#authentication and session management modules
from modules.auth import login
from modules.auth import session_manager


application = Flask(__name__)
application.config['ctl'] = ControlPanel()		#this instance of ControlPanel can be accessed through the application context so blueprints can use it
application.config['store_ctl'] = Store()		#this instance of Store can be accessed through the application context so blueprints can use it
application.config['auth_ctl'] = Auth()		#this instance of Store can be accessed through the application context so blueprints can use it
application.config['IMAGE_UPLOAD_FOLDER'] = 'static/images/'
application.config['FILE_UPLOAD_FOLDER'] = 'static/uploaded_files/'


#jinja2 configuration options
application.jinja_env.trim_blocks = True
application.jinja_env.lstrip_blocks = True

#generate a random secret key
application.secret_key = os.urandom(24)

#register blueprints
application.register_blueprint(product_actions.productActions)
application.register_blueprint(settings_actions.settingsActions)
application.register_blueprint(store_actions.storeActions)
application.register_blueprint(order_actions.orderActions)
application.register_blueprint(customer_actions.customerActions)
application.register_blueprint(resource_actions.resourceActions)
application.register_blueprint(search_actions.searchActions)

#register control panel blueprints
application.register_blueprint(products.product_routes)
application.register_blueprint(orders.order_routes)
application.register_blueprint(customers.customer_routes)
application.register_blueprint(settings.settings_routes)
application.register_blueprint(store_settings.store_settings_routes)

#register store blueprints
application.register_blueprint(store.store_routes)
application.register_blueprint(login.login_routes)
application.register_blueprint(payment.payment_routes)


#initialize store wide session and cart manager
application.config['session_cookie_id'] = 'user_session'
application.config['SessionManager'] = session_manager.SessionManager()

assert application.config['SessionManager'].r is not None, "Can't connect to redis server."

#cart needs access to session interface instance
application.config['CartManager'] = cart.CartManager(application, application.config['SessionManager'])


#only for debugging, makes sure to check all the js files and templates for changes
def debug_dirUpdate():
	extra_dirs = ['templates/','static/js/']
	extra_files = extra_dirs[:]
	for extra_dir in extra_dirs:
	    for dirname, dirs, files in os.walk(extra_dir):
	        for filename in files:
	            filename = os.path.join(dirname, filename)
	            if os.path.isfile(filename):
	                extra_files.append(filename)
	return extra_files



if __name__ == "__main__":
	extra_files = debug_dirUpdate()

	#live_host = "0.0.0.0"
	#live_host = "127.0.0.1"

	application.run(debug=True, extra_files=extra_files, threaded=True)