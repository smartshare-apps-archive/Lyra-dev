import imp

from data_feed_tile import *


class site_visitors_tile(data_feed_tile):
    def __init__(self, query_file, template_file, data_sources):
        super(site_visitors_tile, self).__init__(query_file, template_file, data_sources)
