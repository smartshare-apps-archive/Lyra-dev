import os, stripe, datetime
from modules.db import *

if __name__ == "__main__":
	import modules.database.product as product
	import modules.database.order as order
	import modules.database.config as config


instance_db = instance_handle()
store_database = db_handle(instance_db)

#grab stripe api key settings from database

PRODUCTS_PER_REQUEST = 3

class stripe_manager(object):
	stripe_keys = config.getStripeAPIKeys(instance_db.cursor())

	if(stripe_keys["payment_status"] == "enabled"):
		stripe.api_key = stripe_keys['secret_key_live']
	else:
		stripe.api_key = stripe_keys['secret_key_test']

	def __init__(self):
		pass


	#updates the desired product data in the users stripe api profile
	@classmethod
	def updateProductCatalog(cls):
		products = product.loadAllProducts(store_database.cursor())

		for product_id, product_data in products.iteritems():
			current_variants = product.loadProductVariants(product_id, store_database.cursor())
			#print current_variants

		for i in range(0, len(products), 5):
			product_batch = stripe.Product.list(limit=5)

			for current_product in product_batch:
				current_product.delete()



	#deletes all products and variants from the users stripe api profile
	@classmethod
	def deleteProductCatalog(cls):
		variant_catalog = cls.getVariantCatalog()

		for sku_id, variant_data in variant_catalog.iteritems():
			variant_to_delete = stripe.SKU.retrieve(sku_id)
			variant_to_delete.delete()


		product_catalog = cls.getProductCatalog()

		for product_id, product_data in product_catalog.iteritems():
			product_to_delete = stripe.Product.retrieve(product_id)
			product_to_delete.delete()

		#product_batch = stripe.Product.list(limit=5)

		#for current_product in product_batch:
		#	current_product.delete()


	#retrieves all the product data stored in a users stripe api profile, which is used to create orders during checkout
	@classmethod
	def getVariantCatalog(cls):
		variants_in_catalog = {}

		more_products = True
		last_product_in_batch = None

		while(more_products):
			product_batch = stripe.SKU.list(limit=PRODUCTS_PER_REQUEST, starting_after=last_product_in_batch)

			variants_in_catalog.update({current_product["id"]: current_product for current_product in product_batch["data"]})
			product_id_list = [current_product["id"] for current_product in product_batch["data"]]
			last_product_in_batch = product_id_list[len(product_id_list)-1]

			more_products = product_batch["has_more"]

		return variants_in_catalog



	#retrieves all the product data stored in a users stripe api profile, which is used to create orders during checkout
	@classmethod
	def getProductCatalog(cls):
		products_in_catalog = {}

		more_products = True
		last_product_in_batch = None

		while(more_products):
			product_batch = stripe.Product.list(limit=PRODUCTS_PER_REQUEST, starting_after=last_product_in_batch)

			products_in_catalog.update({current_product["id"]: current_product for current_product in product_batch["data"]})
			product_id_list = [current_product["id"] for current_product in product_batch["data"]]
			last_product_in_batch = product_id_list[len(product_id_list)-1]

			more_products = product_batch["has_more"]

		return products_in_catalog




	#creates a new product object for stripe so it can be referenced during order creation
	@classmethod
	def createProduct(cls, product_data):
		variantTypes = product_data.get("VariantTypes", None)
		productName = product_data.get("Title", None)
		productDescription = product_data.get("BodyHTML", None)

		if variantTypes:
			variantTypes = variantTypes.split(';')
			attribute_list = filter(lambda a: a != '', [attribute.split(':')[0] for attribute in variantTypes])
		else:
			attribute_list = []


		product_obj = stripe.Product.create(
			name = productName,
			description = productDescription,
			attributes = attribute_list

		)

		return product_obj["id"]



	#creates a new variant object for stripe so it can be referenced during order creation
	@classmethod
	def createVariant(cls, product_data, variant_data = None):
		productPrice = product_data.get("VariantPrice", None)

		if productPrice <= 0.00:
			productPrice = 200
		else:
			productPrice = int(float(productPrice)*100)

		if variant_data:
			variantAttributes = variant_data.get("attributes", {})
			print "Creating with:", variantAttributes
		else:
			variantAttributes = {}

		variant_obj = stripe.SKU.create(
			product=product_data["stripe_id"],
			attributes=variantAttributes,
			price=productPrice,
			currency='usd',
			inventory={'type': 'finite', 'quantity': 1}
		)

		return variant_obj["id"]



	#updates a product with new data 
	@classmethod
	def updateProduct(cls, product_data):
		variantTypes = product_data.get("VariantTypes", None)
		productName = product_data.get("Title", None)
		productDescription = product_data.get("BodyHTML", None)
		#productInventory = product_data.get("VariantInventoryQty", None)

		

		productDimensions = {
			product_data.get("VariantWeight", None)
							}

		product_id = product_data["stripe_id"]
		stripe_product = stripe.Product.retrieve(product_id)

		if variantTypes:
			if type(variantTypes) != dict:
				variantTypes = variantTypes.split(';')
				attribute_list = filter(lambda a: a != '', [attribute.split(':')[0] for attribute in variantTypes])
			elif type(variantTypes) == dict:
				attribute_list = [attr for attr, values in variantTypes.iteritems()]
			else:
				attribute_list = []

			stripe_product["attributes"] = attribute_list

		if productName:
			stripe_product["name"] = productName

		if productDescription:
			stripe_product["description"] = productDescription

		cls.updateVariant(product_data)

		stripe_product.save()
		


	@classmethod
	def updateVariant(cls, product_data):
		variant_id = product_data["VariantSKU"]
		stripe_variant = stripe.SKU.retrieve(variant_id)

		inventoryQty = product_data.get('VariantInventoryQty', None)

		if inventoryQty:
			stripe_variant["inventory"] = { 'type': 'finite', 'quantity': int(inventoryQty) }

		stripe_variant.save()


	@classmethod
	def getProduct(cls, productData):
		product_id = productData["stripe_id"]
		stripe_product = stripe.Product.retrieve(product_id)
		
		return stripe_product
	

	@classmethod
	def getDefaultVariant(cls, productData):
		variant_id = productData.get("VariantSKU", None)
		stripe_variant = stripe.SKU.retrieve(variant_id)
		return stripe_variant


	@classmethod
	def getVariant(cls, variantData):
		variant_id = variantData.get("stripe_id", None)
		stripe_variant = stripe.SKU.retrieve(variant_id)
		return stripe_variant



	@classmethod
	def populateProductCatalog(cls, products):
		for product_id, product_data in products.iteritems():
			product_obj = cls.createProduct(product_data)

			product_data["stripe_id"] = product_obj

			variant_obj = cls.createVariant(product_data)

			product_data["VariantSKU"] = variant_obj

			print product_obj,":", variant_obj

			product.saveProductData(product_data, store_database.cursor())

		store_database.commit()



if __name__ == "__main__":
	#productData = product.loadProduct(2, store_database.cursor())
	#stripe_manager.getProduct(productData)

	#stripe_manager.createProduct(productData)

	products = product.loadAllProducts(store_database.cursor())
	stripe_manager.populateProductCatalog(products)

	#stripe_manager.deleteProductCatalog()
	#stripe_manager.getProductCatalog()