		plot = figure(responsive=True)
		plot.logo = None #removes bokeh logo
		plot.xaxis.axis_label = 'Day'
		plot.yaxis.axis_label = 'Sales'

		plot.line([1,2,3,4,5,6,7,8], [3,4,1,6,1,8,1,9])

		script, div = components(plot)

		self.control_data["plot_script"] = script
		self.control_data["plot_div"] = div