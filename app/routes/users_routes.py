from flask import Blueprint, jsonify

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/update/<int:table_id>/<int:row_id>', methods=['PUT'])
def update_row(table_id, row_id):
    # update_row = content_controller.update_row(table_id, row_id) 
    # return update_row
    return jsonify({'message': 'Update user route', 'table_id': f'{table_id}', 'row_id': f'{row_id}'})

@user_routes.route('/delete/<int:table_id>/<int:row_id>', methods=['DELETE'])
def delete_row(table_id, row_id):
    # delete_row = content_controller.delete_row(table_id, row_id) 
    # return delete_row
    return jsonify({'message': 'Delete user route', 'table_id': f'{table_id}', 'row_id': f'{row_id}'})


from flask import request

from ..app import app
from .controllers import list_all_accounts_controller, create_account_controller, retrieve_account_controller, update_account_controller, delete_account_controller

@app.route("/accounts", methods=['GET', 'POST'])
def list_create_accounts():
    if request.method == 'GET': return list_all_accounts_controller()
    if request.method == 'POST': return create_account_controller()
    else: return 'Method is Not Allowed'

@app.route("/accounts/<account_id>", methods=['GET', 'PUT', 'DELETE'])
def retrieve_update_destroy_accounts(account_id):
    if request.method == 'GET': return retrieve_account_controller(account_id)
    if request.method == 'PUT': return update_account_controller(account_id)
    if request.method == 'DELETE': return delete_account_controller(account_id)
    else: return 'Method is Not Allowed'