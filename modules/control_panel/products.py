import json, time

from flask import Blueprint, render_template, abort, current_app, session, request, Markup, url_for, redirect

#ecomm module imports
from modules.db import *
from modules.decorators import *
from modules.auth.login import *
import modules.database.product

import modules.database.config as config

from modules.database.product_util import *


product_routes = Blueprint('product_routes', __name__, template_folder='templates')		#blueprint definition


@product_routes.before_request
def setup_session():
	sm = current_app.config['SessionManager']
	s_id = current_app.config['session_cookie_id']

	if s_id not in session:
		sm.open_session(current_app, session)
		print "Created: ", session[s_id]


#route to main product list
@product_routes.route('/control/products/', methods=['GET', 'POST'])
@product_routes.route('/control/products', methods=['GET', 'POST'])
##@admin_required(current_app, session, login_redirect)
def products():
	ctl = current_app.config["ctl"]
	data = {}

	data["current_page"] = "products"
	data["current_class_js"] = "control_panel/product/Core.js"
	data["current_page_js"] = "control_panel/product/Main.js"
	data["current_requests_js"] = "control_panel/product/Requests.js"

	response = ctl.render_tab("products")

	if response in config.ERROR_CODES:
		return redirect(url_for('settings_routes.advanced_settings', flag="NO_DB"))
	else:
		data["current_page_content"] = response

	data["ts"] = int(time.time())
	data["modals"] = [render_template("control_panel/modal.html")]
	data["submenu"] = Markup(render_template("control_panel/subMenu_products.html"))

	return render_template("control_panel/control.html", data=data)




#route to single product editor
@product_routes.route('/control/products/<int:product_id>/')
@product_routes.route('/control/products/<int:product_id>')
#@admin_required(current_app, session, login_redirect)
def productEditor(product_id):
	ctl = current_app.config["ctl"]
	data = {}

	data["current_page"] = "product_editor"
	data["product_id"] = product_id

	response = ctl.render_tab("product_editor", data=product_id)

	if response in config.ERROR_CODES:
		return redirect(url_for('settings_routes.advanced_settings', flag="NO_DB"))
	else:
		data["current_page_content"] = response


	data["ts"] = int(time.time())

	instance_db = instance_handle()
	db = db_handle(instance_db)
	
	product_data = loadProduct(product_id, db.cursor())

	if product_data["Tags"]:
		product_tags = formatProductTags(product_data["Tags"])
	else:
		product_tags = []

	all_tags = config.loadProductTags(instance_db.cursor())
	all_types = config.loadProductTypes(instance_db.cursor())

	print "ALL TAGS: ", all_tags

	db.close()

	data["modals"] = [render_template("control_panel/modal.html"), 
					  render_template("control_panel/modal_image_upload.html", product_id=product_id), 
					  render_template("control_panel/modal_edit_tags.html", product_id=product_id, product_tags=product_tags, all_tags=all_tags),
					  render_template("control_panel/modal_edit_types.html", product_id=product_id, all_types=all_types, product_type=product_data["Type"])
					  ]

	data["submenu"] = Markup(render_template("control_panel/subMenu_products.html"))
	data["current_class_js"] = "control_panel/product/Core.js"
	data["current_page_js"] = "control_panel/product/ProductEditor.js"
	data["current_requests_js"] = "control_panel/product/Requests.js"


	return render_template("control_panel/control.html", data=data)



#route to single collection editor
@product_routes.route('/control/products/collections/<collection_id>/')
@product_routes.route('/control/products/collections/<collection_id>')
#@admin_required(current_app, session, login_redirect)
def collectionEditor(collection_id):
	ctl = current_app.config["ctl"]
	data = {}

	data["current_page"] = "collection_editor"
	data["product_id"] = collection_id


	response = ctl.render_tab("collection_editor", data=collection_id)

	if response in config.ERROR_CODES:
		return redirect(url_for('settings_routes.advanced_settings', flag="NO_DB"))
	else:
		data["current_page_content"] = response


	data["ts"] = int(time.time())
	data["modals"] = [render_template("control_panel/modal.html"), render_template("control_panel/modal_image_upload.html", collection_id=collection_id)]
	data["submenu"] = Markup(render_template("control_panel/subMenu_products.html"))
	data["current_class_js"] = "control_panel/product/Core.js"
	data["current_page_js"] = "control_panel/product/CollectionEditor.js"
	data["current_requests_js"] = "control_panel/product/Requests.js"

	return render_template("control_panel/control.html", data=data)



#route to single collection editor
@product_routes.route('/control/products/addCollection/')
@product_routes.route('/control/products/addColection')
#@admin_required(current_app, session, login_redirect)
def productEditor_newCollection():
	ctl = current_app.config["ctl"]
	data = {}

	data["current_page"] = "collection_editor_new"

	response = ctl.render_tab("collection_editor_new")

	if response in config.ERROR_CODES:
		return redirect(url_for('settings_routes.advanced_settings', flag="NO_DB"))
	else:
		data["current_page_content"] = response


	data["ts"] = int(time.time())
	data["modals"] = [render_template("control_panel/modal.html")]
	data["submenu"] = Markup(render_template("control_panel/subMenu_products.html"))
	data["current_class_js"] = "control_panel/product/Core.js"
	data["current_page_js"] = "control_panel/product/CollectionEditorNew.js"
	data["current_requests_js"] = "control_panel/product/Requests.js"

	return render_template("control_panel/control.html", data=data)




#route to bulk collection editor
@product_routes.route('/control/products/collections/bulkEditor', methods=['GET'])
#@admin_required(current_app, session, login_redirect)
def productBulkCollectionEditor():
	ctl = current_app.config["ctl"]
	collectionIDList = request.args.get('ids', '')
	collectionIDList = collectionIDList.split(',')
	collectionIDList = map(int, collectionIDList)

	data = {}
	data["collectionIDList"] = collectionIDList

	data["current_page"] = "product_bulk_collection_editor"

	response = ctl.render_tab("product_bulk_collection_editor", data["collectionIDList"])

	if response in config.ERROR_CODES:
		return redirect(url_for('settings_routes.advanced_settings', flag="NO_DB"))
	else:
		data["current_page_content"] = response

	data["current_class_js"] = "control_panel/product/Core.js"
	data["current_page_js"] = "control_panel/product/BulkCollectionEditor.js"
	data["current_requests_js"] = "control_panel/product/Requests.js"

	data["ts"] = int(time.time())
	data["modals"] = [render_template("control_panel/modal.html")]
	data["submenu"] = Markup(render_template("control_panel/subMenu_products.html"))

	return render_template("control_panel/control.html", data=data)



#route to bulk product editor
@product_routes.route('/control/products/bulkEditor', methods=['GET'])
#@admin_required(current_app, session, login_redirect)
def productBulkEditor():
	ctl = current_app.config["ctl"]
	productIdList = request.args.get('ids', '')
	productIdList = productIdList.split(',')
	productIdList = map(int, productIdList)

	data = {}
	data["productIdList"] = productIdList
	data["current_page"] = "product_bulk_editor"

	response = ctl.render_tab("product_bulk_editor", data["productIdList"])

	if response in config.ERROR_CODES:
		return redirect(url_for('settings_routes.advanced_settings', flag="NO_DB"))
	else:
		data["current_page_content"] = response
	
	data["current_class_js"] = "control_panel/product/Core.js"
	data["current_page_js"] = "control_panel/product/BulkProductEditor.js"
	data["current_requests_js"] = "control_panel/product/Requests.js"


	data["ts"] = int(time.time())
	data["modals"] = [render_template("control_panel/modal.html")]
	data["submenu"] = Markup(render_template("control_panel/subMenu_products.html"))

	return render_template("control_panel/control.html", data=data)



#route to product inventory list
@product_routes.route('/control/products/inventory/')
#@admin_required(current_app, session, login_redirect)
def productInventory():
	ctl = current_app.config["ctl"]
	data = {}

	data["current_page"] = "product_inventory"

	response = ctl.render_tab(data["current_page"])

	if response in config.ERROR_CODES:
		return redirect(url_for('settings_routes.advanced_settings', flag="NO_DB"))
	else:
		data["current_page_content"] = response


	data["current_class_js"] = "control_panel/product/Core.js"
	data["current_page_js"] = "control_panel/product/Inventory.js"
	data["current_requests_js"] = "control_panel/product/Requests.js"

	data["ts"] = int(time.time())
	data["modals"] = [render_template("control_panel/modal.html")]
	data["submenu"] = Markup(render_template("control_panel/subMenu_products.html"))

	return render_template("control_panel/control.html", data=data)



#route to single product inventory editor
@product_routes.route('/control/products/inventory/<product_id>')
@product_routes.route('/control/products/inventory/<product_id>/')
#@admin_required(current_app, session, login_redirect)
def productInventoryEditor(product_id):
	ctl = current_app.config["ctl"]
	data = {}

	data["current_page"] = "product_inventory_editor"

	response = ctl.render_tab(data["current_page"], data=product_id)

	if response in config.ERROR_CODES:
		return redirect(url_for('settings_routes.advanced_settings', flag="NO_DB"))
	else:
		data["current_page_content"] = response


	data["current_class_js"] = "control_panel/product/Core.js"
	data["current_page_js"] = "control_panel/product/InventoryEditor.js"
	data["current_requests_js"] = "control_panel/product/Requests.js"

	data["ts"] = int(time.time())
	data["modals"] = [render_template("control_panel/modal.html")]
	data["submenu"] = Markup(render_template("control_panel/subMenu_products.html"))

	return render_template("control_panel/control.html", data=data)



#route to bulk product inventory editor
@product_routes.route('/control/products/inventory/bulkEditor', methods=['GET'])
#@admin_required(current_app, session, login_redirect)
def productBulkInventoryEditor():
	ctl = current_app.config["ctl"]
	variantIdList = request.args.get('ids', '')
	variantIdList = variantIdList.split(',')
	variantIdList = map(int, variantIdList)

	data = {}
	data["variantIdList"] = variantIdList

	data["current_page"] = "product_bulk_inventory_editor"

	response = ctl.render_tab(data["current_page"], data["variantIdList"])

	if response in config.ERROR_CODES:
		return redirect(url_for('settings_routes.advanced_settings', flag="NO_DB"))
	else:
		data["current_page_content"] = response

	
	data["current_class_js"] = "control_panel/product/Core.js"
	data["current_page_js"] = "control_panel/product/BulkInventoryEditor.js"
	data["current_requests_js"] = "control_panel/product/Requests.js"

	data["ts"] = int(time.time())
	data["modals"] = [render_template("control_panel/modal.html")]
	data["submenu"] = Markup(render_template("control_panel/subMenu_products.html"))

	return render_template("control_panel/control.html", data=data)


#route to product collections list
@product_routes.route('/control/products/collections/')
#@admin_required(current_app, session, login_redirect)
def productCollections():
	ctl = current_app.config["ctl"]
	data = {}

	data["current_page"] = "product_collections"
	
	response = ctl.render_tab(data["current_page"])

	if response in config.ERROR_CODES:
		return redirect(url_for('settings_routes.advanced_settings', flag="NO_DB"))
	else:
		data["current_page_content"] = response

	data["current_class_js"] = "control_panel/product/Core.js"
	data["current_page_js"] = "control_panel/product/Collections.js"
	data["current_requests_js"] = "control_panel/product/Requests.js"

	data["ts"] = int(time.time())
	data["modals"] = [render_template("control_panel/modal.html")]
	data["submenu"] = Markup(render_template("control_panel/subMenu_products.html"))

	return render_template("control_panel/control.html", data=data)
