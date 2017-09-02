import json, ast, re

from flask import Blueprint, render_template, abort, current_app, session, request

# ecomm module imports
from modules.db import *
import modules.database.config as config
import modules.database.product as product
import modules.database.resources as resources
import modules.database.customer as customer

from modules.decorators import *
from modules.auth.login import *

settingsActions = Blueprint('settingsActions', __name__, template_folder='templates')


@settingsActions.before_request
def setup_session():
    sm = current_app.config['SessionManager']
    s_id = current_app.config['session_cookie_id']

    if s_id not in session:
        sm.open_session(current_app, session)
        print "Created: ", session[s_id]


@settingsActions.route('/actions/saveStripeAPIKeys', methods=['POST'])
# @admin_required(current_app, session, login_redirect)
def saveStripeAPIKeys():
    stripe_api_keys = request.form['stripe_api_keys']
    stripe_api_keys = json.loads(stripe_api_keys)

    instance_db = instance_handle()

    config.setStripeAPIKeys(api_keys=stripe_api_keys, database=instance_db.cursor())

    instance_db.commit()
    instance_db.close()

    return json.dumps("success")


@settingsActions.route('/actions/saveShippoAPIKeys', methods=['POST'])
# @admin_required(current_app, session, login_redirect)
def saveShippoAPIKeys():
    shippo_api_keys = request.form['shippo_api_keys']
    shippo_api_keys = json.loads(shippo_api_keys)

    instance_db = instance_handle()

    config.setShippoAPIKeys(api_keys=shippo_api_keys, database=instance_db.cursor())

    instance_db.commit()
    instance_db.close()

    return json.dumps("success")


@settingsActions.route('/actions/saveDefaultShippingAddress', methods=['POST'])
# @admin_required(current_app, session, login_redirect)
def saveDefaultShippingAddress():
    default_shipping_address = request.form['default_shipping_address']
    default_shipping_address = json.loads(default_shipping_address)

    instance_db = instance_handle()

    config.setDefaultShippingAddress(default_shipping_address, database=instance_db.cursor())

    instance_db.commit()
    instance_db.close()

    return json.dumps("success")


@settingsActions.route('/actions/savePackageTypes', methods=['POST'])
# @admin_required(current_app, session, login_redirect)
def savePackageTypes():
    package_types = request.form['package_types']
    package_types = json.loads(package_types)

    instance_db = instance_handle()

    config.setPackageTypes(package_types, instance_db.cursor())

    instance_db.commit()
    instance_db.close()

    return json.dumps("success")


@settingsActions.route('/actions/saveRedisConfig', methods=['POST'])
# @admin_required(current_app, session, login_redirect)
def saveRedisConfig():
    redis_config = request.form['redis_config']
    redis_config = json.loads(redis_config)

    instance_db = instance_handle()

    config.setRedisConfig(redis_config, instance_db.cursor())

    instance_db.commit()
    instance_db.close()

    return json.dumps("success")


@settingsActions.route('/actions/saveDatabaseConfig', methods=['POST'])
# @admin_required(current_app, session, login_redirect)
def saveDatabaseConfig():
    database_config = request.form['database_config']
    database_config = json.loads(database_config)

    instance_db = instance_handle()

    config.setDatabaseConfig(database_config, instance_db.cursor())

    instance_db.commit()
    instance_db.close()

    return json.dumps("success")
