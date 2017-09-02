import json, time

from flask import Blueprint, render_template, abort, current_app, session, request, Markup

# ecomm module imports
from modules.db import *
from modules.decorators import *
from modules.auth.login import *
import modules.database.order as order

store_settings_routes = Blueprint('store_settings_routes', __name__,
                                  template_folder='templates')  # blueprint definition


@store_settings_routes.before_request
def setup_session():
    sm = current_app.config['SessionManager']
    s_id = current_app.config['session_cookie_id']

    if s_id not in session:
        sm.open_session(current_app, session)
        print "Created: ", session[s_id]


@store_settings_routes.route('/control/store')
@store_settings_routes.route('/control/store/')
# @admin_required(current_app, session, login_redirect)
def store_settings():
    ctl = current_app.config["ctl"]
    data = {}

    data["current_page"] = "store_settings"
    data["current_class_js"] = "control_panel/store/Core.js"
    data["current_page_js"] = "control_panel/store/Main.js"
    data["current_requests_js"] = "control_panel/store/Requests.js"

    response = ctl.render_tab("store_settings")

    if response in config.ERROR_CODES:
        return redirect(url_for('settings_routes.advanced_settings', flag="NO_DB"))
    else:
        data["current_page_content"] = response

    data["ts"] = int(time.time())
    data["modal"] = Markup(render_template("control_panel/modal.html"))
    data["submenu"] = Markup(render_template("control_panel/subMenu_store_settings.html"))

    return render_template("control_panel/control.html", data=data)


@store_settings_routes.route('/control/store/navigation')
@store_settings_routes.route('/control/store/navigation/')
# @admin_required(current_app, session, login_redirect)
def store_settings_navigation():
    ctl = current_app.config["ctl"]
    data = {}

    data["current_page"] = "store_settings_navigation"
    data["current_class_js"] = "control_panel/store/Core.js"
    data["current_page_js"] = "control_panel/store/Navigation.js"
    data["current_requests_js"] = "control_panel/store/Requests.js"

    response = ctl.render_tab("store_settings_navigation")

    if response in config.ERROR_CODES:
        return redirect(url_for('settings_routes.advanced_settings', flag="NO_DB"))
    else:
        data["current_page_content"] = response

    data["ts"] = int(time.time())
    data["modal"] = Markup(render_template("control_panel/modal.html"))
    data["submenu"] = Markup(render_template("control_panel/subMenu_store_settings.html"))

    return render_template("control_panel/control.html", data=data)


@store_settings_routes.route('/control/store/footer')
@store_settings_routes.route('/control/store/footer/')
# @admin_required(current_app, session, login_redirect)
def store_settings_footer():
    ctl = current_app.config["ctl"]
    data = {}

    data["current_page"] = "store_settings_footer"
    data["current_class_js"] = "control_panel/store/Core.js"
    data["current_page_js"] = "control_panel/store/Footer.js"
    data["current_requests_js"] = "control_panel/store/Requests.js"

    response = ctl.render_tab("store_settings_footer")

    if response in config.ERROR_CODES:
        return redirect(url_for('settings_routes.advanced_settings', flag="NO_DB"))
    else:
        data["current_page_content"] = response

    data["ts"] = int(time.time())
    data["modal"] = Markup(render_template("control_panel/modal.html"))
    data["submenu"] = Markup(render_template("control_panel/subMenu_store_settings.html"))

    return render_template("control_panel/control.html", data=data)


@store_settings_routes.route('/control/store/pages')
@store_settings_routes.route('/control/store/pages/')
# @admin_required(current_app, session, login_redirect)
def store_settings_pages():
    ctl = current_app.config["ctl"]
    data = {}

    data["current_page"] = "store_settings_pages"
    data["current_class_js"] = "control_panel/store/Core.js"
    data["current_page_js"] = "control_panel/store/Pages.js"
    data["current_requests_js"] = "control_panel/store/Requests.js"

    response = ctl.render_tab("store_settings_pages")

    if response in config.ERROR_CODES:
        return redirect(url_for('settings_routes.advanced_settings', flag="NO_DB"))
    else:
        data["current_page_content"] = response

    data["ts"] = int(time.time())
    data["modal"] = Markup(render_template("control_panel/modal.html"))
    data["submenu"] = Markup(render_template("control_panel/subMenu_store_settings.html"))

    return render_template("control_panel/control.html", data=data)


@store_settings_routes.route('/control/store/pages/<string:page_id>')
@store_settings_routes.route('/control/store/pages/<string:page_id>/')
# @admin_required(current_app, session, login_redirect)
def store_settings_page_editor(page_id):
    ctl = current_app.config["ctl"]
    data = {}

    data["current_page"] = "store_settings_page_editor"
    data["current_class_js"] = "control_panel/store/Core.js"
    data["current_page_js"] = "control_panel/store/PageEditor.js"
    data["current_requests_js"] = "control_panel/store/Requests.js"

    response = ctl.render_tab("store_settings_page_editor", page_id)

    if response in config.ERROR_CODES:
        return redirect(url_for('settings_routes.advanced_settings', flag="NO_DB"))
    else:
        data["current_page_content"] = response

    data["ts"] = int(time.time())
    data["modal"] = Markup(render_template("control_panel/modal.html"))
    data["submenu"] = Markup(render_template("control_panel/subMenu_store_settings.html"))

    return render_template("control_panel/control.html", data=data)


@store_settings_routes.route('/control/store/file_manager')
@store_settings_routes.route('/control/store/file_manager/')
# @admin_required(current_app, session, login_redirect)
def store_settings_file_manager():
    ctl = current_app.config["ctl"]
    data = {}

    data["current_page"] = "store_settings_file_manager"
    data["current_class_js"] = "control_panel/store/Core.js"
    data["current_page_js"] = "control_panel/store/FileManager.js"
    data["current_requests_js"] = "control_panel/store/Requests.js"

    response = ctl.render_tab("store_settings_file_manager")

    if response in config.ERROR_CODES:
        return redirect(url_for('settings_routes.advanced_settings', flag="NO_DB"))
    else:
        data["current_page_content"] = response

    data["ts"] = int(time.time())
    data["modal"] = Markup(render_template("control_panel/modal.html"))
    data["submenu"] = Markup(render_template("control_panel/subMenu_store_settings.html"))

    return render_template("control_panel/control.html", data=data)


@store_settings_routes.route('/control/store/theme_manager')
@store_settings_routes.route('/control/store/theme_manager/')
# @admin_required(current_app, session, login_redirect)
def store_settings_theme_manager():
    ctl = current_app.config["ctl"]
    data = {}

    data["current_page"] = "store_settings_theme_manager"
    data["current_class_js"] = "control_panel/store/Core.js"
    data["current_page_js"] = "control_panel/store/ThemeManager.js"
    data["current_requests_js"] = "control_panel/store/Requests.js"

    response = ctl.render_tab("store_settings_theme_manager")

    if response in config.ERROR_CODES:
        return redirect(url_for('settings_routes.advanced_settings', flag="NO_DB"))
    else:
        data["current_page_content"] = response

    data["ts"] = int(time.time())
    data["modal"] = Markup(render_template("control_panel/modal.html"))
    data["submenu"] = Markup(render_template("control_panel/subMenu_store_settings.html"))

    return render_template("control_panel/control.html", data=data)


@store_settings_routes.route('/control/store/analytics')
@store_settings_routes.route('/control/store/analytics/')
# @admin_required(current_app, session, login_redirect)
def store_settings_analytics():
    ctl = current_app.config["ctl"]
    data = {}

    data["current_page"] = "store_settings_analytics"
    data["current_class_js"] = "control_panel/store/Core.js"
    data["current_page_js"] = "control_panel/store/Analytics.js"
    data["current_requests_js"] = "control_panel/store/Requests.js"

    response = ctl.render_tab("store_settings_analytics")

    if response in config.ERROR_CODES:
        return redirect(url_for('settings_routes.advanced_settings', flag="NO_DB"))
    else:
        data["current_page_content"] = response

    data["ts"] = int(time.time())
    data["modal"] = Markup(render_template("control_panel/modal.html"))
    data["submenu"] = Markup(render_template("control_panel/subMenu_store_settings.html"))

    return render_template("control_panel/control.html", data=data)
