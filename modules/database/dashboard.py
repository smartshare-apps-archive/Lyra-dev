import sys,csv,json,collections	

from product_util import *
from order_util import *
from dashboard_util import *

import config
import product
import event
import customer


def loadAllDashboardTiles(database):
	currentQuery = "SELECT tile_id, tile_type, requirements, resources FROM dashboard_tiles;"

	try:
		database.execute(currentQuery)
	except Exception as e:
		print "Error loading dashboard tiles: ",e
		return None

	dashboard_tiles = database.fetchall()
	if dashboard_tiles:
		formattedDashboardTiles = {}
		for tile in dashboard_tiles:
			current_tile = str(tile[0])
			formattedDashboardTiles[current_tile] = {}

			for i in range(len(dashboardColumnMappings)):
				formattedDashboardTiles[current_tile][dashboardColumnMappings[i]] = tile[i]
		
		return formattedDashboardTiles




def loadDashboardTile(tile_id, database):
	currentQuery = "SELECT tile_id, tile_type, requirements, resources FROM dashboard_tiles WHERE tile_id=%s;"

	try:
		database.execute(currentQuery,(tile_id,))
	except Exception as e:
		print "Error loading dashboard tile: ",e
		return None

	dashboard_tile = database.fetchone()

	if dashboard_tile:	
		formattedDashboardTile = {}

		for i in range(len(dashboardColumnMappings)):
			formattedDashboardTile[dashboardColumnMappings[i]] = dashboard_tile[i]
		
		return formattedDashboardTile