import json, time

from flask import Blueprint, render_template, abort, current_app, session, request, Markup

#ecomm module imports
from modules.db import *
from modules.decorators import *
from modules.auth.login import *
import modules.database.order as order


dashboard_routes = Blueprint('dashboard_routes', __name__, template_folder='templates')		#blueprint definition

@dashboard_routes.before_request
def setup_session():
	sm = current_app.config['SessionManager']
	s_id = current_app.config['session_cookie_id']

	if s_id not in session:
		sm.open_session(current_app, session)
		print "Created: ", session[s_id]


@dashboard_routes.route('/control')
@dashboard_routes.route('/control/')
#@admin_required(current_app, session, login_redirect)
def dashboard_main():
	ctl = current_app.config["ctl"]
	data = {}

	data["current_page"] = "dashboard"
	data["current_class_js"] = "control_panel/dashboard/Core.js"
	data["current_page_js"] = "control_panel/dashboard/Main.js"
	data["current_requests_js"] = "control_panel/dashboard/Requests.js"

	data["current_page_content"] = ctl.render_tab("dashboard")


	data["ts"] = int(time.time())
	data["modal"] = Markup(render_template("control_panel/modal.html"))
	data["submenu"] = Markup(render_template("control_panel/subMenu_dashboard.html"))

	return render_template("control_panel/control.html", data=data)



