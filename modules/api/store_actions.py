import json, ast, re

from flask import Blueprint, render_template, abort, current_app, session, request


#ecomm module imports
from modules.db import *
import modules.database.config as config
import modules.database.product as product
import modules.database.resources as resources
import modules.database.customer as customer
import modules.database.store as store

from modules.decorators import *
from modules.auth.login import *


storeActions = Blueprint('storeActions', __name__, template_folder='templates')


@storeActions.before_request
def setup_session():
	sm = current_app.config['SessionManager']
	s_id = current_app.config['session_cookie_id']

	if s_id not in session:
		sm.open_session(current_app, session)
		print "Created: ", session[s_id]



@storeActions.route('/actions/saveNavigationSettings', methods=['POST'])
#@admin_required(current_app, session, login_redirect)
def saveNavigationSettings():
	nav_data = request.form['nav_data']
	nav_data = json.loads(nav_data)
	
	db = db_handle()
	database = db.cursor()

	store.updateNavData(nav_data, database)

	db.commit()
	db.close()

	return json.dumps("success")




@storeActions.route('/actions/saveFooterSettings', methods=['POST'])
#@admin_required(current_app, session, login_redirect)
def saveFooterSettings():
	footer_data = request.form['footer_data']
	footer_data = json.loads(footer_data)
	
	print "footer: ", footer_data
	db = db_handle()
	database = db.cursor()

	store.updateFooterData(footer_data, database)

	db.commit()
	db.close()

	return json.dumps("success")



@storeActions.route('/actions/savePageData', methods=['POST'])
#@admin_required(current_app, session, login_redirect)
def savePageData():
	page_data = request.form['page_data']
	page_data = json.loads(page_data)
	
	db = db_handle()
	database = db.cursor()

	store.updatePageData(page_data, database)

	db.commit()
	db.close()

	return json.dumps("success")



@storeActions.route('/actions/savePageSectionData', methods=['POST'])
#@admin_required(current_app, session, login_redirect)
def savePageSectionData():
	page_id = request.form['page_id']
	page_id = json.loads(page_id)

	page_section_data = request.form['page_section_data']
	page_section_data = json.loads(page_section_data)
	
	db = db_handle()
	database = db.cursor()

	store.updatePageSectionData(page_section_data, page_id, database)

	db.commit()
	db.close()

	return json.dumps("success")



@storeActions.route('/actions/savePageThemes', methods=['POST'])
#@admin_required(current_app, session, login_redirect)
def savePageThemes():
	page_data = request.form['page_data']
	page_data = json.loads(page_data)
	
	page_id_list = request.form['page_id_list']
	page_id_list = json.loads(page_id_list)

	db = db_handle()
	database = db.cursor()

	for page_id in page_id_list:
		store.updatePageSectionData(page_data[page_id]["page_section_data"], page_id, database)
		store.updatePageData(page_data[page_id], database)

	db.commit()
	db.close()

	return json.dumps("success")



@storeActions.route('/actions/createNewPage', methods=['POST'])
#@admin_required(current_app, session, login_redirect)
def createNewPage():
	new_page_data = request.form['new_page_data']
	new_page_data = json.loads(new_page_data)
	
	db = db_handle()
	database = db.cursor()

	store.createNewPage(new_page_data, database)

	db.commit()
	db.close()

	return json.dumps("success")





@storeActions.route('/actions/deletePage', methods=['POST'])
#@admin_required(current_app, session, login_redirect)
def deletePage():
	page_id = request.form['page_id']
	page_id = json.loads(page_id)
	
	db = db_handle()
	database = db.cursor()

	store.deletePage(page_id, database)

	db.commit()
	db.close()

	return json.dumps("success")