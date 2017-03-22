import sqlite3, sys, csv, json, collections

#config current only has column/field mapping information, which will be specific to the import form (of the product csv), e.g. shopify
from config import *	
from product_util import *


#load single product by product_id
def loadProduct(product_id, productDatabase):
	try:
		productDatabase.execute("SELECT product_id,VariantSKU,VariantPrice,VariantCompareAtPrice,VariantInventoryQty,VariantTaxable,Title,BodyHTML,Vendor,Type,Tags,Published,ImageSrc,ImageAltText,VariantTypes,resources FROM products WHERE product_id=%s;", [product_id] )
	except Exception as e:
		print "Exception hey: ", e
		return None

	productData = productDatabase.fetchone()

	if productData:
		print "Product data:", productData
		formattedProductData = {}
		for i in range(len(productColumnMappings)):
			formattedProductData[productColumnMappings[i]] = productData[i]
		return formattedProductData
	else:
		return None



#load single product by product_id
def loadProductBySKU(variantSKU, productDatabase):
	variantData = None 
	if len(variantSKU.split('-')) == 1:
		productDatabase.execute("""SELECT product_id,VariantSKU,VariantPrice,VariantCompareAtPrice,VariantInventoryQty,VariantTaxable,Title,BodyHTML,Vendor,Type,Tags,Published,ImageSrc,ImageAltText,VariantTypes,resources FROM products WHERE VariantSKU='%s';""",(variantSKU, ))
	else:
		product_id = variantSKU.split('-')[0]
		variantData = loadProductVariantBySKU(variantSKU, productDatabase)
		productDatabase.execute("""SELECT product_id,VariantSKU,VariantPrice,VariantCompareAtPrice,VariantInventoryQty,VariantTaxable,Title,BodyHTML,Vendor,Type,Tags,Published,ImageSrc,ImageAltText,VariantTypes,resources FROM products WHERE VariantSKU='%s';""",(product_id, ))

	productData = productDatabase.fetchone()

	if productData:
		formattedProductData = {}
		for i in range(len(productColumnMappings)):
			formattedProductData[productColumnMappings[i]] = productData[i]

		if variantData:
			for field, value in variantData.iteritems():
				formattedProductData[field] = value

		return formattedProductData
	else:
		return None



def loadProductVariant(variant_id, productDatabase):
	currentQuery = """SELECT variant_id, VariantSKU, product_id, VariantData, VariantPrice, VariantCompareAtPrice, VariantGrams, VariantWeightUnit, VariantInventoryQty,
				      VariantImg, VariantTaxCode, VariantTaxable, VariantBarcode, VariantRequiresShipping FROM product_variants WHERE variant_id = %s;"""
	try:
		productDatabase.execute(currentQuery, (variant_id, ))
	except Exception as e:
		print "Error: ", e
		return None

	variantData = productDatabase.fetchone()

	#format the variant data for easy access in the templates
	if variantData:
		formattedVariantData = {}
		for i in range(len(variantColumnMappings)):
			formattedVariantData[variantColumnMappings[i]] = variantData[i]
		return formattedVariantData

	else:
		return None


def loadProductVariants(product_id, productDatabase):
	currentQuery = """SELECT variant_id, VariantSKU, product_id, VariantData, VariantPrice, VariantCompareAtPrice, VariantGrams, VariantWeightUnit, VariantInventoryQty,
				      VariantImg, VariantTaxCode, VariantTaxable, VariantBarcode, VariantRequiresShipping FROM product_variants WHERE product_id = %s;"""
	try:
		productDatabase.execute(currentQuery, (product_id, ))
	except Exception as e:
		print "Error: ", e
		return None

	variantData = productDatabase.fetchall()

	formattedVariantData = []

	#format the variant data for easy access in the templates
	if variantData:
		for i in range(len(variantData)):
			formattedVariantData.append({})
			for j in range(len(variantColumnMappings)):
				formattedVariantData[i][variantColumnMappings[j]] = variantData[i][j]
		return formattedVariantData

	else:
		return []




#loads a variant by it's SKU
def loadProductVariantBySKU(VariantSKU, productDatabase):
	currentQuery = """SELECT variant_id, VariantSKU, product_id, VariantData, VariantPrice, VariantCompareAtPrice, VariantGrams, VariantWeightUnit, VariantInventoryQty,
				      VariantImg, VariantTaxCode, VariantTaxable, VariantBarcode, VariantRequiresShipping FROM product_variants WHERE VariantSKU = '%s';"""
	try:
		productDatabase.execute(currentQuery, (VariantSKU, ))
	except Exception as e:
		print "Error: ", e
		return None

	variantData = productDatabase.fetchone()

	#format the variant data for easy access in the templates
	if variantData:
		formattedVariantData = {}
		for i in range(len(variantColumnMappings)):
			formattedVariantData[variantColumnMappings[i]] = variantData[i]
		return formattedVariantData

	else:
		return None



#load all products and parse columns into dictionary format for easy hashing
def loadAllProducts(productDatabase):
	formattedProductList = collections.OrderedDict()

	#select all products in database, including variants
	productDatabase.execute("""SELECT product_id,VariantSKU,VariantPrice,VariantCompareAtPrice,VariantInventoryQty,VariantTaxable,Title,BodyHTML,Vendor,Type,Tags,Published,ImageSrc,ImageAltText,VariantTypes,resources FROM products;""")

	productList = productDatabase.fetchall()

	for i in range(len(productList)):
		currentProductID = str(productList[i][0])
		formattedProductList[currentProductID] = {}	#create a new dictionary for each product

		#go through the list of key names (set in config.py file) and assign values to their respective keys
		for j in range(len(productColumnMappings)):
			formattedProductList[currentProductID][productColumnMappings[j]] = productList[i][j]
	
	return formattedProductList



#load all product variants and parses them columns into dictionary format for easy hashing
def loadAllProductVariants(formattedProductList, productDatabase):
	formattedVariantList = collections.OrderedDict()

	for product_id, product in formattedProductList.iteritems():
		currentProductVariants = loadProductVariants(product_id, productDatabase)
		if currentProductVariants is not None:
			formattedVariantList[product_id] = currentProductVariants

	return formattedVariantList




def loadCollection(collectionID, productDatabase):	
	try:
		productDatabase.execute("""SELECT collection_id,Title,BodyHTML,CollectionImageSrc,Published,Conditions,Strict,URL,Meta,PageTitle,Template,resources FROM collections WHERE collection_id=%s;""",(collectionID,));
	except Exception as e:
		return None
	
	collection = productDatabase.fetchone()
	
	if collection:
		formattedCollection = {}
		for i in range(len(collectionColumnMappings)):
			formattedCollection[collectionColumnMappings[i]] = collection[i]
		
		return formattedCollection



#loads a list of collections for the product collections page
def loadCollections(productDatabase):	
	try:
		productDatabase.execute("SELECT collection_id,Title,BodyHTML,CollectionImageSrc,Published,Conditions,Strict,URL,Meta,PageTitle,Template,resources FROM collections;")
	except Exception as e:
		return None
	collectionList = productDatabase.fetchall()

	if collectionList:
		formattedCollectionList = []

		for i in range(len(collectionList)):
			formattedCollectionList.append({})
			for j in range(len(collectionColumnMappings)):
				formattedCollectionList[i][collectionColumnMappings[j]] = collectionList[i][j]

		return formattedCollectionList
	else:
		return None




#load products meeting certain conditions
def loadProductsInCollection(conditions, productDatabase):
	formattedConditions = ""
	conditions = conditions.split(";")
	for i in range(len(conditions)):
		currentCondition = conditions[i].split(":")

		if len(currentCondition) > 1:
			field = currentCondition[0]
			rule = currentCondition[1]
			value = currentCondition[2]

			rule = collectionRuleMappings[rule]

			if (field == "Tags"):
				rule = " LIKE "
			
			if rule == " LIKE ":
				value = "%" + value + "%"
			

			if productFieldMapping[field] == "TEXT":
				value = "\"" + value + "\""
			elif productFieldMapping[field] == "INTEGER" or productFieldMapping[field] == "REAL":
				value = value
			else:
				value = "\"" + value + "\""

			currentCondition = field + rule + value
			formattedConditions += currentCondition
			formattedConditions += " AND "
		else:
			del conditions[i]

	formattedConditions = formattedConditions[:-5]
	currentQuery = 'SELECT product_id FROM products WHERE %s;' % formattedConditions
	
	try:
		productDatabase.execute(currentQuery)
	except Exception as e:
		return None

	products = productDatabase.fetchall()
	productIDList = [product_id[0] for product_id in products]

	productDict = {}
	if products:
		for product_id in productIDList:
			productDict[product_id] = (loadProduct(product_id, productDatabase))

		return productDict
	else:
		return None


def saveProductTags(product_id, product_tags, productDatabase):
	currentQuery = "UPDATE products SET Tags=%s WHERE product_id=%s;"

	try:
		productDatabase.execute(currentQuery, (product_tags, product_id,))
	except Exception as e:
		print "Error: ", e
		return None

	return True




def saveProductTypes(product_types, productDatabase):
	currentQuery = "UPDATE settings SET FieldList=%s WHERE setting_id='Types';"

	try:
		productDatabase.execute(currentQuery, (product_types, ))
	except Exception as e:
		print "Error: ", e
		return None

	return True




def loadProductTags(productDatabase):
	currentQuery = "SELECT FieldList FROM settings WHERE setting_id='Tags';";
	
	try:
		productDatabase.execute(currentQuery);
	except Exception as e:
		return None

	tags = productDatabase.fetchone()
	if tags:
		tags = set(filter(lambda t: t != '', sorted(tags[0].split(','))))
		print "all:", tags
		return tags



def loadProductTypes(productDatabase):
	currentQuery = "SELECT FieldList FROM settings WHERE setting_id='Types';"	
	try:
		productDatabase.execute(currentQuery);
	except Exception as e:
		return None

	types = productDatabase.fetchone()
	if types:
		types = set(filter(lambda t: t != '', sorted(types[0].split(','))))
		print "all:", types
		return types



#returns a list of product variants given a product id 
def findProductVariants(product_id, productDatabase):
	currentQuery = "SELECT variant_id FROM product_variants WHERE product_id = '%s';"

	try:
		productDatabase.execute(currentQuery, (product_id,))
	except Exception as e:
		print "Error: ", e
		return None

	variants = productDatabase.fetchall()
	variantIDList = []

	if variants:
		for i in range(len(variants)):
			variantIDList.append(variants[i][0])
		return variantIDList
	else:
		return None



def findTotalProductStock(product_id, productDatabase):
	currentQuery = "SELECT VariantInventoryQty FROM product_variants WHERE product_id=%s;"
	try:
		productDatabase.execute(currentQuery, (product_id,))
	except Exception as e:
		print e

	stockList = productDatabase.fetchall()
	if stockList:
		variantCount = len(stockList)
		totalStock = reduce(lambda x,y: x+y, [int(stock[0]) for stock in stockList])

		return (variantCount, totalStock)



#save changes to product description, title, and other things later on
def saveProductData(productData, productDatabase):
	orderedFields = collections.OrderedDict()
	fieldUpdates = ""
	
	for field, value in productData.iteritems():
		#ensures that data types are preserved properly
		if field == "product_id":
			product_id = int(value)
			continue
		else:	
			orderedFields[field] = value
			fieldUpdates += field + "=%s," 

	fieldUpdates = fieldUpdates[:-1]

	valueList = [value for field, value in orderedFields.iteritems()]
	valueList.append(product_id)

	currentQuery = "UPDATE products SET %s WHERE product_id =" % fieldUpdates	#pop in the fieldUpdates for this query
	currentQuery += " %s;" 

	print currentQuery,":", valueList

	try:
		productDatabase.execute(currentQuery, valueList)		#run current query
	except Exception as e:
		print "Exception:", e


def saveProductVariantTypes(product_id, variantTypes, productDatabase):
	currentQuery = """UPDATE products SET VariantTypes = '%s' WHERE product_id=%s;"""

	formattedVariantTypes = ""

	for variantType, values in variantTypes.iteritems():
		formattedVariantTypes += variantType +  ":" +  ",".join(values) + ";"

	try:
		productDatabase.execute(currentQuery, (formattedVariantTypes[:-1], product_id,))
	except Exception as e:
		print e

	# delete old variants that are incompatible
	if formattedVariantTypes != "":
		deleteInvalidVariants(product_id, productDatabase)
	else:
		deleteAllVariants(product_id, productDatabase)


def deleteAllVariants(product_id, productDatabase):
	currentQuery = "DELETE FROM product_variants WHERE product_id=%s;"
	try:
		productDatabase.execute(currentQuery, (product_id,))
	except Exception as e:
		print "Exception: ", e



def deleteInvalidVariants(product_id, productDatabase):
	currentQuery = "SELECT VariantTypes FROM products WHERE product_id=%s;"
	try:
		productDatabase.execute(currentQuery, (product_id,))
	except Exception as e:
		print "Exception: ", e

	variantTypes = productDatabase.fetchone()
	if variantTypes:
		variantTypes = variantTypes[0].split(';')

	currentVariantTypes = {}

	for variantType in variantTypes:
		variantType = variantType.split(':')
		option = variantType[0]
		values = variantType[1].split(',')
		currentVariantTypes[option] = values

	variants = loadProductVariants(product_id, productDatabase)

	if variants:
		for variant in variants:
			currentOptions = variant["VariantData"].split(';')
			for option in currentOptions:
				option = option.split(':')
				optionName = option[0]
				optionValue = option[1]
				if optionValue not in currentVariantTypes[optionName]:
					deleteVariant(variant["variant_id"], productDatabase)
					continue



#saves a new product to the database
def saveNewProductData(productData, productDatabase):
	currentQuery = "INSERT INTO products(Title, ImageSrc) VALUES(%s, %s);"
	defaultImageID = "1"

	productTuple = (productData["Title"], defaultImageID, )
	
	try:
		print "query:", currentQuery 
		productDatabase.execute(currentQuery, productTuple)
	except Exception as e:
		print "Error creating product: ", e

	try:
		productDatabase.execute("SELECT LAST_INSERT_ID();")
	except Exception as e:
		print "Exception: ", e

	product_id = productDatabase.fetchone()[0]
	print "last insert id: ", product_id
	currentQuery = """UPDATE products SET VariantSKU=%s WHERE product_id = %s;"""

	try:
		productDatabase.execute(currentQuery, (product_id, product_id,)) 
	except Exception as e:
		print e

	if product_id:
		return product_id




# save a new type of product variant based on variant options specified in product editor
def saveNewVariantData(product_id, variantData, productDatabase):
	currentQuery = """INSERT into product_variants(product_id, VariantSKU, VariantData, VariantPrice, VariantImg, VariantRequiresShipping, VariantWeightUnit) VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s');"""
	productData = loadProduct(product_id, productDatabase)
	
	formattedVariantData = ""
	formattedVariantSKU = str(product_id)

	for variantOption, variantValue in variantData.iteritems():
		formattedVariantData += variantOption + ":" + variantValue + ";"
		formattedVariantSKU += "-" + variantValue.replace(' ','-').lower()

	try:
		productDatabase.execute(currentQuery, (product_id, formattedVariantSKU, formattedVariantData[:-1], productData["VariantPrice"], productData["ImageSrc"], "true", "lb"))
	except Exception as e:
		print "Error: ", e





#saves a new colleciton to the database
def saveNewCollectionData(collectionData, productDatabase):
	currentQuery = """INSERT INTO collections(Title, Conditions, Published, CollectionImageSrc) VALUES('%s','%s','%s','%s');"""
	defaultCollectionImage = "1"
	collectionTuple = (collectionData["Title"], collectionData["Conditions"], collectionData["Published"], defaultCollectionImage)
	
	try:
		productDatabase.execute(currentQuery, collectionTuple)
	except Exception as e:
		print e

	try:
		productDatabase.execute("SELECT collection_id FROM collections WHERE Title='%s';", (collectionData["Title"],))
	except Exception as e:
		print e

	collection_id = productDatabase.fetchone()
	
	if collection_id:
		return collection_id[0]



#save changes from product inventory editor
def saveProductInventoryData(variantData, productDatabase):
	currentQuery = """UPDATE product_variants SET VariantPrice = '%s', VariantCompareAtPrice = '%s', VariantBarcode = '%s', VariantSKU = '%s', VariantInventoryQty = '%s' WHERE variant_id=%s;"""
	productTuple = (variantData["VariantPrice"], variantData["VariantCompareAtPrice"], variantData["VariantBarcode"], variantData["VariantSKU"], variantData["VariantInventoryQty"], variantData["variant_id"])
	
	try:
		productDatabase.execute(currentQuery, productTuple)
	except Exception as e:
		print "Exception: ", e



#update collection data, including conditions
def saveCollectionData(collectionData, productDatabase):
	fieldUpdates = ""
	
	for field, value in collectionData.iteritems():
		#ensures that data types are preserved properly
		if field == "collection_id":
			collection_id = int(value)
			continue
		if collectionFieldMapping[field] == "TEXT":
			fieldUpdates += (field + "=\"" + value + "\",")
		elif collectionFieldMapping[field] == "INTEGER":
			fieldUpdates += (field + "=" + str(value) + ",")
		elif collectionFieldMapping[field] == "REAL":
			fieldUpdates += (field + "=" + str(value) + ",")
		else:
			fieldUpdates += (field + "=\"" + value + "\",")

	fieldUpdates = fieldUpdates[:-1] 	#remove the last comma
	currentQuery = "UPDATE collections SET '%s' WHERE collection_id = '%s';" % (fieldUpdates,collection_id)	#pop in the fieldUpdates for this query
			
	try:
		productDatabase.execute(currentQuery)		#run current query
	except Exception as e:
		print "Exception:", e



def setDefaultProductImage(product_id, resource_id, productDatabase):
	currentQuery = "UPDATE products SET ImageSrc=%s WHERE product_id=%s;"
	try:
		productDatabase.execute(currentQuery, (resource_id, product_id, ))
	except Exception as e:
		print "Exception: ", e
		return None

	return True


def updateProductResources(product_id, resource_id, resource_type, productDatabase):
	currentQuery = "SELECT resources FROM products WHERE product_id=%s;"
	try:
		productDatabase.execute(currentQuery, (product_id,))
	except Exception as e:
		print "Exception: ", e
		return None

	resourceDict = {}

	resources = productDatabase.fetchone()[0]
	if resources:
		resources=filter(lambda r: r != '', resources.split(','))
		
		for resource in resources:
			resource = resource.split(':')
			if resource[0] in resourceDict:
				resourceDict[resource[0]] += " " + resource[1]
			else:
			 	resourceDict[resource[0]] = resource[1]

		resourceDict[resource_type] += " " + str(resource_id)
	elif resources is None or resources == "":
		resourceDict[resource_type] = str(resource_id)
		#if this is the first picture they upload, set it to default
		if(resource_type) == "product_image":
			setDefaultProductImage(product_id, resource_id, productDatabase)

	formattedResourceString = ""

	for resource_type, resource_ids in resourceDict.iteritems():
		formattedResourceString += (resource_type + ":" + resource_ids + ",") 


	currentQuery = "UPDATE products SET resources=%s WHERE product_id=%s;"
	print "Query:", currentQuery
	try:
		productDatabase.execute(currentQuery,(formattedResourceString, product_id, ))
	except Exception  as e:
		print "Exception: ", e
		return None

	return True



def updateCollectionImage(collection_id, resource_id, productDatabase):
	currentQuery = "UPDATE collections SET CollectionImageSrc=%s WHERE collection_id=%s;"

	try:
		productDatabase.execute(currentQuery,(str(resource_id), collection_id, ))
	except Exception  as e:
		print "Exception: ", e
		return None

	return True


#deletes a single product from the database
def deleteProduct(product_id, productDatabase):	
	try:
		productDatabase.execute("DELETE FROM products WHERE product_id=%s;",(product_id,))
		productDatabase.execute("DELETE FROM product_variants WHERE product_id=%s;", (product_id,))
	except Exception as e:
		print "Exception:", e
		return None

	return True

#deletes a single collection from the database
def deleteCollection(collection_id, productDatabase):	
	try:
		productDatabase.execute("DELETE FROM collections WHERE collection_id=%s;",(collection_id,))
	except Exception as e:
		print "Exception:", e
		return None

	return True



#deletes a single variant from the database
def deleteVariant(variant_id, productDatabase):
	currentQuery = "DELETE FROM product_variants WHERE variant_id=%s;"
	try:
		productDatabase.execute(currentQuery,(variant_id, ))
	except Exception as e:
		print e
		return None

	return True



#placeholder function to import data from an exported store such as shopify
def importProductsFromCSV(f):
	productList = []
	f = open(f, 'rt')
	try:
	    reader = csv.reader(f)
	    for row in reader:
	        productList.append(row)
	finally:
	    f.close()
	return productList



#another placeholder to create the initial records in the table, for experimentation
def insertProducts(products, tableName, productDatabase):
	for i in range(1,len(products)):
		currentQuery = """INSERT INTO products(product_handle,Title,BodyHTML,Stock,Vendor,BasePrice,Type,Tags,Published,Option1Name,Option1Value,Option2Name,Option2Value,Option3Name,Option3Value,VariantSKU,
		VariantGrams,VariantInventoryTracker,VariantInventoryQty,VariantInventoryPolicy,VariantFulfillmentService,VariantPrice,VariantCompareAtPrice,
		VariantRequiresShipping,VariantTaxable,VariantBarcode,ImageSrc,ImageAltText,GiftCard,SEOTitle,SEODescription,GoogleShopping_Google_Product_Category,
		GoogleShopping_Gender,GoogleShopping_Age_Group,GoogleShopping_MPN,GoogleShopping_AdWords_Grouping,GoogleShopping_AdWords_Labels,GoogleShopping_Condition,
		GoogleShopping_Custom_Product,GoogleShopping_Custom_Label_0,GoogleShopping_Custom_Label_1,GoogleShopping_Custom_Label_2,GoogleShopping_Custom_Label_3,
		GoogleShopping_Custom_Label_4,VariantImage,VariantWeightUnit,VariantTaxCod,IsDefaultProduct)
		VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');"""

		try:
			productDatabase.execute(currentQuery, tuple(products[i]))
		except Exception as e:
			print e



def bulkUpdateProducts(productData, productDatabase):
	#iterates through a dictionary of product data and updates product db

	#product data is represented as a dictionary of dictionaries, with each field in the main dict representing a different product
	for product_id, currentProductData in productData.iteritems():				
		fieldUpdates = ""

		#each subdictionary contains fields correspending to database columns to allow easy indexing and dynamic query building
		for field, value in currentProductData.iteritems():
			
			#ensures that data types are preserved properly
			if productFieldMapping[field] == "TEXT":
				fieldUpdates += (field + "=\"" + value + "\",")
			elif productFieldMapping[field] == "INTEGER":
				fieldUpdates += (field + "=" + value + ",")
			elif productFieldMapping[field] == "REAL":
				fieldUpdates += (field + "=" + value + ",")
			else:
				fieldUpdates += (field + "=\"" + value + "\",")

		fieldUpdates = fieldUpdates[:-1] 	#remove the last comma
		currentQuery = "UPDATE products SET '%s' WHERE product_id = '%s';" % (fieldUpdates, product_id)	#pop in the fieldUpdates for this query
		
		try:
			productDatabase.execute(currentQuery)		#run current query
		except Exception as e:
			print e


def bulkUpdateVariants(variantData, productDatabase):
	#iterates through a dictionary of product data and updates product db

	#variant data is represented as a dictionary of dictionaries, with each field in the main dict representing a different product
	for variant_id, currentVariantData in variantData.iteritems():				
		fieldUpdates = ""

		#each subdictionary contains fields correspending to database columns to allow easy indexing and dynamic query building
		for field, value in currentVariantData.iteritems():
			
			#ensures that data types are preserved properly
			if variantFieldMapping[field] == "TEXT":
				fieldUpdates += (field + "=\"" + value + "\",")
			elif variantFieldMapping[field] == "INTEGER":
				fieldUpdates += (field + "=" + value + ",")
			elif variantFieldMapping[field] == "REAL":
				fieldUpdates += (field + "=" + value + ",")
			else:
				fieldUpdates += (field + "=\"" + value + "\",")

		fieldUpdates = fieldUpdates[:-1] 	#remove the last comma
		currentQuery = "UPDATE product_variants SET '%s' WHERE variant_id = '%s';" % (fieldUpdates,variant_id)	#pop in the fieldUpdates for this query
		
		print currentQuery
		try:
			productDatabase.execute(currentQuery)		#run current query
		except Exception as e:
			print e


def bulkUpdateCollections(collectionData, productDatabase):
	#iterates through a dictionary of collection data and updates product db

	#collection data is represented as a dictionary of dictionaries, with each field in the main dict representing a different product
	for collection_id, currentCollectionData in collectionData.iteritems():				
		fieldUpdates = ""

		#each subdictionary contains fields correspending to database columns to allow easy indexing and dynamic query building
		for field, value in currentCollectionData.iteritems():
			
			#ensures that data types are preserved properly
			if collectionFieldMapping[field] == "TEXT":
				fieldUpdates += (field + "=\"" + value + "\",")
			elif collectionFieldMapping[field] == "INTEGER":
				fieldUpdates += (field + "=" + value + ",")
			elif collectionFieldMapping[field] == "REAL":
				fieldUpdates += (field + "=" + value + ",")
			else:
				fieldUpdates += (field + "=\"" + value + "\",")

		fieldUpdates = fieldUpdates[:-1] 	#remove the last comma
		currentQuery = "UPDATE collections SET '%s' WHERE collection_id = '%s';" % (fieldUpdates, collection_id)	#pop in the fieldUpdates for this query
		
		print currentQuery
		try:
			productDatabase.execute(currentQuery)		#run current query
		except Exception as e:
			print e

		


#sets all products in the list of product ids to either published or hidden (based on value="true" or "false")
def bulkPublish(value, product_id_list, productDatabase):
	product_id_list = map(int, product_id_list)

	placeholder = "%s"
	placeholders = ','.join(placeholder for unused in product_id_list)

	values = [value] + product_id_list
	
	currentQuery = "UPDATE products SET Published = '%s' WHERE product_id IN (%s);" % (placeholders, values)

	try:
		productDatabase.execute(currentQuery)
	except Exception as e:
		print e




#deletes a product and all of it's variants from the database
def bulkDelete(products, productDatabase):
	products = map(int, products)
	placeholder = "%s"
	fullProductList = []

	for i in range(len(products)):
		productData = loadProduct(products[i], productDatabase)
		variantIDList = findProductVariants(products[i], productDatabase)
		if variantIDList:
			fullProductList += variantIDList
	
	if fullProductList != []:
		placeholders = ','.join(placeholder for unused in fullProductList)
		currentQuery = "DELETE FROM products WHERE product_id IN (%s);" % placeholders
		values = fullProductList
	else:
		placeholders = ','.join(placeholder for unused in products)
		currentQuery = "DELETE FROM products WHERE product_id IN (%s);" % placeholders
		values = products
	
	try:
		productDatabase.execute(currentQuery, values)
	except Exception as e:
		print e
	



