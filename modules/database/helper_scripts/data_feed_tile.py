"""
	basic data feed tile class, any extra functionality can be added to the helper script that inherits from this
	the basic gist is that any post processing of requirement data/data sourcing can be added into a helper script class 
	so long as the basic structure and flow remains the same 

"""
import collections


class data_feed_tile(object):
    def __init__(self, query_file, template_file, data_sources):
        self.query_file = query_file
        self.template_file = template_file
        self.data_sources = data_sources
        self.possible_operations = collections.OrderedDict()

    def parse_query_file(self):
        self.query_list = {}

        with open('modules/database/query_files/' + self.query_file, 'r') as f:
            for line in f:
                parsed_line = line.split('<query_split>')
                name = parsed_line[0]
                query = parsed_line[1]

                self.query_list[name] = query

    def set_database(self, database):
        self.database = database

    def load_data_sources(self, source_handles):
        self.source_handles = source_handles

    def run_script(self):
        self.parse_query_file()  # cycle through file and parse out data source ids and the queries
        self.run_query_list()  # run all the queries in the lsql file associated with this tile
        self.populate_template_data()  # grabs all of the initial template data, before operations are performed on it

        self.register_operations()  # registers the list of operations to be performed on the data
        self.run_operations()  # runs the data operations

    # runs all the queries stored in the corresponding "lsql" file
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

    # fills unmodified data from queries
    def populate_template_data(self):
        self.template_data = {}

        for query_name, result in self.data.iteritems():
            self.template_data[query_name] = result

        return self.template_data

    # runs a specific operation on the data
    def run(self, op):
        return self.possible_operations[op]()

    # runs all registered data operations
    def run_operations(self):
        for op, fn in self.possible_operations.iteritems():
            self.run(op)
