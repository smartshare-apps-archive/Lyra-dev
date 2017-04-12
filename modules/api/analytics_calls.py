
	for row in report.get('data', {}).get('rows', []):
		dimensions = row.get('dimensions', [])
		dateRangeValues = row.get('metrics', [])

		for header, dimension in zip(dimensionHeaders, dimensions):
			print header , ': ' , dimension

		for i, values in enumerate(dateRangeValues):
			print 'Date range: ' , str(i)

		for metricHeader, value in zip(metricHeaders, values.get('values')):
			print metricHeader.get('name') , ': ' , value