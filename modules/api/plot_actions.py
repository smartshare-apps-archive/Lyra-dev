import ast, re

from flask import Blueprint, render_template, abort, current_app, session, request


#ecomm module imports
if __name__ != "__main__":

	from modules.db import *
	import modules.database.config as config
	import modules.database.product as product
	import modules.database.resources as resources
	import modules.database.customer as customer
	import modules.database.order as order
	import modules.database.dashboard as dashboard
	import modules.database.store as store

	from modules.database.dashboard_util import *

	from modules.decorators import *
	from modules.auth.login import *

import numpy as np
import json 



plotActions = Blueprint('plotActions', __name__, template_folder='templates')


@plotActions.before_request
def setup_session():
	sm = current_app.config['SessionManager']
	s_id = current_app.config['session_cookie_id']

	if s_id not in session:
		sm.open_session(current_app, session)
		print "Created: ", session[s_id]




@plotActions.route('/actions/plot/<int:tile_id>', methods=['GET'])
#@admin_required(current_app, session, login_redirect)
def generate_plot(tile_id):
	plot_params = request.args 
	
	instance_db = instance_handle()
	db = db_handle(instance_db)
	database = db.cursor()


	tile_data = dashboard.loadDashboardTile(tile_id, database)
	tile_data["requirements"] = parsePlot_requirements(tile_data)
	tile_data["helper_script"] = load_PlotHelperScript(tile_data["requirements"]["helper_script"])

	helper_instance = tile_data["helper_script"](tile_data["requirements"]["data_endpoint"], tile_data["requirements"]["template_file"], tile_data["requirements"]["data_sources"])
	
	data_sources = set(helper_instance.data_sources.split(','))

	source_handles = {}
					
	for source_id in data_sources:
		if source_id == "order":
			source_handles["order"] = order
		elif source_id == "product":
			source_handles["product"] = product
		elif source_id == "config":
			source_handles["config"] = config
		elif source_id == "store":
			source_handles["store"] = store
	
	helper_instance.set_database(database)	#point the helper instance at the data source for query file
	helper_instance.load_data_sources(source_handles)	#load local db functions, if necessary

	helper_instance.run_script(plot_params)
	
	template_data = helper_instance.template_data

	tile_template = render_template("control_panel/dashboard/tile_templates/base_plot.html", template_data = template_data)
	
	#rendered_plots[tile_id] = tile_template


	#db.commit()
	db.close()
	return tile_template




def main():
	pass


if __name__ == "__main__":main()