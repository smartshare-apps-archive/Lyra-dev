import json, time

from flask import Blueprint, render_template, abort, current_app, session, request, Markup


#ecomm module imports
from modules.db import *
import modules.database.order
from modules.decorators import *
from modules.auth.login import *


order_routes = Blueprint('order_routes', __name__, template_folder='templates')		#blueprint definition


@order_routes.before_request
def setup_session():
	sm = current_app.config['SessionManager']
	s_id = current_app.config['session_cookie_id']

	if s_id not in session:
		sm.open_session(current_app, session)
		print "Created: ", session[s_id]
		

		
#route to main order list
@order_routes.route('/control/orders/', methods=['GET', 'POST'])
@order_routes.route('/control/orders', methods=['GET', 'POST'])
#@admin_required(current_app, session, login_redirect)
def orders():
	ctl = current_app.config["ctl"]
	data = {}

	data["current_page"] = "orders"
	data["current_class_js"] = "control_panel/order/Core.js"
	data["current_page_js"] = "control_panel/order/Main.js"
	data["current_requests_js"] = "control_panel/order/Requests.js"


	data["current_page_content"] = ctl.render_tab("orders")
	data["ts"] = int(time.time())
	data["modals"] = [render_template("control_panel/modal.html")]
	data["submenu"] = Markup(render_template("control_panel/subMenu_orders.html"))

	return render_template("control_panel/control.html", data=data)


#route to main order list
@order_routes.route('/control/orders/drafts/', methods=['GET', 'POST'])
@order_routes.route('/control/orders/drafts', methods=['GET', 'POST'])
#@admin_required(current_app, session, login_redirect)
def orders_drafts():
	ctl = current_app.config["ctl"]
	data = {}

	data["current_page"] = "orders_drafts"
	data["current_class_js"] = "control_panel/order/Core.js"
	data["current_page_js"] = "control_panel/order/Drafts.js"
	data["current_requests_js"] = "control_panel/order/Requests.js"


	data["current_page_content"] = ctl.render_tab("orders_drafts")
	data["ts"] = int(time.time())
	data["modals"] = [render_template("control_panel/modal.html")]
	data["submenu"] = Markup(render_template("control_panel/subMenu_orders.html"))

	return render_template("control_panel/control.html", data=data)



#route to single order editor
@order_routes.route('/control/orders/<order_id>', methods=['GET', 'POST'])
@order_routes.route('/control/orders/<order_id>/', methods=['GET', 'POST'])
#@admin_required(current_app, session, login_redirect)
def orderEditor(order_id):
	ctl = current_app.config["ctl"]
	data = {}

	data["current_page"] = "order_editor"
	data["current_class_js"] = "control_panel/order/Core.js"
	data["current_page_js"] = "control_panel/order/OrderEditor.js"
	data["current_requests_js"] = "control_panel/order/Requests.js"

	data["current_page_content"] = ctl.render_tab("order_editor", data=order_id)
	data["ts"] = int(time.time())
	data["modals"] = [render_template("control_panel/modal.html")]
	data["submenu"] = Markup(render_template("control_panel/subMenu_orders.html"))

	return render_template("control_panel/control.html", data=data)


#route to single draft editor
@order_routes.route('/control/orders/addDraft', methods=['GET', 'POST'])
@order_routes.route('/control/orders/addDraft/', methods=['GET', 'POST'])
#@admin_required(current_app, session, login_redirect)
def addDraft():
	ctl = current_app.config["ctl"]
	data = {}

	data["current_page"] = "order_editor_draft_new"
	data["current_class_js"] = "control_panel/order/Core.js"
	data["current_page_js"] = "control_panel/order/DraftEditorNew.js"
	data["current_requests_js"] = "control_panel/order/Requests.js"

	data["current_page_content"] = ctl.render_tab("order_editor_draft_new")
	data["ts"] = int(time.time())
	data["modals"] = [render_template("control_panel/modal.html")]
	data["submenu"] = Markup(render_template("control_panel/subMenu_orders.html"))

	return render_template("control_panel/control.html", data=data)


#route to order fulfillment
@order_routes.route('/control/orders/fulfill/<order_id>', methods=['GET', 'POST'])
@order_routes.route('/control/orders/fulfill/<order_id>/', methods=['GET', 'POST'])
#@admin_required(current_app, session, login_redirect)
def fulfillOrder(order_id):
	ctl = current_app.config["ctl"]
	data = {}

	data["current_page"] = "order_fulfill"
	data["current_class_js"] = "control_panel/order/Core.js"
	data["current_page_js"] = "control_panel/order/Fulfill.js"
	data["current_requests_js"] = "control_panel/order/Requests.js"

	data["current_page_content"] = ctl.render_tab("order_fulfill", data=order_id)
	data["ts"] = int(time.time())
	data["modals"] = [render_template("control_panel/modal.html")]
	data["submenu"] = Markup(render_template("control_panel/subMenu_orders.html"))

	return render_template("control_panel/control.html", data=data)