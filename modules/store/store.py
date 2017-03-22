import json, time

from flask import Blueprint, render_template, abort, current_app, session, request, Response, url_for, redirect
from uuid import uuid4

#ecomm module imports
from modules.db import *
from modules.decorators import *
from modules.auth.login import *
from modules.database.store import *
from modules.database.order import *
from modules.database.resources import *
from modules.database.user import *
import modules.database.customer as customer
from store_util import *

#this is only included here temporarily, as I can access the store wide cart object
from cart import *


store_routes = Blueprint('store_routes', __name__, template_folder='templates')		#blueprint definition


#this method creates a session for the store visitor before any request occurs
@store_routes.before_request
def setup_session():
	session_manager = current_app.config['SessionManager']
	s_id = current_app.config['session_cookie_id']

	if s_id not in session:
		session_manager.open_session(current_app, session)
		print "Created new session: ", session[s_id]



@store_routes.route('/index.html')
@store_routes.route('/')
@with_user_data(current_app, session)
def Home(user_data=None):
	page_id = "Home"
	ctl = current_app.config["store_ctl"]
	cart = current_app.config['CartManager']
	cartContents = cart.getCartContents(session)
	
	data = {}

	data["current_page"] = page_id
	data["current_class_js"] = "store/Core.js"
	data["current_page_js"] = ["store/"+page_id+".js", "store/lulu.js"]
	data["common_libraries"] = render_template("store/common_libraries.html")

	if user_data:
		user_data["cart_contents"] = cartContents
		data["nav_bar"] = ctl.render_tab("nav_bar", user_data)
		data["footer"] = ctl.render_tab("footer", user_data)
	else:
		user_data = {}
		user_data["cart_contents"] = cartContents
		data["nav_bar"] = ctl.render_tab("nav_bar", user_data)
		data["footer"] = ctl.render_tab("footer", user_data)

		
	data["page"] = ctl.render_tab("page",page_id)
	data["ts"] = int(time.time())

	return render_template("store/page.html", data=data)


@store_routes.route('/page/<string:page_id>')
@with_user_data(current_app, session)
def Page(page_id, user_data=None):
	ctl = current_app.config["store_ctl"]
	cart = current_app.config['CartManager']
	cartContents = cart.getCartContents(session)
	
	data = {}

	data["current_page"] = page_id
	data["current_class_js"] = "store/Core.js"
	data["current_page_js"] = ["store/"+page_id+".js", "store/lulu.js"]
	data["common_libraries"] = render_template("store/common_libraries.html")

	if user_data:
		user_data["cart_contents"] = cartContents
		data["nav_bar"] = ctl.render_tab("nav_bar", user_data)
		data["footer"] = ctl.render_tab("footer", user_data)
	else:
		user_data = {}
		user_data["cart_contents"] = cartContents
		data["nav_bar"] = ctl.render_tab("nav_bar", user_data)
		data["footer"] = ctl.render_tab("footer", user_data)

		
	data["page"] = ctl.render_tab("page",page_id)
	data["ts"] = int(time.time())

	return render_template("store/page.html", data=data)



@store_routes.route('/products/')
@store_routes.route('/products')
@with_user_data(current_app, session)
def AllProducts(user_data=None):
	ctl = current_app.config["store_ctl"]
	cart = current_app.config['CartManager']
	cartContents = cart.getCartContents(session)

	data = {}

	data["current_page"] = "all_products"
	data["current_class_js"] = "store/Core.js"
	data["current_page_js"] = ["store/AllProducts.js", "store/lulu.js"]

	if user_data:
		user_data["cart_contents"] = cartContents
		data["nav_bar"] = ctl.render_tab("nav_bar", user_data)
		data["footer"] = ctl.render_tab("footer", user_data)
	else:
		user_data = {}
		user_data["cart_contents"] = cartContents
		data["nav_bar"] = ctl.render_tab("nav_bar", user_data)
		data["footer"] = ctl.render_tab("footer", user_data)


	data["page_content"] = ctl.render_tab("all_products")
	data["common_libraries"] = render_template("store/common_libraries.html")
	data["ts"] = int(time.time())

	return render_template("store/all_products.html", data=data)



@store_routes.route('/collection/<collection_id>/')
@store_routes.route('/collection/<collection_id>')
@with_user_data(current_app, session)
def loadCollection(collection_id, user_data=None):
	ctl = current_app.config["store_ctl"]
	cart = current_app.config['CartManager']
	cartContents = cart.getCartContents(session)

	data = {}

	data["current_page"] = "load_collection"
	data["current_class_js"] = "store/Core.js"
	data["current_page_js"] = ["store/Collection.js", "store/lulu.js"]

	if user_data:
		user_data["cart_contents"] = cartContents
		data["nav_bar"] = ctl.render_tab("nav_bar", user_data)
		data["footer"] = ctl.render_tab("footer", user_data)
	else:
		user_data = {}
		user_data["cart_contents"] = cartContents
		data["nav_bar"] = ctl.render_tab("nav_bar", user_data)
		data["footer"] = ctl.render_tab("footer", user_data)


	data["page_content"] = ctl.render_tab("load_collection", collection_id)
	data["common_libraries"] = render_template("store/common_libraries.html")
	data["ts"] = int(time.time())

	return render_template("store/collection.html", data=data)



@store_routes.route('/product/<int:product_id>/')
@store_routes.route('/product/<int:product_id>')
@with_user_data(current_app, session)
def viewProduct(product_id, user_data=None):
	ctl = current_app.config["store_ctl"]
	cart = current_app.config['CartManager']
	cartContents = cart.getCartContents(session)

	data = {}

	data["current_page"] = "product"
	data["current_class_js"] = "store/Core.js"
	data["current_page_js"] = ["store/Product.js", "store/lulu.js"]

	if user_data:
		user_data["cart_contents"] = cartContents
		data["nav_bar"] = ctl.render_tab("nav_bar", user_data)
		data["footer"] = ctl.render_tab("footer", user_data)
	else:
		user_data = {}
		user_data["cart_contents"] = cartContents
		data["nav_bar"] = ctl.render_tab("nav_bar", user_data)
		data["footer"] = ctl.render_tab("footer", user_data)


	data["page_content"] = ctl.render_tab("product", product_id)

	data["common_libraries"] = render_template("store/common_libraries.html")
	data["ts"] = int(time.time())

	return render_template("store/product.html", data=data)




#shopping cart routes

@store_routes.route('/cart')
@with_user_data(current_app, session)
def cart(user_data=None):
	cart = current_app.config['CartManager']
	cartContents = cart.getCartContents(session)
	
	ctl = current_app.config["store_ctl"]
	data = {}

	data["current_page"] = "cart"
	data["current_class_js"] = "store/Core.js"
	data["current_page_js"] = ["store/Cart.js", "store/lulu.js"]

	if user_data:
		user_data["cart_contents"] = cartContents
		data["nav_bar"] = ctl.render_tab("nav_bar", user_data)
		data["footer"] = ctl.render_tab("footer", user_data)
	else:
		user_data = {}
		user_data["cart_contents"] = cartContents
		data["nav_bar"] = ctl.render_tab("nav_bar", user_data)
		data["footer"] = ctl.render_tab("footer", user_data)


	data["page_content"] = ctl.render_tab("cart", cartContents)
	data["common_libraries"] = render_template("store/common_libraries.html")
	data["ts"] = int(time.time())

	return render_template("store/cart.html", data=data)



@store_routes.route('/store/addToCart', methods=['POST'])
@with_user_data(current_app, session)
def addToCart(user_data=None):
	cart = current_app.config['CartManager']

	item = request.form['productData']
	item = json.loads(item)

	cart.addItem(session, item)
	return json.dumps("success")



@store_routes.route('/store/updateCartItem', methods=['POST'])
@with_user_data(current_app, session)
def updateCartItem(user_data=None):
	cart = current_app.config['CartManager']

	item = request.form['productData']
	item = json.loads(item)

	cart.updateItem(session, item)
	return json.dumps("success")



#popups a message on the bottom of the screen to show that an item has been added to the cart
@store_routes.route('/store/popupMessage', methods=['POST'])
@with_user_data(current_app, session)
def popupMessage(user_data=None):
	message = request.form['message']
	message = json.loads(message)
	
	message = message.split(';')

	item_sku = message[0]
	quantity = message[1]
	db = db_handle()

	productData = loadProductBySKU(item_sku, db.cursor())
	
	if productData:
		product_thumbnail = loadResourceURI(productData["ImageSrc"], db.cursor())
		return json.dumps(render_template("store/popup_message.html", productData = productData, productQuantity = quantity, product_thumbnail = product_thumbnail))
	else:
		return json.dumps("no such product.")

	return json.dumps("success")


#checkout routes
@store_routes.route('/checkout')
@with_user_data(current_app, session)
def checkout(user_data=None):
	data = {}

	cart = current_app.config['CartManager']
	cartContents = cart.getCartContents(session)

	if len(cartContents) == 0:
		return redirect(url_for('store_routes.Home'))

	data["cart_contents"] = cartContents
	data["saved_customer_data"] = {}

	if user_data: 
		if("customer_id" in user_data):	#this checks if this use has a customer_id associated with their account, if so, try to get saved address data
			db = db_handle()
			#get saved customer info
			customer_info = customer.loadCustomer(user_data["customer_id"], db.cursor())

			#populate a dictionary for the template
			for field, value in customer_info.iteritems():
				data["saved_customer_data"][field] = value

			db.close()

	ctl = current_app.config["store_ctl"]

	data["current_page"] = "checkout"
	data["current_class_js"] = "store/Core.js"
	data["current_page_js"] = ["store/Checkout.js", "store/Payment.js", "store/lulu.js"]	

	if user_data:
		user_data["cart_contents"] = cartContents
		data["nav_bar"] = ctl.render_tab("nav_bar", user_data)
		data["footer"] = ctl.render_tab("footer", user_data)
	else:
		user_data = {}
		user_data["cart_contents"] = cartContents
		data["nav_bar"] = ctl.render_tab("nav_bar", user_data)
		data["footer"] = ctl.render_tab("footer", user_data)


	data["page_content"] = ctl.render_tab("checkout", data)
	data["common_libraries"] = render_template("store/common_libraries.html")
	data["ts"] = int(time.time())

	return render_template("store/checkout.html", data=data)



@store_routes.route('/order_success', methods=['GET'])
@with_user_data(current_app, session)
def order_success(user_data=None):
	ctl = current_app.config["store_ctl"]
	sm = current_app.config['SessionManager']

	#empties cart before navbar render
	empty_cart(sm, current_app, session);

	cart = current_app.config['CartManager']
	cartContents = cart.getCartContents(session)
	
	data = {}

	charge_id = request.args.get('ch','')

	if charge_id != '':
		db = db_handle()
		order_details = loadOrderByCharge(charge_id, db.cursor())	#loads order from db, so no session is required for persistance
		print "CHARGE ID: ", charge_id
		if order_details:
			data["current_page"] = "order_success"
			data["current_class_js"] = "store/Core.js"
			data["current_page_js"] = ["store/OrderSuccess.js", "store/lulu.js"]
			data["order_details"] = order_details
			data["page_content"] = ctl.render_tab("order_success", order_details)
		else:
			return redirect(url_for('store_routes.Home'))
	else:
		return redirect(url_for('store_routes.Home'))


	if user_data:
		user_data["cart_contents"] = cartContents
		data["nav_bar"] = ctl.render_tab("nav_bar", user_data)
		data["footer"] = ctl.render_tab("footer", user_data)
	else:
		user_data = {}
		user_data["cart_contents"] = cartContents
		data["nav_bar"] = ctl.render_tab("nav_bar", user_data)
		data["footer"] = ctl.render_tab("footer", user_data)


	data["common_libraries"] = render_template("store/common_libraries.html")
	data["ts"] = int(time.time())

	return render_template("store/order_success.html", data=data)




#empties the cart 
def empty_cart(session_manager, app, session):
	s_id = current_app.config['session_cookie_id']

	data = {}
	data['key'] = session[s_id]
	
	val = session_manager.get_session_key(app, session, data)

	if val:
		data["table"] = "cart:" + session[s_id]
		result = session_manager.delete_session_hashTable(app, session, data)

	if result:
		return result
	else:
		return None