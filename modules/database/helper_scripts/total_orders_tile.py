from flask import render_template
import imp

from data_feed_tile import *


class total_orders_tile(data_feed_tile):
	def __init__(self, query_file, template_file, data_sources):
		super(total_orders_tile, self).__init__(query_file, template_file, data_sources)


