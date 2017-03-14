from flask import render_template, request
import paypalrestsdk
import logging
import collections

paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "Ab1gIE7gbpoBcxgyURdYazh4gtVcTewv7bT_xhZo90-FXO631Fi6xe-L9Ce9KKp9SIEQEtmCzG6A4u_J",
  "client_secret": "EE8nOc2i2GnXnHqS1oqFqIl0bfR6xFf0v6hvRroDNRxYq4AgGCVFgONIlykSSff1gT0kSyE_vP3d-sa8" })


def validate_cc():
	pass


def construct_payment(payment_data):
	pass

def pay(payment_data):
	payment = paypalrestsdk.Payment(payment_data)

	if payment.create():
		#payment.execute()
 		print "created a payment successfully."
 		#payment_history = paypalrestsdk.Payment.all({"count": 10})
 		#print payment_history.payments
 		for link in payment.links:
 			print link, ":", link.method


	else:
		print payment.error

def main():
	#create payment dict
	payment_data = collections.OrderedDict()

	#create cc info
	cc_info = collections.OrderedDict({
		"type": "mastercard",
		"number": "5500000000000004",
		"expire_month": "11",
		"expire_year": "2020",
		"cvv2": "262",
		"first_name": "luke",
		"last_name": "lombardi"
	})
	
	#basic item data dict
	item = collections.OrderedDict({
		"name": "itemtitle",
		"sku": "item_sku",
		"price": "1.00",
		"currency": "USD",
		"quantity": "1"
	})

	#contains data for each item in sale
	item_list = collections.OrderedDict({"items": []})

	#add an item to this list
	item_list["items"].append(item)
	
	#dict for amount data
	amount = collections.OrderedDict({
		"total":"1.00",
		"currency": "USD"
	})

	#first type of intent -> sale
	payment_data["intent"] = "sale"
	
	#create the payer info section
	payment_data["payer"] = collections.OrderedDict({
		#set payment method
		"payment_method": "credit_card",
		"funding_instruments": []
	})

	#add the cc_info the funding instruments
	payment_data["payer"]["funding_instruments"].append({"credit_card": cc_info})

	#add all the above fields to the transactions field
	payment_data["transactions"] = [collections.OrderedDict({
		"item_list": item_list,
		"amount":amount,
		"description":"some description"
	})]

	print payment_data
	pay(payment_data)




if __name__ == "__main__":main()