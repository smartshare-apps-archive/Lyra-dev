import json, time

from flask import Blueprint, render_template, abort, current_app, session, request, Markup

# ecomm module imports
from modules.db import *
import modules.database.order
from modules.decorators import *
from modules.auth.login import *

order_routes = Blueprint('order_routes', __name__)


@order_routes.before_request
def setup_session():
    sm = current_app.config['SessionManager']
    s_id = current_app.config['session_cookie_id']

    if s_id not in session:
        sm.open_session(current_app, session)
        print 'Created:', session[s_id]


# route to main order list
@order_routes.route('/control/orders/', methods=['GET', 'POST'])
@order_routes.route('/control/orders', methods=['GET', 'POST'])
# @admin_required(current_app, session, login_redirect)
def orders():
    current_page = 'orders'
    ctl = current_app.config['ctl']
    response = ctl.render_tab(current_page)

    if response in config.ERROR_CODES:
        return redirect(url_for('settings_routes.advanced_settings', flag='NO_DB'))

    context = {
        'current_page': current_page,
        'current_class_js': 'control_panel/order/Core.js',
        'current_page_js': 'control_panel/order/Main.js',
        'current_requests_js': 'control_panel/order/Requests.js',
        'current_page_content': response,
        'ts': int(time.time()),
        'modals': [render_template('control_panel/modal.html')],
        'submenu': Markup(render_template('control_panel/subMenu_orders.html'))
    }

    return render_template('control_panel/control.html', data=context)


# route to main order list
@order_routes.route('/control/orders/drafts/', methods=['GET', 'POST'])
@order_routes.route('/control/orders/drafts', methods=['GET', 'POST'])
# @admin_required(current_app, session, login_redirect)
def orders_drafts():
    current_page = 'orders_drafts'
    ctl = current_app.config['ctl']
    response = ctl.render_tab(current_page)

    if response in config.ERROR_CODES:
        return redirect(url_for('settings_routes.advanced_settings', flag='NO_DB'))

    context = {
        'current_page': current_page,
        'current_class_js': 'control_panel/order/Core.js',
        'current_page_js': 'control_panel/order/Drafts.js',
        'current_requests_js': 'control_panel/order/Requests.js',
        'current_page_content': response,
        'ts': int(time.time()),
        'modals': [render_template('control_panel/modal.html')],
        'submenu': Markup(render_template('control_panel/subMenu_orders.html'))
    }

    return render_template('control_panel/control.html', data=context)


# route to single order editor
@order_routes.route('/control/orders/<order_id>', methods=['GET', 'POST'])
@order_routes.route('/control/orders/<order_id>/', methods=['GET', 'POST'])
# @admin_required(current_app, session, login_redirect)
def orderEditor(order_id):
    current_page = 'order_editor'
    ctl = current_app.config['ctl']
    response = ctl.render_tab(current_page, data=order_id)

    if response in config.ERROR_CODES:
        return redirect(url_for('settings_routes.advanced_settings', flag='NO_DB'))

    context = {
        'current_page': current_page,
        'current_class_js': 'control_panel/order/Core.js',
        'current_page_js': 'control_panel/order/OrderEditor.js',
        'current_requests_js': 'control_panel/order/Requests.js',
        'current_page_content': response,
        'ts': int(time.time()),
        'modals': [render_template('control_panel/modal.html')],
        'submenu': Markup(render_template('control_panel/subMenu_orders.html'))
    }

    return render_template('control_panel/control.html', data=context)


# route to single draft editor
@order_routes.route('/control/orders/addDraft', methods=['GET', 'POST'])
@order_routes.route('/control/orders/addDraft/', methods=['GET', 'POST'])
# @admin_required(current_app, session, login_redirect)
def addDraft():
    current_page = 'order_editor_draft_new'
    ctl = current_app.config['ctl']
    response = ctl.render_tab(current_page)

    if response in config.ERROR_CODES:
        return redirect(url_for('settings_routes.advanced_settings', flag='NO_DB'))

    context = {
        'current_page': current_page,
        'current_class_js': 'control_panel/order/Core.js',
        'current_page_js': 'control_panel/order/DraftEditorNew.js',
        'current_requests_js': 'control_panel/order/Requests.js',
        'current_page_content': response,
        'ts': int(time.time()),
        'modals': [render_template('control_panel/modal.html')],
        'submenu': Markup(render_template('control_panel/subMenu_orders.html'))
    }

    return render_template('control_panel/control.html', data=context)


# route to order fulfillment
@order_routes.route('/control/orders/fulfill/<order_id>', methods=['GET', 'POST'])
@order_routes.route('/control/orders/fulfill/<order_id>/', methods=['GET', 'POST'])
# @admin_required(current_app, session, login_redirect)
def fulfillOrder(order_id):
    current_page = 'order_fulfill'
    ctl = current_app.config['ctl']
    response = ctl.render_tab(current_page, data=order_id)

    if response in config.ERROR_CODES:
        return redirect(url_for('settings_routes.advanced_settings', flag='NO_DB'))

    context = {
        'current_page': current_page,
        'current_class_js': 'control_panel/order/Core.js',
        'current_page_js': 'control_panel/order/Fulfill.js',
        'current_requests_js': 'control_panel/order/Requests.js',
        'current_page_content': response,
        'ts': int(time.time()),
        'modals': [render_template('control_panel/modal.html')],
        'submenu': Markup(render_template('control_panel/subMenu_orders.html'))
    }

    return render_template('control_panel/control.html', data=context)
