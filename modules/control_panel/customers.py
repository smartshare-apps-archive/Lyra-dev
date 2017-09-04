import json, time

from flask import Blueprint, redirect, render_template, abort, current_app, session, request, Markup, url_for

# ecomm module imports
from modules.db import *
from modules.decorators import *
from modules.auth.login import *
import modules.database.order

customer_routes = Blueprint('customer_routes', __name__)


@customer_routes.before_request
def setup_session():
    sm = current_app.config['SessionManager']
    s_id = current_app.config['session_cookie_id']

    if s_id not in session:
        sm.open_session(current_app, session)
        print 'Created:', session[s_id]


@customer_routes.route('/control/customers')
@customer_routes.route('/control/customers/')
# @admin_required(current_app, session, login_redirect)
def customers():
    current_page = 'customers'
    ctl = current_app.config['ctl']
    response = ctl.render_tab(current_page)

    if response in config.ERROR_CODES:
        return redirect(url_for('settings_routes.advanced_settings', flag='NO_DB'))

    context = dict(
        current_page_content=response,
        current_page=current_page,
        current_class_js='control_panel/customer/Core.js',
        current_page_js='control_panel/customer/Main.js',
        current_requests_js='control_panel/customer/Requests.js',
        ts=int(time.time()),
        modal=Markup(render_template('control_panel/modal.html')),
        submenu=Markup(render_template('control_panel/subMenu_customers.html'))
    )

    return render_template('control_panel/control.html', data=context)


# route to single customer editor
@customer_routes.route('/control/customers/<customer_id>', methods=['GET', 'POST'])
@customer_routes.route('/control/customers/<customer_id>/', methods=['GET', 'POST'])
# @admin_required(current_app, session, login_redirect)
def customerEditor(customer_id):
    current_page = 'customer_editor'
    ctl = current_app.config['ctl']
    response = ctl.render_tab(current_page, data=customer_id)

    if response in config.ERROR_CODES:
        return redirect(url_for('settings_routes.advanced_settings', flag='NO_DB'))

    context = dict(
        current_page=current_page,
        current_class_js='control_panel/customer/Core.js',
        current_page_js='control_panel/customer/CustomerEditor.js',
        current_requests_js='control_panel/customer/Requests.js',
        current_page_content=response,
        ts=int(time.time()),
        modals=[render_template('control_panel/modal.html')],
        submenu=Markup(render_template('control_panel/subMenu_customers.html'))
    )

    return render_template('control_panel/control.html', data=context)
