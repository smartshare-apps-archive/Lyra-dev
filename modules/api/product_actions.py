import json, ast, re

from flask import Blueprint, render_template, abort, current_app, session, request


#ecomm module imports
from modules.db import *
import modules.database.config
import modules.database.product as product
import modules.database.resources as resources
import modules.database.customer
from modules.decorators import *
from modules.auth.login import *


productActions = Blueprint('productActions', __name__, template_folder='templates')


@productActions.before_request
def setup_session():
	sm = current_app.config['SessionManager']
	s_id = current_app.config['session_cookie_id']

	if s_id not in session:
		sm.open_session(current_app, session)
		print "Created: ", session[s_id]



@productActions.route('/actions/addProduct', methods=['POST'])
#@admin_required(current_app, session, login_redirect)
def addProduct():
	productData = request.form['productData']
	productData = json.loads(productData)

	instance_db = instance_handle()
	db = db_handle(instance_db)

	productDatabase = db.cursor()

	product_id = product.saveNewProductData(productData, productDatabase)

	db.commit()
	db.close()

	return json.dumps(product_id)



@productActions.route('/actions/addCollection', methods=['POST'])
#@admin_required(current_app, session, login_redirect)
def addCollection():
	collectionData = request.form['collectionData']
	collectionData = json.loads(collectionData)

	instance_db = instance_handle()
	db = db_handle(instance_db)

	productDatabase = db.cursor()

	collection_id = product.saveNewCollectionData(collectionData, productDatabase)

	db.commit()
	db.close()

	return json.dumps(collection_id)




@productActions.route('/actions/addProductVariant', methods=['POST'])
##@admin_required(current_app, session, login_redirect)
def addProductVariant():
	variantData = request.form['variantData']
	variantData = json.loads(variantData)

	product_id = request.form['product_id'];
	product_id = json.loads(product_id);

	instance_db = instance_handle()
	db = db_handle(instance_db)

	productDatabase = db.cursor()
	
	product.saveNewVariantData(product_id, variantData, productDatabase)

	db.commit()
	db.close()

	return json.dumps(product_id)






@productActions.route('/actions/deleteProduct', methods=['POST'])
#@admin_required(current_app, session, login_redirect)
def deleteSingleProduct():
	product_id = request.form['product_id']

	instance_db = instance_handle()
	db = db_handle(instance_db)

	productDatabase = db.cursor()

	product_id = product.deleteProduct(product_id, productDatabase)

	db.commit()
	db.close()

	return "success"


@productActions.route('/actions/deleteCollection', methods=['POST'])
#@admin_required(current_app, session, login_redirect)
def deleteSingleCollection():
	collection_id = request.form['collection_id']

	instance_db = instance_handle()
	db = db_handle(instance_db)

	productDatabase = db.cursor()

	collection_id = product.deleteCollection(collection_id, productDatabase)

	db.commit()
	db.close()

	return "success"




@productActions.route('/actions/deleteVariant', methods=['POST'])
#@admin_required(current_app, session, login_redirect)
def deleteSingleVariant():
	variant_id = request.form['variant_id']

	instance_db = instance_handle()
	db = db_handle(instance_db)

	productDatabase = db.cursor()

	product.deleteVariant(variant_id, productDatabase)

	db.commit()
	db.close()

	return "success"



@productActions.route('/actions/updateProductData', methods=['POST'])
#@admin_required(current_app, session, login_redirect)
def updateProductData():
	product_data = request.form['product_data']
	product_data = json.loads(product_data)

	instance_db = instance_handle()
	db = db_handle(instance_db)

	
	productDatabase = db.cursor()
	product.saveProductData(product_data, productDatabase)

	db.commit()
	db.close()

	return json.dumps(product_data["product_id"]);



@productActions.route('/actions/updateProductInventory', methods=['POST'])
##@admin_required(current_app, session, login_redirect)
def updateProductInventory():
	inventory_qty = request.form['inventory_qty']
	inventory_qty = json.loads(inventory_qty)

	product_id = request.form['product_id'];
	product_id = json.loads(product_id);

	instance_db = instance_handle()
	db = db_handle(instance_db)

	productDatabase = db.cursor()
	
	product.updateProductInventory(product_id, inventory_qty, productDatabase)

	db.commit()
	db.close()

	return json.dumps(product_id)



#updates customer data changed in the customer editor 
@productActions.route('/actions/updateProductData', methods=['POST'])
#@admin_required(current_app, session, login_redirect)
def updateCustomerData():
	customer_data = request.form['customer_data']
	customer_data = json.loads(customer_data)

	instance_db = instance_handle()
	db = db_handle(instance_db)

	db_cursor = db.cursor()
	customer.saveCustomerData(customer_data, db_cursor)

	db.commit()
	db.close()

	return json.dumps(customer_data["customer_id"]);




@productActions.route('/actions/updateProductTags', methods=['POST'])
#@admin_required(current_app, session, login_redirect)
def updateProductTags():
	product_id = request.form['product_id']
	product_id = json.loads(product_id)

	product_tags = request.form['product_tags']
	product_tags = json.loads(product_tags)

	instance_db = instance_handle()
	db = db_handle(instance_db)

	productDatabase = db.cursor()

	result = product.saveProductTags(product_id, product_tags, productDatabase)

	db.commit()
	db.close()

	return json.dumps(product_id);



@productActions.route('/actions/updateProductTypes', methods=['POST'])
#@admin_required(current_app, session, login_redirect)
def updateProductTypes():
	product_types = request.form['product_types']
	product_types = json.loads(product_types)
	
	instance_db = instance_handle()
	database = instance_db.cursor()

	result = config.saveProductTypes(product_types, database)

	instance_db.commit()
	instance_db.close()

	return json.dumps("success");


@productActions.route('/actions/updateProductVendors', methods=['POST'])
#@admin_required(current_app, session, login_redirect)
def updateProductVendors():
	product_vendors = request.form['product_vendors']
	product_vendors = json.loads(product_vendors)
	
	instance_db = instance_handle()
	db = db_handle(instance_db)
	database = db.cursor()

	result = product.saveProductVendors(product_vendors, database)

	if result:
		db.commit()
		db.close()
		return json.dumps("success");
	else:
		db.close()
		return json.dumps("error saving vendors");



	




@productActions.route('/actions/deleteProductResource', methods=['POST'])
#@admin_required(current_app, session, login_redirect)
def deleteProductResource():
	product_id = request.form['product_id']
	product_id = json.loads(product_id)

	resource_id = request.form['resource_id']
	resource_id = json.loads(resource_id)

	resource_type = request.form['resource_type']
	resource_type = json.loads(resource_type)

	instance_db = instance_handle()
	db = db_handle(instance_db)

	productDatabase = db.cursor()
	result = resources.deleteProductResource(product_id, resource_id, resource_type, productDatabase)

	db.commit()
	db.close()

	return json.dumps(product_id);


@productActions.route('/actions/setDefaultProductImage', methods=['POST'])
#@admin_required(current_app, session, login_redirect)
def setDefaultProductImage():
	product_id = request.form['product_id']
	product_id = json.loads(product_id)

	resource_id = request.form['resource_id']
	resource_id = json.loads(resource_id)

	instance_db = instance_handle()
	db = db_handle(instance_db)

	productDatabase = db.cursor()
	result = product.setDefaultProductImage(product_id, resource_id, productDatabase)

	db.commit()
	db.close()

	return json.dumps(product_id);





@productActions.route('/actions/updateVariantTypes', methods=['POST'])
##@admin_required(current_app, session, login_redirect)
def updateProductVariantTypes():
	variantTypes = request.form['variantTypes']
	variantTypes = json.loads(variantTypes)

	product_id = request.form['product_id']
	product_id = json.loads(product_id)

	instance_db = instance_handle()
	db = db_handle(instance_db)

	
	productDatabase = db.cursor()
	product.saveProductVariantTypes(product_id, variantTypes, productDatabase)

	db.commit()
	db.close()
	

	return json.dumps(product_id);



@productActions.route('/actions/updateVariantData', methods=['POST'])
#@admin_required(current_app, session, login_redirect)
def updateVariantData():
	variant_data = request.form['variant_data']
	variant_data = json.loads(variant_data)

	instance_db = instance_handle()
	db = db_handle(instance_db)

	productDatabase = db.cursor()

	success = product.saveProductVariantData(variant_data, productDatabase)
	
	if success:
		db.commit()
		db.close()
		return json.dumps("success")
	else:
		db.close()
		return json.dumps("error")

	


@productActions.route('/actions/updateBulkProductEditorFields', methods=['POST'])
#@admin_required(current_app, session, login_redirect)
def updateBulkProductEditorFields():
	selectedFields = request.form['selectedFields']
	selectedFields = json.loads(selectedFields)

	instance_db = instance_handle()

	modules.database.config.setBulkProductEditorSettings(selectedFields, instance_db.cursor())

	instance_db.commit()
	instance_db.close()

	return json.dumps("success")



@productActions.route('/actions/updateBulkInventoryEditorFields', methods=['POST'])
#@admin_required(current_app, session, login_redirect)
def updateBulkInventoryEditorFields():
	selectedFields = request.form['selectedFields']
	selectedFields = json.loads(selectedFields)

	instance_db = instance_handle()

	modules.database.config.setBulkInventoryEditorSettings(selectedFields, instance_db.cursor())

	instance_db.commit()
	instance_db.close()

	return json.dumps("success")


@productActions.route('/actions/updateBulkCollectionEditorFields', methods=['POST'])
#@admin_required(current_app, session, login_redirect)
def updateBulkCollectionEditorFields():
	selectedFields = request.form['selectedFields']
	selectedFields = json.loads(selectedFields)

	instance_db = instance_handle()

	modules.database.config.setBulkCollectionEditorSettings(selectedFields, instance_db.cursor())

	instance_db.commit()
	instance_db.close()

	return json.dumps("success")





@productActions.route('/actions/updateCollectionData', methods=['POST'])
#@admin_required(current_app, session, login_redirect)
def updateCollectionData():
	collection_data = request.form['collection_data']
	collection_data = json.loads(collection_data)

	instance_db = instance_handle()
	db = db_handle(instance_db)

	productDatabase = db.cursor()
	
	product.saveCollectionData(collection_data, productDatabase)

	db.commit()
	db.close()

	return json.dumps("success")



#pull products in a collection, dump as JSON
@productActions.route('/actions/getCollectionProducts', methods=['POST'])
#@admin_required(current_app, session, login_redirect)
def getCollectionProducts():
	collection_conditions = request.form['collection_conditions']
	collection_conditions = json.loads(collection_conditions)

	collection_policy = request.form['collection_policy']
	collection_policy = json.loads(collection_policy)

	instance_db = instance_handle()
	db = db_handle(instance_db)

	productDatabase = db.cursor()
	
	collectionProductIDList = product.loadProductsInCollection(collection_conditions, collection_policy, productDatabase)
	productData = product.loadProductsByID(collectionProductIDList, productDatabase)

	db.close()

	return json.dumps(productData)








@productActions.route('/actions/bulkPublish', methods=['POST'])
#@admin_required(current_app, session, login_redirect)
def bulkAction_Publish():
	value = request.form['published']

	product_id_list = request.form['product_id_list']
	product_id_list = json.loads(product_id_list)

	instance_db = instance_handle()
	db = db_handle(instance_db)

	productDatabase = db.cursor()

	bulkPublish(value, product_id_list, productDatabase)

	db.commit()
	db.close()

	return json.dumps("success")



@productActions.route('/actions/bulkDelete', methods=['POST'])
#@admin_required(current_app, session, login_redirect)
def bulkAction_Delete():

	product_id_list = request.form['product_id_list']
	product_id_list = json.loads(product_id_list)

	instance_db = instance_handle()
	db = db_handle(instance_db)

	productDatabase = db.cursor()

	bulkDelete(product_id_list, productDatabase)

	db.commit()
	db.close()

	return json.dumps("success")



@productActions.route('/actions/bulkUpdateProducts', methods=['POST'])
#@admin_required(current_app, session, login_redirect)
def bulkAction_Update():
	productData = request.form['productData']
	productData = json.loads(productData)

	variantData = request.form['variantData']
	variantData = json.loads(variantData)

	instance_db = instance_handle()
	db = db_handle(instance_db)

	productDatabase = db.cursor()

	bulkUpdateProducts(productData, productDatabase)
	bulkUpdateVariants(variantData, productDatabase)

	db.commit()
	db.close()

	return json.dumps("success")



@productActions.route('/actions/bulkUpdateCollections', methods=['POST'])
#@admin_required(current_app, session, login_redirect)
def bulkAction_UpdateCollections():
	collectionData = request.form['collectionData']
	collectionData = json.loads(collectionData)

	instance_db = instance_handle()
	db = db_handle(instance_db)

	productDatabase = db.cursor()

	bulkUpdateCollections(collectionData, productDatabase)

	db.commit()
	db.close()

	return json.dumps("success")
