import sys,csv,json,collections


import product
import resources
import config
import event
import customer

from product_util import *
from order_util import *



def loadAllPlugins(database):
	currentQuery = "SELECT plugin_id, plugin_name, plugin_icon, plugin_type, uri, description FROM plugins";
	
	try:
		database.execute(currentQuery)
	except Exception as e:
		print e

	pluginList = database.fetchall();
	if pluginList:
		formattedPluginList = {}
		for i in range(len(pluginList)):
			currentPluginID = str(pluginList[i][0])
			formattedPluginList[currentPluginID] = {}

			for j in range(len(pluginColumnMappings)):
				formattedPluginList[currentPluginID][pluginColumnMappings[j]] = pluginList[i][j]

		return formattedPluginList


def loadPluginByID(plugin_id, database):
	currentQuery = "SELECT plugin_id, plugin_name, plugin_icon, plugin_type, uri, description FROM plugins WHERE plugin_id=%s;"

	try: 
		database.execute(currentQuery,(plugin_id, ))
	except Exception as e:
		print "Error: ", e
		return None

	plugin = database.fetchone()
	if plugin:
		formattedPluginData = {}
		for i in range(len(pluginColumnMappings)):
			formattedPluginData[pluginColumnMappings[i]] = plugin[i]

		return formattedPluginData



