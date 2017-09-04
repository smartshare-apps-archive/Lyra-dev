import json, time

from flask import Blueprint, render_template, abort, current_app, session, request, Markup

# ecomm module imports
from modules.db import *
from modules.decorators import *
from modules.auth.login import *
import modules.database.order

settings_routes = Blueprint('settings_routes', __name__)


@settings_routes.before_request
def setup_session():
    sm = current_app.config['SessionManager']
    s_id = current_app.config['session_cookie_id']

    if s_id not in session:
        sm.open_session(current_app, session)
        print 'Created:', session[s_id]


@settings_routes.route('/control/settings')
@settings_routes.route('/control/settings/')
# @admin_required(current_app, session, login_redirect)
def settings():
    current_page = 'settings'
    ctl = current_app.config['ctl']
    response = ctl.render_tab(current_page)

    if response in config.ERROR_CODES:
        return redirect(url_for('settings_routes.advanced_settings', flag='NO_DB'))

    context = dict(
        current_page=current_page,
        current_class_js='control_panel/settings/Core.js',
        current_page_js='control_panel/settings/Main.js',
        current_requests_js='control_panel/settings/Requests.js',
        current_page_content=response,
        ts=int(time.time()),
        modal=Markup(render_template('control_panel/modal.html')),
        submenu=Markup(render_template('control_panel/subMenu_settings.html'))
    )

    return render_template('control_panel/control.html', data=context)


@settings_routes.route('/control/settings/advanced')
@settings_routes.route('/control/settings/advanced/')
@settings_routes.route('/control/settings/advanced/?flag=<string:flag>')
# @admin_required(current_app, session, login_redirect)
def advanced_settings(flag=None):
    current_page = 'settings_advanced'
    ctl = current_app.config['ctl']

    response = ctl.render_tab(current_page)

    context = dict(
        current_page=current_page,
        current_class_js='control_panel/settings/Core.js',
        current_page_js='control_panel/settings/Advanced.js',
        current_requests_js='control_panel/settings/Requests.js',
        ts=int(time.time()),
        modal=Markup(render_template('control_panel/modal.html')),
        submenu=Markup(render_template('control_panel/subMenu_settings.html')),
        current_page_content=ctl.render_tab('settings_advanced', flag)
    )

    return render_template('control_panel/control.html', data=context)


@settings_routes.route('/control/settings/payment')
@settings_routes.route('/control/settings/payment/')
# @admin_required(current_app, session, login_redirect)
def payment_settings():
    current_page = 'settings_payment'
    ctl = current_app.config['ctl']
    response = ctl.render_tab(current_page)

    if response in config.ERROR_CODES:
        return redirect(url_for('settings_routes.advanced_settings', flag='NO_DB'))

    context = dict(
        current_page=current_page,
        current_class_js='control_panel/settings/Core.js',
        current_page_js='control_panel/settings/PaymentSettings.js',
        current_requests_js='control_panel/settings/Requests.js',
        current_page_content=response,
        ts=int(time.time()),
        modal=Markup(render_template('control_panel/modal.html')),
        submenu=Markup(render_template('control_panel/subMenu_settings.html'))
    )

    return render_template('control_panel/control.html', data=context)


@settings_routes.route('/control/settings/shipping')
@settings_routes.route('/control/settings/shipping/')
# @admin_required(current_app, session, login_redirect)
def shipping_settings():
    current_page = 'settings_shipping'
    ctl = current_app.config['ctl']
    response = ctl.render_tab(current_page)

    if response in config.ERROR_CODES:
        return redirect(url_for('settings_routes.advanced_settings', flag='NO_DB'))

    context = dict(
        current_page=current_page,
        current_class_js='control_panel/settings/Core.js',
        current_page_js='control_panel/settings/Shipping.js',
        current_requests_js='control_panel/settings/Requests.js',
        current_page_content=response,
        ts=int(time.time()),
        modal=Markup(render_template('control_panel/modal.html')),
        submenu=Markup(render_template('control_panel/subMenu_settings.html'))
    )

    return render_template('control_panel/control.html', data=context)
