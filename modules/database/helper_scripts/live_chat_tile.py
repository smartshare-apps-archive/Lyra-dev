import imp

from data_feed_tile import *


class live_chat_tile(data_feed_tile):
    def __init__(self, query_file, template_file, data_sources):
        super(live_chat_tile, self).__init__(query_file, template_file, data_sources)

    # a data operation must be registered here in order for it to run, they execute in the order they are inserted into the dictionary
    def register_operations(self):
        pass
