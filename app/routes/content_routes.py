from flask import Blueprint, jsonify

content_routes = Blueprint('content_routes', __name__)

@content_routes.route('/update/<int:table_id>/<int:row_id>')
def update_row(table_id, row_id):
    # update_row = content_controller.update_row(table_id, row_id) 
    # return update_row
    return jsonify({'message': 'Update row route', 'table_id': f'{table_id}', 'row_id': f'{row_id}'})

@content_routes.route('/delete/<int:table_id>/<int:row_id>')
def delete_row(table_id, row_id):
    # delete_row = content_controller.delete_row(table_id, row_id) 
    # return delete_row
    return jsonify({'message': 'Delete row route', 'table_id': f'{table_id}', 'row_id': f'{row_id}'})

