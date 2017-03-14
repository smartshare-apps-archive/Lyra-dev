#a basic cart object implementing redis

import json, time

from flask import Blueprint, render_template, current_app, session, request, Markup
from uuid import uuid4
import redis

#ecomm module imports
from modules.db import *
from modules.database.store import *
import modules.database.order


CartMessage = {
			'CART_EXISTS':None,	
			'CART_EMPTY':"empty"
			}

class CartManager(object):

	def __init__(self, app, session_interface):
		self.s = session_interface
		self.app = app
		self.cart = None

	
	#creates a new cart list if none exists, or returns 
	def getCartContents(self, session):
		data = {}
		data["table"] = "cart:" + session['user_session']
		
		cart = self.s.get_session_hashTable(self.app, session, data)

		if cart is not []:
			self.cart = self.s.get_session_hashTable(self.app, session, data)
			return self.cart
		else:
			return None


		#adds an item to the cart
	def addItem(self, session, data):
		prefix = "cart:"
		data = data.split(';')
		item = data[0]
		quantity = data[1]

		currentContents = self.getCartContents(session)

		data = {}
		data["table"] = prefix + session['user_session']
		data["key"] = item
		data["value"] = quantity

		result = self.s.set_session_hashKey(self.app, session, data)
		currentContents = self.getCartContents(session)
		
		print "After contents: ", currentContents
		return result



	def deleteItem(self, session, data):
		prefix = "cart:"
		item = data
		currentContents = self.getCartContents(session)
		
		data = {}
		data["table"] = prefix + session['user_session']
		data["key"] = item

		result = self.s.delete_session_hashKey(self.app, session, data)
		currentContents = self.getCartContents(session)
		
		print "After contents: ", currentContents
		return result


	def updateItem(self, session, data):
		prefix = "cart:"
		data = data.split(';')
		item = data[0]
		quantity = data[1]

		currentContents = self.getCartContents(session)

		data = {}
		data["table"] = prefix + session['user_session']
		data["key"] = item
		data["value"] = quantity

		if(quantity == '0'):
			result = self.s.delete_session_hashKey(self.app, session, data)
		else:
			result = self.s.set_session_hashKey(self.app, session, data)
		
		currentContents = self.getCartContents(session)
		
		print "After contents: ", currentContents
		return result
