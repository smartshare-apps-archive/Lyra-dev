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
	import modules.database.message as message

	from modules.decorators import *
	from modules.auth.login import *


import numpy as np
import json 
from datetime import datetime
import re

messageActions = Blueprint('messageActions', __name__, template_folder='templates')


@messageActions.before_request
def setup_session():
	sm = current_app.config['SessionManager']
	s_id = current_app.config['session_cookie_id']

	if s_id not in session:
		sm.open_session(current_app, session)
		print "Created: ", session[s_id]


ACCEPTED_MESSAGES = ["email_signup", "live_chat", "contact_form"]
EMAIL_TTL = 1000000
LIVECHAT_TTL = 3000

@messageActions.route('/actions/store_message', methods=['GET'])
#@admin_required(current_app, session, login_redirect)
@with_user_data(current_app, session)
def store_message():
	s_id = current_app.config['session_cookie_id']
	session_token = session[s_id]

	args = request.args

	message_data = {}
	for arg in args:
		message_data[arg] = request.args.get(arg)

	if valid_message(message_data):

		instance_db = instance_handle()
		db = db_handle(instance_db)
		database = db.cursor()
		ts = datetime.now()

		message_data["timestamp"] = ts
		message_data["session_id"] = session_token
		message_data["ttl"] = get_ttl(message_data)

		
		message.saveMessage(message_data, database)

		db.commit()
		db.close()
		return json.dumps(message_data["ttl"])


	return json.dumps("Invalid message format.")

	


def get_ttl(data):
	if "type" in data:
		if data["type"] == "email_signup":
			return EMAIL_TTL
		elif data["type"] == "live_chat":
			return LIVECHAT_TTL



def valid_message(data):
	valid = True

	if "type" in data:
		if data["type"] == "email_signup":
			if "body" in data:
				valid_email = validate_email(data["body"])
				if valid_email:
					return True
			else:
				return False

		if data["type"] == "live_chat":
			if "body" in data:
				return True
			else:
				return False




	else:
		return False

	return False



	



def validate_email(body):
	VALID_EMAIL_RE = re.compile(r'[^@]+@[^@]+\.[^@]+')

	m = re.search(VALID_EMAIL_RE, body)
	if m:
		return True
	else:
		return False





def main():
	pass


if __name__ == "__main__":main()