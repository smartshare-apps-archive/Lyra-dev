import json, time

from flask import Blueprint, render_template, abort, current_app, session, request, Markup

#ecomm module imports
from modules.db import *
from modules.decorators import *
from modules.auth.login import *
import modules.database.order


settings_routes = Blueprint('settings_routes', __name__, template_folder='templates')		#blueprint definition

@settings_routes.before_request
def setup_session():
	sm = current_app.config['SessionManager']
	s_id = current_app.config['session_cookie_id']

	if s_id not in session:
		sm.open_session(current_app, session)
		print "Created: ", session[s_id]


@settings_routes.route('/control/settings')
@settings_routes.route('/control/settings/')
#@admin_required(current_app, session, login_redirect)
def settings():
	ctl = current_app.config["ctl"]
	data = {}

	data["current_page"] = "settings"
	data["current_class_js"] = "control_panel/settings/Core.js"
	data["current_page_js"] = "control_panel/settings/Main.js"
	data["current_requests_js"] = "control_panel/settings/Requests.js"

	response = ctl.render_tab("settings")

	if response in config.ERROR_CODES:
		return redirect(url_for('settings_routes.advanced_settings', flag="NO_DB"))
	else:
		data["current_page_content"] = response

	data["ts"] = int(time.time())
	data["modal"] = Markup(render_template("control_panel/modal.html"))
	data["submenu"] = Markup(render_template("control_panel/subMenu_settings.html"))

	return render_template("control_panel/control.html", data=data)


@settings_routes.route('/control/settings/advanced')
@settings_routes.route('/control/settings/advanced/')
@settings_routes.route('/control/settings/advanced/?flag=<string:flag>')
#@admin_required(current_app, session, login_redirect)
def advanced_settings(flag = None):
	ctl = current_app.config["ctl"]
	data = {}

	data["current_page"] = "settings_advanced"
	data["current_class_js"] = "control_panel/settings/Core.js"
	data["current_page_js"] = "control_panel/settings/Advanced.js"
	data["current_requests_js"] = "control_panel/settings/Requests.js"


	response = ctl.render_tab("settings_advanced")


	if flag != None:
		data["current_page_content"] = ctl.render_tab("settings_advanced", flag)
	else:
		data["current_page_content"] = ctl.render_tab("settings_advanced")


	data["ts"] = int(time.time())
	data["modal"] = Markup(render_template("control_panel/modal.html"))
	data["submenu"] = Markup(render_template("control_panel/subMenu_settings.html"))

	return render_template("control_panel/control.html", data=data)



@settings_routes.route('/control/settings/payment')
@settings_routes.route('/control/settings/payment/')
#@admin_required(current_app, session, login_redirect)
def payment_settings():
	ctl = current_app.config["ctl"]
	data = {}

	data["current_page"] = "settings_payment"
	data["current_class_js"] = "control_panel/settings/Core.js"
	data["current_page_js"] = "control_panel/settings/PaymentSettings.js"
	data["current_requests_js"] = "control_panel/settings/Requests.js"
	
	response = ctl.render_tab("settings_payment")

	if response in config.ERROR_CODES:
		return redirect(url_for('settings_routes.advanced_settings', flag="NO_DB"))
	else:
		data["current_page_content"] = response

	data["ts"] = int(time.time())
	data["modal"] = Markup(render_template("control_panel/modal.html"))
	data["submenu"] = Markup(render_template("control_panel/subMenu_settings.html"))

	return render_template("control_panel/control.html", data=data)



