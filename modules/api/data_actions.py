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

	from modules.decorators import *
	from modules.auth.login import *

import numpy as np
import json 



#google analytics api inclusions

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'modules/api/My Project-4a4e3894caff.json'
VIEW_ID = '129134234'



dataActions = Blueprint('dataActions', __name__, template_folder='templates')


@dataActions.before_request
def setup_session():
	sm = current_app.config['SessionManager']
	s_id = current_app.config['session_cookie_id']

	if s_id not in session:
		sm.open_session(current_app, session)
		print "Created: ", session[s_id]




@dataActions.route('/actions/get_analytics_data', methods=['GET'])
#@admin_required(current_app, session, login_redirect)
def getAnalyticsData():
	plot_args = request.args
	plot_params = {}

	for param in plot_args:
		plot_params[param] = request.args.get(param)

	print plot_params


	analytics = initialize_google_analytics() 

	response = get_analytics(analytics, plot_params)

	analytics_data = parse_analytics_response(response)

	a = np.array(analytics_data)
	b = a.tolist()
	
	#b = a.tolist() # nested lists with same data, indices

	return json.dumps(b)





def initialize_google_analytics():
	credentials = ServiceAccountCredentials.from_json_keyfile_name(
	KEY_FILE_LOCATION, SCOPES)

	analytics = build('analytics', 'v4', credentials=credentials)
	return analytics





def get_analytics(analytics, plot_params):

	return analytics.reports().batchGet(
			body={
			'reportRequests': [
			{
			'viewId': VIEW_ID,
			'dateRanges': [{'startDate': plot_params["start_date"], 'endDate': plot_params["end_date"]}],
			'metrics': [
						{'expression': plot_params["metric"]}, 
						],
			'dimensions': [{'name': 'ga:date'}],
			"includeEmptyRows": True,
			}]

			}
			).execute()






def parse_analytics_response(response):
	x_data = []
	y_data = []

	for report in response.get('reports', []):
		columnHeader = report.get('columnHeader', {})
		dimensionHeaders = columnHeader.get('dimensions', [])
		metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

		for row in report.get('data', {}).get('rows', []):
			dimensions = row.get('dimensions', [])
			dateRangeValues = row.get('metrics', [])

			x_data.append(dimensions[0])
			y_data.append(dateRangeValues[0]["values"][0])

			#print dateRangeValues

	return [x_data, y_data]



def main():
	analytics = initialize_analyticsreporting()
	response = get_report(analytics)
	parse_analytics_response(response)


if __name__ == "__main__":main()