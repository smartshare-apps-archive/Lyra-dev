import json, time

from flask import Blueprint, render_template, abort, current_app, session, request, Markup, url_for, redirect

# ecomm module imports
from modules.db import *
from modules.decorators import *
from modules.auth.login import *
import modules.database.product

import modules.database.config as config
import modules.database.vendor as vendor

from modules.database.product_util import *

product_routes = Blueprint('product_routes', __name__)


@product_routes.before_request
def setup_session():
    sm = current_app.config['SessionManager']
    s_id = current_app.config['session_cookie_id']

    if s_id not in session:
        sm.open_session(current_app, session)
        print 'Created:', session[s_id]


# route to main product list
@product_routes.route('/control/products/', methods=['GET', 'POST'])
@product_routes.route('/control/products', methods=['GET', 'POST'])
# @admin_required(current_app, session, login_redirect)
def products():
    current_page = 'products'
    ctl = current_app.config['ctl']
    response = ctl.render_tab(current_page)

    if response in config.ERROR_CODES:
        return redirect(url_for('settings_routes.advanced_settings', flag='NO_DB'))

    context = {
        'current_page': current_page,
        'current_class_js': 'control_panel/product/Core.js',
        'current_page_js': 'control_panel/product/Main.js',
        'current_requests_js': 'control_panel/product/Requests.js',
        'current_page_content': response,
        'ts': int(time.time()),
        'modals': [render_template('control_panel/modal.html')],
        'submenu': Markup(render_template('control_panel/subMenu_products.html'))
    }

    return render_template('control_panel/control.html', data=context)


# route to single product editor
@product_routes.route('/control/products/<int:product_id>/')
@product_routes.route('/control/products/<int:product_id>')
# @admin_required(current_app, session, login_redirect)
def productEditor(product_id):
    current_page = 'product_editor'
    ctl = current_app.config['ctl']
    response = ctl.render_tab(current_page, data=product_id)

    if response in config.ERROR_CODES:
        return redirect(url_for('settings_routes.advanced_settings', flag='NO_DB'))

    instance_db = instance_handle()
    db = db_handle(instance_db)

    product_data = loadProduct(product_id, db.cursor())

    if product_data['Tags']:
        product_tags = formatProductTags(product_data['Tags'])
    else:
        product_tags = []

    all_tags = config.loadProductTags(instance_db.cursor())
    all_types = config.loadProductTypes(instance_db.cursor())
    all_vendors = vendor.loadAllVendors(db.cursor())

    db.close()

    context = {
        'current_page': current_page,
        'product_id': product_id,
        'current_page_content': response,
        'ts': int(time.time()),
        'modals': [render_template('control_panel/modal.html'),
                   render_template('control_panel/modal_image_upload.html', product_id=product_id),
                   render_template('control_panel/modal_edit_tags.html', product_id=product_id,
                                   product_tags=product_tags, all_tags=all_tags),
                   render_template('control_panel/modal_edit_types.html', product_id=product_id, all_types=all_types,
                                   product_type=product_data['Type']),
                   render_template('control_panel/modal_edit_vendors.html', product_id=product_id,
                                   vendors=all_vendors)],
        'submenu': Markup(render_template('control_panel/subMenu_products.html')),
        'current_class_js': 'control_panel/product/Core.js',
        'current_page_js': 'control_panel/product/ProductEditor.js',
        'current_requests_js': 'control_panel/product/Requests.js'
    }

    return render_template('control_panel/control.html', data=context)


# route to single collection editor
@product_routes.route('/control/products/collections/<collection_id>/')
@product_routes.route('/control/products/collections/<collection_id>')
# @admin_required(current_app, session, login_redirect)
def collectionEditor(collection_id):
    current_page = 'collection_editor'
    ctl = current_app.config['ctl']
    response = ctl.render_tab(current_page, data=collection_id)

    if response in config.ERROR_CODES:
        return redirect(url_for('settings_routes.advanced_settings', flag='NO_DB'))

    context = {
        'current_page': current_page,
        'product_id': collection_id,
        'current_page_content': response,
        'ts': int(time.time()),
        'modals': [render_template('control_panel/modal.html'),
                   render_template('control_panel/modal_image_upload.html', collection_id=collection_id)],
        'submenu': Markup(render_template('control_panel/subMenu_products.html')),
        'current_class_js': 'control_panel/product/Core.js',
        'current_page_js': 'control_panel/product/CollectionEditor.js',
        'current_requests_js': 'control_panel/product/Requests.js'}

    return render_template('control_panel/control.html', data=context)


# route to bulk collection editor
@product_routes.route('/control/products/collections/bulkEditor', methods=['GET'])
# @admin_required(current_app, session, login_redirect)
def productBulkCollectionEditor():
    current_page = 'product_bulk_collection_editor'
    ctl = current_app.config['ctl']
    collectionIDList = map(int, request.args.get('ids', '').split(','))

    response = ctl.render_tab(current_page, collectionIDList)

    if response in config.ERROR_CODES:
        return redirect(url_for('settings_routes.advanced_settings', flag='NO_DB'))

    context = {
        'collectionIDList': collectionIDList,
        'current_page': current_page,
        'current_page_content': response,
        'current_class_js': 'control_panel/product/Core.js',
        'current_page_js': 'control_panel/product/BulkCollectionEditor.js',
        'current_requests_js': 'control_panel/product/Requests.js',
        'ts': int(time.time()),
        'modals': [render_template('control_panel/modal.html')],
        'submenu': Markup(render_template('control_panel/subMenu_products.html'))
    }

    return render_template('control_panel/control.html', data=context)


# route to bulk product editor
@product_routes.route('/control/products/bulkEditor', methods=['GET'])
# @admin_required(current_app, session, login_redirect)
def productBulkEditor():
    current_page = 'product_bulk_editor'
    ctl = current_app.config['ctl']
    productIdList = map(int, request.args.get('ids', '').split(','))

    response = ctl.render_tab(current_page, productIdList)

    if response in config.ERROR_CODES:
        return redirect(url_for('settings_routes.advanced_settings', flag='NO_DB'))

    context = {
        'productIdList': productIdList,
        'current_page': current_page,
        'current_page_content': response,
        'current_class_js': 'control_panel/product/Core.js',
        'current_page_js': 'control_panel/product/BulkProductEditor.js',
        'current_requests_js': 'control_panel/product/Requests.js',
        'ts': int(time.time()),
        'modals': [render_template('control_panel/modal.html')],
        'submenu': Markup(render_template('control_panel/subMenu_products.html'))
    }

    return render_template('control_panel/control.html', data=context)


# route to product inventory list
@product_routes.route('/control/products/inventory/')
# @admin_required(current_app, session, login_redirect)
def productInventory():
    current_page = 'product_inventory'
    ctl = current_app.config['ctl']
    response = ctl.render_tab(current_page)

    if response in config.ERROR_CODES:
        return redirect(url_for('settings_routes.advanced_settings', flag='NO_DB'))

    context = {
        'current_page': current_page,
        'current_page_content': response,
        'current_class_js': 'control_panel/product/Core.js',
        'current_page_js': 'control_panel/product/Inventory.js',
        'current_requests_js': 'control_panel/product/Requests.js',
        'ts': int(time.time()),
        'modals': [render_template('control_panel/modal.html')],
        'submenu': Markup(render_template('control_panel/subMenu_products.html'))
    }

    return render_template('control_panel/control.html', data=context)


# route to single product inventory editor
@product_routes.route('/control/products/inventory/<variant_id>')
@product_routes.route('/control/products/inventory/<variant_id>/')
# @admin_required(current_app, session, login_redirect)
def productInventoryEditor(variant_id):
    current_page = 'product_inventory_editor'
    ctl = current_app.config['ctl']
    response = ctl.render_tab(current_page, data=variant_id)

    if response in config.ERROR_CODES:
        return redirect(url_for('settings_routes.advanced_settings', flag='NO_DB'))

    context = {
        'current_page': current_page,
        'current_page_content': response,
        'current_class_js': 'control_panel/product/Core.js',
        'current_page_js': 'control_panel/product/InventoryEditor.js',
        'current_requests_js': 'control_panel/product/Requests.js',
        'ts': int(time.time()),
        'modals': [render_template('control_panel/modal.html'),
                   render_template('control_panel/modal_image_upload.html', variant_id=variant_id)],
        'submenu': Markup(render_template('control_panel/subMenu_products.html'))
    }

    return render_template('control_panel/control.html', data=context)


# route to bulk product inventory editor
@product_routes.route('/control/products/inventory/bulkEditor', methods=['GET'])
# @admin_required(current_app, session, login_redirect)
def productBulkInventoryEditor():
    current_page = 'product_bulk_inventory_editor'
    ctl = current_app.config['ctl']
    variantIdList = map(int, request.args.get('ids', '').split(','))

    response = ctl.render_tab(current_page, variantIdList)

    if response in config.ERROR_CODES:
        return redirect(url_for('settings_routes.advanced_settings', flag='NO_DB'))

    context = {
        'variantIdList': variantIdList,
        'current_page': current_page,
        'current_page_content': response,
        'current_class_js': 'control_panel/product/Core.js',
        'current_page_js': 'control_panel/product/BulkInventoryEditor.js',
        'current_requests_js': 'control_panel/product/Requests.js',
        'ts': int(time.time()),
        'modals': [render_template('control_panel/modal.html')],
        'submenu': Markup(render_template('control_panel/subMenu_products.html'))
    }

    return render_template('control_panel/control.html', data=context)


# route to product collections list
@product_routes.route('/control/products/collections/')
# @admin_required(current_app, session, login_redirect)
def productCollections():
    current_page = 'product_collections'
    ctl = current_app.config['ctl']
    response = ctl.render_tab(current_page)

    if response in config.ERROR_CODES:
        return redirect(url_for('settings_routes.advanced_settings', flag='NO_DB'))

    context = {
        'current_page': current_page,
        'current_page_content': response,
        'current_class_js': 'control_panel/product/Core.js',
        'current_page_js': 'control_panel/product/Collections.js',
        'current_requests_js': 'control_panel/product/Requests.js',
        'ts': int(time.time()),
        'modals': [render_template('control_panel/modal.html')],
        'submenu': Markup(render_template('control_panel/subMenu_products.html'))
    }

    return render_template('control_panel/control.html', data=context)
