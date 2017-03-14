import json, time

from flask import Blueprint, render_template, abort, current_app, session, request, Markup

#ecomm module imports
from modules.db import *
from modules.decorators import *
from modules.auth.login import *
import modules.database.order


customer_routes = Blueprint('customer_routes', __name__, template_folder='templates')		#blueprint definition

@customer_routes.before_request
def setup_session():
	sm = current_app.config['SessionManager']
	s_id = current_app.config['session_cookie_id']

	if s_id not in session:
		sm.open_session(current_app, session)
		print "Created: ", session[s_id]


@customer_routes.route('/control/customers')
@customer_routes.route('/control/customers/')
#@admin_required(current_app, session, login_redirect)
def customers():
	ctl = current_app.config["ctl"]
	data = {}

	data["current_page"] = "customers"
	data["current_class_js"] = "control_panel/customer/Core.js"
	data["current_page_js"] = "control_panel/customer/Main.js"
	data["current_requests_js"] = "control_panel/customer/Requests.js"

	data["current_page_content"] = ctl.render_tab("customers")
	data["ts"] = int(time.time())
	data["modal"] = Markup(render_template("control_panel/modal.html"))
	data["submenu"] = Markup(render_template("control_panel/subMenu_customers.html"))

	return render_template("control_panel/control.html", data=data)





#route to single customer editor
@customer_routes.route('/control/customers/<customer_id>', methods=['GET', 'POST'])
@customer_routes.route('/control/customers/<customer_id>/', methods=['GET', 'POST'])
#@admin_required(current_app, session, login_redirect)
def customerEditor(customer_id):
	ctl = current_app.config["ctl"]
	data = {}

	data["current_page"] = "order_editor"
	data["current_class_js"] = "control_panel/customer/Core.js"
	data["current_page_js"] = "control_panel/customer/CustomerEditor.js"
	data["current_requests_js"] = "control_panel/customer/Requests.js"

	data["current_page_content"] = ctl.render_tab("customer_editor", data=customer_id)
	data["ts"] = int(time.time())
	data["modals"] = [render_template("control_panel/modal.html")]
	data["submenu"] = Markup(render_template("control_panel/subMenu_customers.html"))

	return render_template("control_panel/control.html", data=data)

