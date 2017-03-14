import json, ast, re, os

from flask import Blueprint, render_template, abort, current_app, session, request, flash
from werkzeug.utils import secure_filename
from flask import send_from_directory

#ecomm module imports
from modules.db import *
import modules.database.config
import  modules.database.product as product
import modules.database.resources as resources
from modules.decorators import *
from modules.auth.login import *


ALLOWED_IMAGE_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
ALLOWED_RESOURCE_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx'])

resourceActions = Blueprint('resourceActions', __name__, template_folder='templates')

@resourceActions.before_request
def setup_session():
	sm = current_app.config['SessionManager']
	s_id = current_app.config['session_cookie_id']

	if s_id not in session:
		sm.open_session(current_app, session)
		print "Created: ", session[s_id]


def allowed_image_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

def allowed_resource_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_RESOURCE_EXTENSIONS




@resourceActions.route('/actions/uploadImage', methods=['GET', 'POST'])
def upload_image_file():
	if request.method == 'POST':

		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':

			flash('No selected file')
			return redirect(request.url)

		if file and allowed_image_file(file.filename):
			product_id = request.form.get('product_id',None)
			collection_id = request.form.get('collection_id',None)

			filename = secure_filename(file.filename)
			file.save(os.path.join(current_app.config['IMAGE_UPLOAD_FOLDER'], filename))
            
			db = db_handle()
			database = db.cursor()
			imageURL = url_for('resourceActions.uploaded_file',
                                    filename=filename)

			if collection_id is not None:
				resource_id = resources.createResource(imageURL, "collection_image", database)
				updated = product.updateCollectionImage(collection_id, resource_id, database)
			elif product_id is not None:
				resource_id = resources.createResource(imageURL, "product_image", database)
				updated = product.updateProductResources(product_id, resource_id, "product_image", database)

			if updated:
				print "resource id: ", resource_id
				print "image url:", imageURL

			db.commit()
			db.close()

			return redirect(request.referrer)
	return redirect(request.referrer)



#upload a file to resources folder and store a handle to it in resources table
@resourceActions.route('/actions/uploadFile', methods=['GET', 'POST'])
def upload_resource_file():
	if request.method == 'POST':

		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':

			flash('No selected file')
			return redirect(request.url)

		if file and allowed_resource_file(file.filename):

			filename = secure_filename(file.filename)
			file.save(os.path.join(current_app.config['FILE_UPLOAD_FOLDER'], filename))
            
			db = db_handle()
			database = db.cursor()
			fileURL = url_for('resourceActions.uploaded_file',
                                    filename=filename)

			resource_id = resources.createResource(fileURL, "uploaded_file", database)

			db.commit()
			db.close()

			return redirect(request.referrer)
	return redirect(request.referrer)
	


#deletes a stored resource file from both the table and local filesystem
@resourceActions.route('/actions/deleteResource/<int:resourceID>', methods=['GET', 'POST'])
def delete_resource_file(resourceID):
	db = db_handle()
	database = db.cursor()

	resource_uri = resources.loadResourceURI(resourceID, database)
	resource_uri = resource_uri.split('/')
	filename = resource_uri[len(resource_uri)-1]

	resources.deleteResource(resourceID, database)

	print "Deleting: ", filename

	db.commit()
	db.close()

	os.remove(os.path.join(current_app.config['FILE_UPLOAD_FOLDER'], filename))
	
	return redirect(request.referrer)


@resourceActions.route('/actions/bulkDeleteResources', methods=['POST'])
#@admin_required(current_app, session, login_redirect)
def bulkDeleteResources():
	resource_id_list = request.form['resource_id_list']
	resource_id_list = json.loads(resource_id_list)
	
	db = db_handle()
	database = db.cursor()
	
	resources.bulkDeleteResources(resource_id_list, database)

	db.commit()
	db.close()

	return json.dumps("success")



@resourceActions.route('/static/images/<filename>')
def uploaded_image(filename):
    return send_from_directory(current_app.config['IMAGE_UPLOAD_FOLDER'],
                               filename)



@resourceActions.route('/static/uploaded_files/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['FILE_UPLOAD_FOLDER'],
                               filename)