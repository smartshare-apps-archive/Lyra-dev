from resources import *


def formatCollectionConditions(collectionConditions):
	if type(collectionConditions) == type(None):
		return ""

	conditionsString = ""

	for condition_id, condition in collectionConditions.iteritems():
		conditionsString += condition["type"] + "<field_split>" + condition["rule"] + "<field_split>" + condition["value"] + "<condition_split>"

	return conditionsString



def formatProductTags(product_tags):
	product_tags = sorted(product_tags.split(','))
	product_tags = set(filter(lambda t: t!='', product_tags))
	return product_tags


def formatProductTypes(product_types):
	product_types = sorted(product_types.split(','))
	product_types = set(filter(lambda t: t!='', product_types))
	return product_types


def formatVariantData(variantTypeData):
	variantTypeData = variantTypeData.split(';')
	formattedVariantTypeData = {}

	for variantType in variantTypeData:
		variantOption = variantType.split(':')[0]
		variantValue = variantType.split(':')[1]
		formattedVariantTypeData[variantOption] = variantValue

	return formattedVariantTypeData



def extractImageResources(resources):
	resources = filter(lambda r: r != '', resources.split(','))
	for r in resources:
		r = r.split(':')
		if r[0] == "product_image":
			resource_ids = r[1].split(' ')			
			return resource_ids
		elif r[0] == "collection_image":
			resource_ids = r[1].split(' ')			
			return resource_ids		

	return None


def formatImageURIs(imageURI):
	formattedURI = {}
	
	for uri in imageURI:
		formattedURI[uri[0]] = uri[1]

	return formattedURI


def loadProductImages(products, productDatabase):
	image_resources = {}
	
	for product_id, product in products.iteritems():
		if product.has_key("resources"):
			if(product["resources"] is not None and product["resources"] != ""):
				imageResources = extractImageResources(product["resources"]) #gets image resource id list from resource database
				imageURI = loadResourceURIList(imageResources, productDatabase)
				imageURI = formatImageURIs(imageURI)

				image_resources[product_id] = imageURI[int(product["ImageSrc"])] #so the product editor can access those image resources
		else:
			image_resources[product_id] = None  #so the product editor can access those image resource_ids

	return image_resources