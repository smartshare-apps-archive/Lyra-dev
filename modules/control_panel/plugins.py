import json, time

from flask import Blueprint, render_template, abort, current_app, session, request, Markup

# ecomm module imports
from modules.db import *
from modules.decorators import *
from modules.auth.login import *
import modules.database.order

plugin_routes = Blueprint('plugin_routes', __name__)


@plugin_routes.before_request
def setup_session():
    sm = current_app.config['SessionManager']
    s_id = current_app.config['session_cookie_id']

    if s_id not in session:
        sm.open_session(current_app, session)
        print 'Created:', session[s_id]


@plugin_routes.route('/control/plugins')
@plugin_routes.route('/control/plugins/')
# @admin_required(current_app, session, login_redirect)
def plugins():
    ctl = current_app.config['ctl']

    context = dict(
        current_page='plugins',
        current_class_js='control_panel/plugins/Core.js',
        current_page_js='control_panel/plugins/Main.js',
        current_requests_js='control_panel/plugins/Requests.js',
        current_page_content=ctl.render_tab('plugins'),
        ts=int(time.time()),
        modal=Markup(render_template('control_panel/modal.html')),
        submenu=Markup(render_template('control_panel/subMenu_plugins.html'))
    )

    return render_template('control_panel/control.html', data=context)


@plugin_routes.route('/control/plugins/pyutil/<int:plugin_id>')
@plugin_routes.route('/control/plugins/pyutil/<int:plugin_id>/')
# @admin_required(current_app, session, login_redirect)
def plugins_pyutil(plugin_id):
    ctl = current_app.config['ctl']

    context = dict(
        current_page='plugins_pyutil',
        current_class_js='control_panel/plugins/Core.js',
        current_page_js='control_panel/plugins/PyUtil.js',
        current_requests_js='control_panel/plugins/Requests.js',
        current_page_content=ctl.render_tab('plugins_pyutil', plugin_id),
        ts=int(time.time()),
        modal=Markup(render_template('control_panel/modal.html')),
        submenu=Markup(render_template('control_panel/subMenu_plugins.html'))
    )

    return render_template('control_panel/control.html', data=context)
