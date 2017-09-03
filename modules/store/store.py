import json, time

from flask import Blueprint, render_template, abort, current_app, session, request, Response, url_for, redirect
from uuid import uuid4

# ecomm module imports
from modules.db import *
from modules.decorators import *
from modules.auth.login import *
from modules.database.store import *
from modules.database.order import *
from modules.database.resources import *
from modules.database.user import *
import modules.database.customer as customer
import modules.database.config as config
from store_util import *

# this is only included here temporarily, as I can access the store wide cart object
from cart import *

store_routes = Blueprint('store_routes', __name__)


# this method creates a session for the store visitor before any request occurs
@store_routes.before_request
def setup_session():
    session_manager = current_app.config['SessionManager']
    s_id = current_app.config['session_cookie_id']

    if s_id not in session:
        session_manager.open_session(current_app, session)
        print 'Created new session:', session[s_id]


@store_routes.route('/index.html')
@store_routes.route('/')
@with_user_data(current_app, session)
def Home(user_data=None):
    if user_data is None:
        user_data = {}

    s_id = current_app.config['session_cookie_id']
    session_id = session[s_id]
    ts = int(time.time())

    current_page = 'Home'
    ctl = current_app.config['store_ctl']
    cart = current_app.config['CartManager']
    cartContents = cart.getCartContents(session)
    user_data['cart_contents'] = cartContents

    cursor = instance_handle().cursor()
    stripe_api_keys = config.getAPIKeys(cursor, 'stripe_api_keys')
    cursor.close()

    context = {
        'current_page': current_page,
        'current_class_js': 'store/Core.js',
        'current_page_js': ['store/' + current_page + '.js', 'store/lulu.js'],
        'common_libraries': render_template('store/common_libraries.html'),
        'nav_bar': ctl.render_tab('nav_bar', user_data),
        'footer': ctl.render_tab('footer', user_data),
        'page': ctl.render_tab('page', current_page),
        'live_chat_window': render_template('store/live_chat_window.html', ts=ts, session_id=session_id),
        'ts': ts,
        'stripe_api_keys': stripe_api_keys
    }

    return render_template('store/page.html', data=context)


@store_routes.route('/page/<string:page_id>')
@with_user_data(current_app, session)
def Page(page_id, user_data=None):
    if user_data is None:
        user_data = {}
    s_id = current_app.config['session_cookie_id']
    session_id = session[s_id]
    ts = int(time.time())

    ctl = current_app.config['store_ctl']
    cart = current_app.config['CartManager']
    cartContents = cart.getCartContents(session)
    user_data['cart_contents'] = cartContents

    cursor = instance_handle().cursor()
    stripe_api_keys = config.getAPIKeys(cursor, 'stripe_api_keys')
    cursor.close()

    context = {
        'current_page': page_id,
        'current_class_js': 'store/Core.js',
        'current_page_js': ['store/' + page_id + '.js', 'store/lulu.js'],
        'common_libraries': render_template('store/common_libraries.html'),
        'stripe_api_keys': stripe_api_keys,
        'nav_bar': ctl.render_tab('nav_bar', user_data),
        'footer': ctl.render_tab('footer', user_data),
        'page': ctl.render_tab('page', page_id),
        'live_chat_window': render_template('store/live_chat_window.html', ts=ts, session_id=session_id),
        'ts': int(time.time())
    }

    return render_template('store/page.html', data=context)


@store_routes.route('/googlec039a3f1a173c2f4.html')
@with_user_data(current_app, session)
def site_ownership(user_data=None):
    s_id = current_app.config['session_cookie_id']
    session_id = session[s_id]

    return render_template('store/googlec039a3f1a173c2f4.html')


@store_routes.route('/products/')
@store_routes.route('/products')
@with_user_data(current_app, session)
def AllProducts(user_data=None):
    if user_data is None:
        user_data = {}
    s_id = current_app.config['session_cookie_id']
    session_id = session[s_id]
    ts = int(time.time())

    ctl = current_app.config['store_ctl']
    cart = current_app.config['CartManager']
    cartContents = cart.getCartContents(session)

    instance_db = instance_handle().cursor()
    stripe_api_keys = config.getAPIKeys(instance_db, 'stripe_api_keys')
    instance_db.close()

    user_data['cart_contents'] = cartContents

    context = {
        'current_page': 'all_products',
        'current_class_js': 'store/Core.js',
        'current_page_js': ['store/AllProducts.js', 'store/lulu.js'],
        'stripe_api_keys': stripe_api_keys,
        'nav_bar': ctl.render_tab('nav_bar', user_data),
        'footer': ctl.render_tab('footer', user_data),
        'page_content': ctl.render_tab('all_products'),
        'live_chat_window': render_template('store/live_chat_window.html', ts=ts, session_id=session_id),
        'common_libraries': render_template('store/common_libraries.html'),
        'ts': ts
    }

    return render_template('store/all_products.html', data=context)


@store_routes.route('/collection/<collection_id>/')
@store_routes.route('/collection/<collection_id>')
@with_user_data(current_app, session)
def loadCollection(collection_id, user_data=None):
    if user_data is None:
        user_data = {}
    s_id = current_app.config['session_cookie_id']
    session_id = session[s_id]
    ts = int(time.time())

    ctl = current_app.config['store_ctl']
    cart = current_app.config['CartManager']
    cartContents = cart.getCartContents(session)

    instance_db = instance_handle().cursor()
    stripe_api_keys = config.getStripeAPIKeys(instance_db)
    instance_db.close()

    user_data['cart_contents'] = cartContents

    context = {
        'current_page': 'load_collection',
        'current_class_js': 'store/Core.js',
        'current_page_js': ['store/Collection.js', 'store/lulu.js'],
        'nav_bar': ctl.render_tab('nav_bar', user_data),
        'footer': ctl.render_tab('footer', user_data),
        'page_content': ctl.render_tab('load_collection', collection_id),
        'live_chat_window': render_template('store/live_chat_window.html', ts=ts, session_id=session_id),
        'common_libraries': render_template('store/common_libraries.html'),
        'ts': ts,
        'stripe_api_keys': stripe_api_keys
    }

    return render_template('store/collection.html', data=context)


@store_routes.route('/product/<int:product_id>/')
@store_routes.route('/product/<int:product_id>')
@with_user_data(current_app, session)
def viewProduct(product_id, user_data=None):
    if user_data is None:
        user_data = {}
    s_id = current_app.config['session_cookie_id']
    session_id = session[s_id]
    ts = int(time.time())

    ctl = current_app.config['store_ctl']
    cart = current_app.config['CartManager']
    cartContents = cart.getCartContents(session)

    instance_db = instance_handle().cursor()
    stripe_api_keys = config.getStripeAPIKeys(instance_db)
    instance_db.close()

    user_data['cart_contents'] = cartContents

    context = {
        'current_page': 'product',
        'current_class_js': 'store/Core.js',
        'current_page_js': ['store/Product.js', 'store/lulu.js'],
        'stripe_api_keys': stripe_api_keys,
        'nav_bar': ctl.render_tab('nav_bar', user_data),
        'footer': ctl.render_tab('footer', user_data),
        'page_content': ctl.render_tab('product', product_id),
        'live_chat_window': render_template('store/live_chat_window.html', ts=ts, session_id=session_id),
        'common_libraries': render_template('store/common_libraries.html'),
        'ts': ts
    }

    return render_template('store/product.html', data=context)


# shopping cart routes

@store_routes.route('/cart')
@with_user_data(current_app, session)
def cart(user_data=None):
    if user_data is None:
        user_data = {}
    s_id = current_app.config['session_cookie_id']
    session_id = session[s_id]
    ts = int(time.time())

    cart = current_app.config['CartManager']
    cartContents = cart.getCartContents(session)

    ctl = current_app.config['store_ctl']

    instance_db = instance_handle().cursor()
    stripe_api_keys = config.getStripeAPIKeys(instance_db)
    instance_db.close()

    user_data['cart_contents'] = cartContents

    context = {
        'current_page': 'cart',
        'current_class_js': 'store/Core.js',
        'current_page_js': ['store/Cart.js', 'store/lulu.js'],
        'stripe_api_keys': stripe_api_keys,
        'nav_bar': ctl.render_tab('nav_bar', user_data),
        'footer': ctl.render_tab('footer', user_data),
        'page_content': ctl.render_tab('cart', cartContents),
        'live_chat_window': render_template('store/live_chat_window.html', ts=ts, session_id=session_id),
        'common_libraries': render_template('store/common_libraries.html'),
        'ts': ts
    }

    return render_template('store/cart.html', data=context)


@store_routes.route('/store/addToCart', methods=['POST'])
@with_user_data(current_app, session)
def addToCart(user_data=None):
    cart = current_app.config['CartManager']

    item = request.form['productData']
    item = json.loads(item)

    cart.addItem(session, item)
    return json.dumps('success')


@store_routes.route('/store/updateCartItem', methods=['POST'])
@with_user_data(current_app, session)
def updateCartItem(user_data=None):
    cart = current_app.config['CartManager']

    item = request.form['productData']
    item = json.loads(item)

    cart.updateItem(session, item)
    return json.dumps('success')


# popups a message on the bottom of the screen to show that an item has been added to the cart
@store_routes.route('/store/popupMessage', methods=['POST'])
@with_user_data(current_app, session)
def popupMessage(user_data=None):
    message = request.form['message']
    message = json.loads(message)
    message = message.split(';')

    item_sku = message[0]
    quantity = message[1]

    instance_db = instance_handle()
    db = db_handle(instance_db)

    productData = loadProductBySKU(item_sku, db.cursor())

    if productData:
        product_thumbnail = loadResourceURI(productData['ImageSrc'], db.cursor())
        return json.dumps(render_template('store/popup_message.html', productData=productData, productQuantity=quantity,
                                          product_thumbnail=product_thumbnail))
    else:
        return json.dumps('no such product.')

    # return json.dumps('success')


# checkout routes
@store_routes.route('/checkout')
@with_user_data(current_app, session)
def checkout(user_data=None):
    if user_data is None:
        user_data = {}
    s_id = current_app.config['session_cookie_id']
    session_id = session[s_id]
    ts = int(time.time())

    cart = current_app.config['CartManager']
    cartContents = cart.getCartContents(session)

    if len(cartContents) == 0:
        return redirect(url_for('store_routes.Home'))

    saved_customer_data = {}
    if user_data:
        # this checks if this use has a customer_id associated with their account, if so, try to get saved address data
        if 'customer_id' in user_data:
            instance_db = instance_handle()
            db = db_handle(instance_db)
            # get saved customer info
            customer_info = customer.loadCustomer(user_data['customer_id'], db.cursor())

            # populate a dictionary for the template
            for field, value in customer_info.iteritems():
                saved_customer_data[field] = value

            db.close()

    ctl = current_app.config['store_ctl']

    instance_db = instance_handle().cursor()
    stripe_api_keys = config.getStripeAPIKeys(instance_db)
    instance_db.close()

    user_data['cart_contents'] = cartContents

    context = {
        'cart_contents': cartContents,
        'saved_customer_data': saved_customer_data,
        'current_page': 'checkout',
        'current_class_js': 'store/Core.js',
        'current_page_js': ['store/Checkout.js', 'store/Payment.js', 'store/lulu.js'],
        'stripe_api_keys': stripe_api_keys,
        'nav_bar': ctl.render_tab('nav_bar', user_data),
        'footer': ctl.render_tab('footer', user_data)
    }

    context['page_content'] = ctl.render_tab('checkout', context)
    context['live_chat_window'] = render_template('store/live_chat_window.html', ts=ts, session_id=session_id)
    context['common_libraries'] = render_template('store/common_libraries.html')
    context['ts'] = ts

    return render_template('store/checkout.html', data=context)


@store_routes.route('/order_success', methods=['GET'])
@with_user_data(current_app, session)
def order_success(user_data=None):
    if user_data is None:
        user_data = {}
    s_id = current_app.config['session_cookie_id']
    session_id = session[s_id]
    ts = int(time.time())

    ctl = current_app.config['store_ctl']
    sm = current_app.config['SessionManager']

    # empties cart before navbar render
    empty_cart(sm, current_app, session);

    cart = current_app.config['CartManager']
    cartContents = cart.getCartContents(session)

    context = {}

    charge_id = request.args.get('ch', '')

    if charge_id != '':
        instance_db = instance_handle()
        db = db_handle(instance_db)

        order_details = loadOrderByCharge(charge_id,
                                          db.cursor())  # loads order from db, so no session is required for persistance
        print 'CHARGE ID: ', charge_id
        if order_details:
            instance_db = instance_handle().cursor()
            context['stripe_api_keys'] = config.getStripeAPIKeys(instance_db)
            instance_db.close()

            context['current_page'] = 'order_success'
            context['current_class_js'] = 'store/Core.js'
            context['current_page_js'] = ['store/OrderSuccess.js', 'store/lulu.js']
            context['order_details'] = order_details
            context['page_content'] = ctl.render_tab('order_success', order_details)
        else:
            return redirect(url_for('store_routes.Home'))
    else:
        return redirect(url_for('store_routes.Home'))

    user_data['cart_contents'] = cartContents
    context['nav_bar'] = ctl.render_tab('nav_bar', user_data)
    context['footer'] = ctl.render_tab('footer', user_data)

    context['live_chat_window'] = render_template('store/live_chat_window.html', ts=ts, session_id=session_id)
    context['common_libraries'] = render_template('store/common_libraries.html')
    context['ts'] = ts

    return render_template('store/order_success.html', data=context)


# empties the cart
def empty_cart(session_manager, app, session):
    result = None
    s_id = current_app.config['session_cookie_id']

    context = {'key': session[s_id]}

    val = session_manager.get_session_key(app, session, context)

    if val:
        context['table'] = 'cart:' + session[s_id]
        result = session_manager.delete_session_hashTable(app, session, context)

    return result
