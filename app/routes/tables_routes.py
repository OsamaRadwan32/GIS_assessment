from flask import Blueprint, jsonify, request
from ..controllers.table_controller import TableController
from ..services.table_services import TableServices

table_routes = Blueprint('table_routes', __name__)

# Get all tables
@table_routes.route('/', methods=['GET', 'POST'])
def get_or_create():
    if request.method == 'GET': return jsonify({'message': 'get_tables route'})
    if request.method == 'POST': return create_account_controller()
    else: return 'Method is Not Allowed'

# Get tables per user
@table_routes.route('/user/<int:user_id>', methods=['GET'])
def get_tables_per_user(user_id):
    # update_row = content_controller.update_row(table_id, row_id) 
    # return update_row
    return jsonify({'message': 'get_tables_per_user route', 'user_id': f'{user_id}'})

@table_routes.route('/<int:table_id>', methods=['GET'])
def get_table(table_id, row_id):
    # update_row = content_controller.update_row(table_id, row_id) 
    # return update_row
    return jsonify({'message': 'get_table route', 'table_id': f'{table_id}'})

@table_routes.route('/', methods=['POST'])
def create_table():
    # update_row = content_controller.update_row(table_id, row_id) 
    # return update_row
    return jsonify({'message': 'create_table route', 'table_id': f'{table_id}'})

@table_routes.route('/update/<int:table_id>', methods=['PUT'])
def update_table(table_id):
    # update_row = content_controller.update_row(table_id, row_id) 
    # return update_row
    return jsonify({'message': 'update_table route', 'table_id': f'{table_id}'})

@table_routes.route('/delete/<int:table_id>>', methods=['DELETE'])
def delete_table(table_id):
    # delete_row = content_controller.delete_row(table_id, row_id) 
    # return delete_row
    return jsonify({'message': 'delete_table route', 'table_id': f'{table_id}'})

"""
Testing Routes
"""
@table_routes.route('/check_tablename_record/<int:user_id>/<table_name>', methods=['GET'])
def check_tablename_record(user_id, table_name):
    if request.method == 'GET': 
        return jsonify({'message': str(TableServices.check_tablename_record(user_id, table_name))}), 200
    else: return jsonify({'error': 'Method is Not Allowed'}), 400
    
@table_routes.route('/check_table_exists/<table_name>', methods=['GET'])
def check_table_exists(table_name):
    if request.method == 'GET': 
        return jsonify({'message': str(TableServices.check_table_exists(table_name))}), 200 
    else: return jsonify({'error': 'Method is Not Allowed'}), 400
    
@table_routes.route('/create_table_in_db', methods=['POST'])
def create_table_in_db():
    if request.method == 'POST': 
        request_form = request.form.to_dict()
        table_name = request_form['table_name']
        table_structure = request_form['table_structure']
        return jsonify({'message': str(TableController.create_table_in_db(table_name, table_structure))}), 200 
    else: return jsonify({'error': 'Method is Not Allowed'}), 400

@table_routes.route('/populate_table', methods=['POST'])
def populate_table():
    if request.method == 'POST': 
        request_form = request.form.to_dict()
        table_name = request_form['table_name']
        table_structure = request_form['table_structure']
        csv_file_name = request_form['csv_file_name']
        return TableController.populate_table(table_name, table_structure, csv_file_name) 
    else: return jsonify({'error': 'Method is Not Allowed'}), 400