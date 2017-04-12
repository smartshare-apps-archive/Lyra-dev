import imp
import numpy as np
from datetime import datetime as dt

from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import HoverTool, BoxSelectTool

TOOLS = [BoxSelectTool(), HoverTool()]


from data_plot_tile import *

class sample_plot(data_plot_tile):
	def __init__(self, query_file, template_file, data_sources):
		super(sample_plot, self).__init__(query_file, template_file, data_sources)
	


	def format_plot_data(self):
		self.formatted_plot_data = {}

		self.formatted_plot_data["x"] = map(lambda d: dt(int(d[:4]), int(d[4:6]), int(d[6:8])), self.plot_data[0])
		self.formatted_plot_data["y"] = map(lambda u: int(u), self.plot_data[1])

		print "formatted x plot data:", self.formatted_plot_data["x"]
		print "formatted y plot data:", self.formatted_plot_data["y"]

	# a data operation must be registered here in order for it to run, they execute in the order they are inserted into the dictionary
	def register_operations(self):
		self.flags = {}






	def create_plot(self):
		plot = figure(plot_width=960, plot_height=300, responsive=True, x_axis_type='datetime', tools=TOOLS)

		plot.logo = None #removes bokeh logo

		plot.xaxis.axis_label = 'Date'
		plot.yaxis.axis_label = 'Users'

		x_data = self.formatted_plot_data["x"]
		y_data = self.formatted_plot_data["y"]
		

		#plot.line(x_data, y_data)

		plot.line(x=x_data,y=y_data)

		script, div = components(plot)

		self.script = script
		self.div = div



#	hardware interaction server, arduino, raspberry pie
#   flag evaluation -> neural networks, threshold, other types of classifiers