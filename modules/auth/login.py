import json, time

from flask import Blueprint, render_template, abort, current_app, session, request, Response
from uuid import uuid4

# ecomm module imports
from modules.db import *
from modules.database.config import *
from modules.decorators import *
from modules.database.store import *
from modules.database.user import *
import modules.database.order
import modules.database.config as config

# this is only included here temporarily, as I can access the store wide cart object
from modules.store.cart import *
from modules.store.store import *

login_routes = Blueprint('login_routes', __name__)


# this method creates a session for the store visitor before any request occurs
@login_routes.before_request
def setup_session():
    sm = current_app.config['SessionManager']
    s_id = current_app.config['session_cookie_id']

    if s_id not in session:
        sm.open_session(current_app, session)
        print 'Created:', session[s_id]


@login_routes.route('/login')
@login_routes.route('/login/')
@redirect_logged_in(current_app, session, Home)
@with_user_data(current_app, session)
def login_redirect(product_id=None, collection_id=None):
    ctl = current_app.config['auth_ctl']
    store_ctl = current_app.config['store_ctl']
    cart = current_app.config['CartManager']
    instance_db = instance_handle().cursor()
    redirect_url = request.url_rule

    user_data = {
        'cart_contents': cart.getCartContents(session)
    }

    context = dict(
        current_page='home',
        current_class_js='auth/Core.js',
        current_page_js='auth/Login.js',
        nav_bar=store_ctl.render_tab('nav_bar', user_data),
        footer=store_ctl.render_tab('footer', user_data),
        page_content=ctl.render_tab('login'),
        redirect_url=redirect_url,
        ts=int(time.time()),
        stripe_api_keys=config.getStripeAPIKeys(instance_db),
        common_libraries=render_template('store/common_libraries.html')
    )

    instance_db.close()

    return render_template('auth/login.html', data=context)


@login_routes.route('/auth/login', methods=['POST'])
@db_required
def auth_login(db):
    login_info = request.form['login_info']
    login_info = json.loads(login_info)

    user_data = auth_user(login_info, db)

    if user_data:
        sm = current_app.config['SessionManager']
        set_session_data(sm, current_app, session, user_data)
        return json.dumps(user_data)
    else:
        return json.dumps('invalid')


@login_routes.route('/auth/logout')
@db_required
def logout(db):
    sm = current_app.config['SessionManager']
    destroy_session_data(sm, current_app, session)
    db.close()

    return Home()


def destroy_session_data(session_manager, app, session):
    s_id = current_app.config['session_cookie_id']
    data = {'key': session[s_id]}
    val = session_manager.get_session_key(app, session, data)
    result = None

    if val and val != 'guest':
        # delete all session data associated with this user from the redis table
        for prefix in sessionPrefixList:
            data['table'] = prefix + session[s_id]
            result = session_manager.delete_session_hashTable(app, session, data)

        # preserve distinct login to a session
        data['key'] = session[s_id]
        data['value'] = 'guest'

        session_manager.update_session_key(app, session, data)
    return result


def set_session_data(session_manager, app, session, user_data):
    s_id = current_app.config['session_cookie_id']

    data = {
        'key': session[s_id]
    }

    val = session_manager.get_session_key(app, session, data)

    if val:
        prefix = 'auth:'
        data['table'] = prefix + session[s_id]

        for key, value in user_data.iteritems():
            if type(value) is type(None):
                continue

            data['key'] = key
            data['value'] = value

            session_manager.set_session_hashKey(app, session, data)

        # preserve distinct login to a session
        data['key'] = session[s_id]
        data['value'] = user_data['username']

        session_manager.update_session_key(app, session, data)
