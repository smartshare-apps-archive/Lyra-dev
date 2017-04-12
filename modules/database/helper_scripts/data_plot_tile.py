"""
	basic data plot tile class, any extra functionality can be added to the helper script that inherits from this
	the basic gist is that any post processing of requirement data/data sourcing can be added into a helper script class 
	so long as the basic structure and flow remains the same 

"""
import collections
import requests

import numpy as np
import json


class data_plot_tile(object):
	
	def __init__(self, data_endpoint, template_file, data_sources):
		self.data_endpoint = data_endpoint
		self.template_file = template_file
		self.data_sources = data_sources
		self.possible_operations = collections.OrderedDict()


	def get_plot_data(self):
		r = requests.get(self.data_endpoint)

		if r.status_code == 200:
			plot_data = json.loads(r.text)
			formatted_plot_data = np.array(plot_data)
			self.plot_data = formatted_plot_data
		else:
			self.plot_data = None
		

	def set_database(self, database):
		self.database = database


	def load_data_sources(self, source_handles):
		self.source_handles = source_handles
		
	
	def run_script(self):
		self.get_plot_data()	
		self.format_plot_data()
		self.register_operations()	#registers the list of operations to be performed on the data
		self.run_operations()	# runs the data operations

		self.create_plot()
		self.populate_template_data()



	def populate_template_data(self):
		self.template_data = {}

		self.template_data["plot_script"] = self.script
		self.template_data["plot_div"] = self.div

		return self.template_data


	def format_plot_data(self):
		""" child overrides with custom plot data """
		pass


	def create_plot(self):
		""" child overrides with custom plot data """
		pass

	def register_operations(self):
		""" child class overrides this with custom functionality """
		pass


	#runs a specific operation on the data
	def run(self, op):
		return self.possible_operations[op]()


	#runs all registered data operations
	def run_operations(self):
		for op, fn in self.possible_operations.iteritems():
			self.run(op)


