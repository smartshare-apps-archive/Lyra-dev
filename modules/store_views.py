from flask import render_template, Markup

#ecomm module imports
import database.config as config

from database.product import *
from database.order import *
from database.product_util import *
from database.order_util import *
import database.resources as resources
import database.store as store
from store.store_util import *

from db import *

import sqlite3, sys

class Store(object):
	def __init__(self):
		self.setupVariables()

	def setupVariables(self,):
		self.store_data = {}

	def render_tab(self, tab, data=None):
		instance_db = instance_handle()
		db = db_handle(instance_db)
		
		self.database = db.cursor()
		self.instance_db = instance_db.cursor()
		#store views: gotta think of a way to add these in a better way
		if tab == "home":
			return self.Home()
		elif tab == "all_products":
			return self.AllProducts()
		elif tab == "load_collection":
			return self.LoadCollection(data)
		elif tab == "product":
			return self.ViewProduct(data)
		elif tab == "cart":
			return self.ViewCart(data)
		elif tab == "checkout":
			return self.ViewCheckout(data)	
		elif tab == "order_success":
			return self.ViewOrderDetails(data)	
		elif tab == "page":
			return self.ViewPage(data)	
		elif tab == "nav_bar":
			return self.NavBar(data)
		elif tab == "footer":
			return self.Footer(data)


		self.database = None
		db.close()	



	def NavBar(self, user_data=None):
		navBarRoot = "top_nav_bar"
		navBarTheme = "_lulu"

		nav_categories = store.getNavCategories(self.database)

		formattedNavCategories = {}

		for nav_category, nav_data in nav_categories.iteritems():
			formattedNavCategories[nav_category] = {}
			for nav_item in nav_data:
				nav_item = nav_item.split(':')
				formattedNavCategories[nav_category][nav_item[0]] = nav_item[1]


		for navCategory,navData in formattedNavCategories.iteritems():
			resource_id =  formattedNavCategories[navCategory]["resource_id"]
			formattedNavCategories[navCategory]["resource"] = resources.loadResourceURI(resource_id, self.database)
			if(formattedNavCategories[navCategory]["type"]) == "dropdown_list":
				formattedNavCategories[navCategory]["resource"] = parseDropdownList(formattedNavCategories[navCategory]["resource"])
			

		if user_data:
			rendered_nav_data = render_template("store/" + navBarRoot + navBarTheme + ".html", nav_data=formattedNavCategories, user_data=user_data)
		else:
			rendered_nav_data = render_template("store/" + navBarRoot + navBarTheme + ".html", nav_data=formattedNavCategories)
		return rendered_nav_data


	def Footer(self, user_data=None):
		footerRoot = "footer"
		footerTheme = "_lulu"

		footer_categories = store.getFooterCategories(self.database)

		formattedFooterCategories = {}

		for footer_category, footer_data in footer_categories.iteritems():
			formattedFooterCategories[footer_category] = {}
			for footer_item in footer_data:
				footer_item = footer_item.split(':')
				formattedFooterCategories[footer_category][footer_item[0]] = footer_item[1]


		for footerCategory,footerData in formattedFooterCategories.iteritems():
			resource_id =  formattedFooterCategories[footerCategory]["resource_id"]
			formattedFooterCategories[footerCategory]["resource"] = resources.loadResourceURI(resource_id, self.database)
			if(formattedFooterCategories[footerCategory]["type"]) == "dropdown_list":
				formattedFooterCategories[footerCategory]["resource"] = parseDropdownList(formattedFooterCategories[footerCategory]["resource"])
			

		if user_data:
			rendered_footer_data = render_template("store/" + footerRoot + footerTheme + ".html", footer_data=formattedFooterCategories, user_data=user_data)
		else:
			rendered_footer_data = render_template("store/" + footerRoot + footerTheme + ".html", footer_data=formattedFooterCategories)
		return rendered_footer_data


	def PageSection(self):
		pass


	def Home(self):
		product_splash = render_template("store/platform_demo.html")
		
		self.store_data["product_splash"] = product_splash
		return self.store_data



	def AllProducts(self):
		products = loadAllProducts(self.database)
		print products
		image_resources = loadProductImages(products, self.database)

		for product_id, product in products.iteritems():
			if(products[product_id]["Published"] == "false"):
				del products[product_id]
				continue

		rows = formatProductRows(products)

		self.store_data["product_rows"] = render_template("store/product_row.html", products=products, rows=rows, image_resources=image_resources)
		return self.store_data



	def ViewProduct(self, product_id):
		productData = loadProduct(product_id, self.database)
		
		image_resources = {}

		if productData.has_key("resources"):
			if(productData["resources"] is not None and productData["resources"] != ""):
				imageResources = extractImageResources(productData["resources"]) #gets image resource id list from resource database
				imageURI = loadResourceURIList(imageResources, self.database)
				imageURI = formatImageURIs(imageURI)

				image_resources = imageURI  #so the product editor can access those image resources
				print "image resources: ", image_resources

		variants = loadProductVariants(product_id, self.database)
		variantTypes = productData["VariantTypes"]
		formattedVariantTypes = {}
		availableVariants = []

		if variantTypes:
			variantTypes = filter(lambda v: v != '', variantTypes.split(';'))
			
			for variant in variantTypes:
				variant = variant.split(':')

				variantType = variant[0]
				variantValues = variant[1].split(',')
				
				formattedVariantTypes[variantType] = variantValues

			if variants:
				for variant in variants:
					variantData = formatVariantData(variant["VariantData"])
					availableVariants.append(variantData)	


		productDetails = render_template("store/product_details.html", product = productData, variants = variants, variant_types = formattedVariantTypes, availableVariants = availableVariants, image_resources=image_resources)
		
		self.store_data["product_details"] = productDetails
		self.store_data["product_title"] = productData["Title"]

		return self.store_data




	def ViewPage(self, page_id):
		page_data = store.getPage(page_id, self.database) 

		page_template = page_data["template"]
		page_type = page_data["type"]
		page_content = page_data["content"]
		page_sections = filter(lambda s: s != '', page_data["sections"].split(','))
		page_section_data = page_data["section_data"]
		
		page_section_data = filter(lambda s: s != '', page_section_data.split('<section_split>'))
		pageSectionData = {}
		
		#this block loads all the section data and parses it into a dictionary
		for section_data in page_section_data:
			section_data = section_data.split('<id_split>')
			
			section_type = section_data[0].split(':')

			section_id = section_type[0]
			section_template = section_type[1]

			sectionData = section_data[1]

			pageSectionData[section_id] = {}
			pageSectionData[section_id]["section_template"] = section_template
			anchors = sectionData.split('<split>')

			for anchor in anchors:
				anchor = anchor.split('<anchor_id_split>')
				anchor_tag = anchor[0]
				anchor_data = anchor[1]

				pageSectionData[section_id][anchor_tag] = {}
				
				anchor_data = anchor_data.split('<>')
				for anchor_field in anchor_data:
					anchor_field = anchor_field.split('=')
					anchor_field = [anchor_field[0], '='.join(anchor_field[1:])]

					anchor_field_id = anchor_field[0]
					anchor_field_value = anchor_field[1]

					pageSectionData[section_id][anchor_tag][anchor_field_id] = anchor_field_value
		
		

		self.store_data["page_sections"] = page_sections
		self.store_data["rendered_sections"] = {}

		#print pageSectionData
		for section_id in page_sections:
			if section_id != "content":
				section_template_id = pageSectionData[section_id]["section_template"]
				current_section_template = store.loadSectionTemplate(section_template_id, self.database)
				current_section_template = filter(lambda s: s != '' , current_section_template.split('<split>'))

				pageSectionTemplateData = {}

				for section_template_field in current_section_template:
					section_template_field = section_template_field.split('=')
					section_template_field = [section_template_field[0], '='.join(section_template_field[1:])]

					section_template_field_id = section_template_field[0]
					section_template_field_value = section_template_field[1]

					pageSectionTemplateData[section_template_field_id] = section_template_field_value

				for anchor_id, anchor_data in pageSectionData[section_id].iteritems():
					if anchor_id == "section_template":
						continue
					if anchor_data["anchor_type"] == 'image-resource':
						anchor_data["anchor_value"] = loadResourceURI(anchor_data["anchor_value"], self.database)

				#render a specific section
				rendered_section = render_template(pageSectionTemplateData["template_file"], section_data = pageSectionData[section_id])
				self.store_data["rendered_sections"][section_id] = rendered_section



		template_data = store.loadTemplateData(page_template, self.database)
		type_template_data = store.loadTypeTemplateData(page_type, self.database)

		template_folder = template_data["template_folder"]

		if "delimeter" in template_data:
			content_delimeter = template_data["delimeter"]
			page_content = page_content.split(content_delimeter)
		elif "delimeter" in type_template_data:
			content_delimeter = type_template_data["delimeter"]
			page_content = page_content.split(content_delimeter)
		else:
			content_delimeter = None


		root_name =  type_template_data["root_name"]
		template_location = "store/" + template_folder + "/" + root_name + "_"+page_template+".html"
				
		self.store_data["content_section"] = render_template(template_location, page_content = page_content)
		
		return self.store_data



	def ViewCart(self, cartContents):
		products = {}
		
		try:
			product_thumbnail = {}
			for productSKU, quantity in cartContents.iteritems():
				currentProductData = loadProductBySKU(productSKU, self.database)		
				currentImageURI = loadResourceURI(currentProductData["ImageSrc"], self.database)

				product_thumbnail[currentProductData["product_id"]] = currentImageURI 
				products[productSKU] = [currentProductData, quantity]
		except:
			print "Cart is empty."

		finally:		
			self.store_data["cart_details"] = render_template("store/cart_details.html", products=products, product_thumbnail = product_thumbnail)

		return self.store_data




	def ViewCheckout(self, data):
		products = {}

		if data["cart_contents"]:
			product_thumbnail = {}

			for productSKU, quantity in data["cart_contents"].iteritems():
				currentProductData = loadProductBySKU(productSKU, self.database)

				currentImageURI = loadResourceURI(currentProductData["ImageSrc"], self.database)
				product_thumbnail[currentProductData["product_id"]] = currentImageURI 

				products[productSKU] = [currentProductData, quantity]
				
			self.store_data["cart_details"] = render_template("store/cart_details_checkout.html", products=products, product_thumbnail=product_thumbnail)
				
		country_list = config.CountryList(self.instance_db)
		country_options = render_template("store/country_list.html", country_list=country_list, saved_customer_data=data["saved_customer_data"])

		self.store_data["table_checkout"] = render_template("store/table_checkout.html", products=products, country_options=country_options, saved_customer_data = data["saved_customer_data"]) 

		return self.store_data



	def ViewOrderDetails(self, data):
		products = {}
		order_details = data

		if order_details:
			itemList = order_details["SKU_List"].split(',')
			product_thumbnail = {}

			for item in itemList:
				productSKU = item.split(';')[0]
				quantity = item.split(';')[1]
				#load product data by SKU_List
				currentProductData = loadProductBySKU(productSKU, self.database)
				#load product image thumbnail for cart table
				currentImageURI = loadResourceURI(currentProductData["ImageSrc"], self.database)
				product_thumbnail[currentProductData["product_id"]] = currentImageURI 

				products[productSKU] = [currentProductData, quantity]
				
			self.store_data["cart_details"] = render_template("store/cart_details_checkout.html", products=products, product_thumbnail = product_thumbnail)

		return self.store_data
	


	def LoadCollection(self, collection_id):
		collectionData = loadCollection(collection_id, self.database)
		products = loadProductsInCollection(collectionData, self.database)	
		products = filter(lambda p: p["Published"]==True, products)

		rows = formatProductRows(products)

		self.store_data["collection_title"] = collectionData["Title"]
		self.store_data["product_rows"] = render_template("store/product_row.html", products=products, rows=rows)

		return self.store_data



