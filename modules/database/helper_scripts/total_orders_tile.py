import imp

from data_feed_tile import *


class total_orders_tile(data_feed_tile):
	def __init__(self, query_file, template_file, data_sources, data_operations):
		super(total_orders_tile, self).__init__(query_file, template_file, data_sources, data_operations)


	def register_operations(self):
		self.possible_operations["double"] = self.double_orders


	def double_orders(self):
		print "trying to double: ", self.template_data["order_data"][0][0]
		self.template_data["order_data"][0][0] = self.template_data["order_data"][0][0] * 2
