from flask import render_template, Markup

#ecomm module imports
import database.config as config
from database.product import *
from database.order import *
from database.product_util import *
from database.order_util import *
from database.store import *
from store.store_util import *

from db import *

import sqlite3, sys


class Auth(object):
	def __init__(self):
		self.setupVariables()

	def setupVariables(self,):
		self.store_data = {}


	def render_tab(self, tab, data=None):
		instance_db = instance_handle()
		db = db_handle(instance_db)

		self.database = db.cursor()

		#store sections
		if tab == "login":
			return self.Login()
		elif tab == "nav_bar":
			return self.NavBar(data)

		self.database = None
		db.close()	



	def Login(self):
		self.store_data["login_panel"] = render_template('auth/login_panel.html')

		return self.store_data






