import sys,csv,json,collections	

from product_util import *
from order_util import *
from dashboard_util import *

import config
import product
import event
import customer


def loadAllVendors(database):
	currentQuery = "SELECT vendor_id, Name, URL, Phone, Email FROM vendors;"

	try:
		database.execute(currentQuery)
	except Exception as e:
		print "Error loading dashboard tiles: ",e
		return None

	vendors = database.fetchall()
	if vendors:
		formattedVendors = {}
		for vendor in vendors:
			current_vendor = str(vendor[0])
			formattedVendors[current_vendor] = {}

			for i in range(len(vendorColumnMappings)):
				formattedVendors[current_vendor][vendorColumnMappings[i]] = vendor[i]
		
		return formattedVendors




def loadVendor(vendor_id, database):
	currentQuery = "SELECT vendor_id, Name, URL, Phone, Email FROM vendors WHERE vendor_id=%s;"

	try:
		database.execute(currentQuery,(vendor_id,))
	except Exception as e:
		print "Error loading dashboard tile: ",e
		return None

	vendor = database.fetchone()

	if vendor:	
		formattedVendor = {}

		for i in range(len(vendorColumnMappings)):
			formattedVendor[vendorColumnMappings[i]] = vendor[i]
		
		return formattedVendor