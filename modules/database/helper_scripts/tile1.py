from flask import render_template
import imp

from data_feed_tile import *


class tile1(data_feed_tile):
	def __init__(self, query_file, template_file, data_sources):
		super(tile1, self).__init__(query_file, template_file, data_sources)


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
		print "Loaded: ", self.source_handles


	def run_query_list(self):
		self.data = {}

		for query_name, query in self.query_list.iteritems():
			try:
				self.database.execute(query)
			except Exception as e:
				print "Error executing query: ", e

			results = self.database.fetchall()
			if results:
				self.data[query_name] = results


	def populate_template_data(self):
		self.template_data = {}

		for query_name, result in self.data.iteritems():
			self.template_data[query_name] = result

		return self.template_data
