import json, time

from flask import Blueprint, render_template, abort, current_app, session, request, Markup

# ecomm module imports
from modules.db import *

from modules.decorators import *
from modules.auth.login import *
import modules.database.order as order
import modules.database.config as config

dashboard_routes = Blueprint('dashboard_routes', __name__)


@dashboard_routes.before_request
def setup_session():
    sm = current_app.config['SessionManager']
    s_id = current_app.config['session_cookie_id']

    if s_id not in session:
        sm.open_session(current_app, session)
        print 'Created:', session[s_id]


@dashboard_routes.route('/control')
@dashboard_routes.route('/control/')
# @admin_required(current_app, session, login_redirect)
def dashboard_main():
    current_page = 'dashboard'
    ctl = current_app.config['ctl']
    response = ctl.render_tab(current_page)

    if response in config.ERROR_CODES:
        return redirect(url_for('settings_routes.advanced_settings', flag='NO_DB'))

    context = {
        'current_page': current_page,
        'current_class_js': 'control_panel/dashboard/Core.js',
        'current_page_js': 'control_panel/dashboard/Main.js',
        'current_requests_js': 'control_panel/dashboard/Requests.js',
        'current_page_content': response,
        'ts': int(time.time()),
        'modal': Markup(render_template('control_panel/modal.html')),
        'submenu': Markup(render_template('control_panel/subMenu_dashboard.html'))
    }

    return render_template('control_panel/control.html', data=context)


@dashboard_routes.route('/control/live_chat')
@dashboard_routes.route('/control/live_chat/')
# @admin_required(current_app, session, login_redirect)
def dashboard_live_chat():
    current_page = 'dashboard_live_chat'
    ctl = current_app.config['ctl']
    response = ctl.render_tab(current_page)

    if response in config.ERROR_CODES:
        return redirect(url_for('settings_routes.advanced_settings', flag='NO_DB'))

    context = {
        'current_page': current_page,
        'current_class_js': 'control_panel/dashboard/Core.js',
        'current_page_js': 'control_panel/dashboard/Main.js',
        'current_requests_js': 'control_panel/dashboard/Requests.js',
        'current_page_content': response,
        'ts': int(time.time()),
        'modal': Markup(render_template('control_panel/modal.html')),
        'submenu': Markup(render_template('control_panel/subMenu_dashboard.html'))
    }

    return render_template('control_panel/control.html', data=context)
