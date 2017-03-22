import sqlite3,sys,csv,json

#config current only has column/field mapping information, which will be specific to the import form (of the product csv), e.g. shopify
from config import *	
import product
from order import *
#from product_util import *



def createResource(resource_URI, resource_type, database):
	currentQuery = "INSERT INTO resources(resource_uri, resource_type) VALUES(%s,%s);"

	try:
		database.execute(currentQuery, (resource_URI, resource_type,))
	except Exception as e:
		print "Exception: ", e
		return None

	try:
		database.execute("SELECT LAST_INSERT_ID();")
	except Exception as e:
		print "Exception: ", e

	resource_id = database.fetchone()[0]

	if resource_id:
		return resource_id
	else:
		return None



def loadResourceURI(resource_id, database):
	currentQuery = "SELECT resource_uri FROM resources WHERE resource_id=%s;"

	try:
		database.execute(currentQuery, (resource_id, ))
	except Exception as e:
		print "Exception: ", e
		return None

	resource_uri = database.fetchone()

	if resource_uri:
		return resource_uri[0]
	return None



def deleteResource(resource_id, database):
	currentQuery = "DELETE FROM resources WHERE resource_id=%s;"
	
	try:
		database.execute(currentQuery,(resource_id, ))
	except Exception as e:
		print "Error: ", e
		return False

	return True


# deletes a batch of resources by id

def bulkDeleteResources(resource_id_list, database):
	resource_id_list = map(int, resource_id_list)

	placeholder = '%s'
	placeholders = ','.join(placeholder for unused in resource_id_list)

	currentQuery = "DELETE FROM resources WHERE resource_id IN(%s);" % placeholders

	try:
		database.execute(currentQuery, resource_id_list)
	except Exception as e:
		print "Error: ", e
		return False

	return True


def loadResourcesByType(resource_type, database):
	currentQuery = """SELECT resource_uri, resource_id FROM resources WHERE resource_type='%s';"""
	try:
		database.execute(currentQuery, (resource_type, ))
	except Exception as e:
		print "Error: ", e
		return None

	resource_list = database.fetchall()
	if resource_list:
		resource_dict = {}
		for resource in resource_list:
			resource_uri = resource[0]
			resource_id = resource[1]
			resource_dict[resource_id] = {}
			resource_dict[resource_id]["uri"] = resource_uri
			
			resource_fname = resource_uri.split('/')
			resource_fname = resource_fname[len(resource_fname)-1]

			resource_ext = (resource_fname.split('.')[1]).upper()

			resource_dict[resource_id]["filename"] = resource_fname
			resource_dict[resource_id]["filetype"] = resource_ext

		return resource_dict
	
	return None



def deleteProductResource(product_id, resource_id, resource_type, database):
	productData = product.loadProduct(product_id, database)

	if "resources" in productData:
		currentResourceValue = ""

		product_resources = filter(lambda r: r != '', productData["resources"].split(','))
		for index, resource in enumerate(product_resources):
			resource = resource.split(':')

			if resource[0] == resource_type:
				currentResourceType = resource[0]
				currentResourceValues = sorted(set(filter(lambda r: r!='', resource[1].split(" "))))

		currentIndex = currentResourceValues.index(resource_id)
		del currentResourceValues[currentIndex]

		newResourceValues = " ".join(currentResourceValues)

		if newResourceValues == "" and resource_type == "product_image":
			formattedProductResources = ""

		else:
			newResourceString = resource_type + ":" + newResourceValues
			product_resources[index] = newResourceString
			formattedProductResources = ",".join(product_resources) + ","

		try:
			#check if the resource they are deleting is the default product image resource, if so, choose a new resource automatically
			if(resource_id == productData["ImageSrc"]):
				if len(currentResourceValues) > 0:
					newDefaultImage = currentResourceValues[0]
				else:
					newDefaultImage = "1"
				#update main product image	
				database.execute("UPDATE products SET ImageSrc=%s WHERE product_id=%s;", (newDefaultImage, product_id,))

			#update resources
			database.execute("UPDATE products SET resources=%s WHERE product_id=%s;", (formattedProductResources, product_id,))
		except Exception as e:
			print "Error: ", e
			return None

		return True

	else:	
		return None

def loadResourceURIList(resourceID_list, database):
	resourceIDs = ','.join(resourceID_list)

	currentQuery = "SELECT resource_id,resource_uri FROM resources WHERE resource_id IN(%s);" % resourceIDs

	try:
		database.execute(currentQuery)
	except Exception as e:
		print "Exception: ", e
		return None

	resource_uri_list = database.fetchall()
	
	if resource_uri_list:
		return resource_uri_list

	return None