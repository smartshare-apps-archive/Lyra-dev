from flask import render_template, Markup

import collections


def formatProductRows(products):
	maxItemsPerRow = 3

	rowList = []
	currentRow = 0
	cItems = 0
	nProducts = len(products)
	
	rowList.append([])

	if type(products) == type([]):
		print "this is a list"
		for product in products:
			if (cItems == maxItemsPerRow):
				rowList.append([])
				cItems = 0
				currentRow += 1
			
			rowList[currentRow].append(product["product_id"])

			cItems += 1
			nProducts -= 1

	elif type(products) == type({}) or isinstance(products, collections.OrderedDict):
		for product_id, product in products.iteritems():
			if (cItems == maxItemsPerRow):
				rowList.append([])
				cItems = 0
				currentRow += 1
			
			rowList[currentRow].append(product_id)

			cItems += 1
			nProducts -= 1
	else:
		print "Invalid type:", type(products)
		
 	return rowList



def parseAddress(address):
	formattedAddress = {}
	address = address.split(';')
	print address
	for a in address:
		a = a.split(':')

		try:
			formattedAddress[a[0]] = a[1]
		except:
			formattedAddress[a[0]] = ""

	return formattedAddress



def parseDropdownList(navData):
	navData = navData.split('<split>')
	formattedDropdown = {}
	formattedDropdown["links"] = []

	for resource in navData:
		resource = resource.split(':')
		if resource[0] == "title":
			formattedDropdown["title"] = resource[1]
			continue

		formattedDropdown["links"].append(resource)
	return formattedDropdown



#renders a specific page according to the template parameters
def injectPageData(template, pageData):
	return pageData