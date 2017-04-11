import imp
import numpy as np


from bokeh.plotting import figure
from bokeh.embed import components


from data_plot_tile import *

class sample_plot(data_plot_tile):
	def __init__(self, query_file, template_file, data_sources):
		super(sample_plot, self).__init__(query_file, template_file, data_sources)
	


	def format_plot_data(self):
		self.formatted_plot_data = {}

		self.formatted_plot_data["x"] = self.plot_data[0]
		self.formatted_plot_data["y"] = self.plot_data[1]



	# a data operation must be registered here in order for it to run, they execute in the order they are inserted into the dictionary
	def register_operations(self):
		self.flags = {}
		self.possible_operations["flag_plot"] = self.flag_plot



	def flag_plot(self):
		maxVal = np.amax(self.formatted_plot_data["x"])
		print "Max val: ", maxVal
		if maxVal >= 4:
			self.flags["max_passed"] = True
		else:
			self.flags["max_passed"] = False




	def create_plot(self):
		plot = figure(plot_width=960, plot_height=300, responsive=True)

		plot.logo = None #removes bokeh logo

		if(self.flags["max_passed"]):
			plot.xaxis.axis_label = 'max passed'
		else:
			plot.xaxis.axis_label = 'x'

		plot.yaxis.axis_label = 'y'

		x_data = self.formatted_plot_data["x"]
		y_data = self.formatted_plot_data["y"]
		



		#plot.line(x_data, y_data)
		plot.vbar(x=x_data, width=0.5, bottom=0,
		top=y_data, color="firebrick")

		script, div = components(plot)

		self.script = script
		self.div = div



