"""
	basic data feed tile class, any extra functionality can be added to the helper script that inherits from this
	the basic gist is that any post processing of requirement data/data sourcing can be added into a helper script class 
	so long as the basic structure and flow remains the same 

"""

class data_feed_tile(object):
	
	def __init__(self, query_file, template_file, data_sources, data_operations):
		self.query_file = query_file
		self.template_file = template_file
		self.data_sources = data_sources
		self.possible_operations = {}


	def parse_query_file(self):
		self.query_list = {}

		with open('modules/database/query_files/'+self.query_file, 'r') as f:
			for line in f:
				parsed_line = line.split('<query_split>')
				name = parsed_line[0]
				query = parsed_line[1]

				self.query_list[name] = query


	def set_database(self, database):
		self.database = database


	def load_data_sources(self, source_handles):
		self.source_handles = source_handles
		


	def run_query_list(self):
		self.data = {}

		for query_name, query in self.query_list.iteritems():
			try:
				self.database.execute(query)
			except Exception as e:
				print "Error executing query: ", e

			results = self.database.fetchall()
			if results:
				self.data[query_name] = list(results)
				for i in range(len(list(results))):
					temp_data = self.data[query_name][i]
					self.data[query_name][i] = list(temp_data)
				


	def populate_template_data(self):
		self.template_data = {}

		for query_name, result in self.data.iteritems():
			self.template_data[query_name] = result

		return self.template_data


	def run(self, op):
		return self.possible_operations[op]()


	def run_operations(self):
		for op, fn in self.possible_operations.iteritems():
			self.run(op)


