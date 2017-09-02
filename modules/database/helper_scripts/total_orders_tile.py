import imp

from data_feed_tile import *


class total_orders_tile(data_feed_tile):
    def __init__(self, query_file, template_file, data_sources):
        super(total_orders_tile, self).__init__(query_file, template_file, data_sources)

    # a data operation must be registered here in order for it to run, they execute in the order they are inserted into the dictionary
    def register_operations(self):
        self.possible_operations["calculate_total_sales"] = self.calculate_total_sales

    # sums up all of the order sales
    def calculate_total_sales(self):
        self.template_data["sum_order_totals"] = 0.00

        order_totals = self.template_data.get("order_totals", None)

        if order_totals:
            for total in self.template_data["order_totals"]:
                total = total[0]
                self.template_data["sum_order_totals"] += total
