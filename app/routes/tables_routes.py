from flask import Blueprint, jsonify

table_routes = Blueprint("table_routes", __name__)

# Get all tables
@table_routes.route("/", methods=["GET"])
def get_tables():
    # update_row = content_controller.update_row(table_id, row_id) 
    # return update_row
    return jsonify({"message": "'Get all tables' route"})

# Get tables per user
@table_routes.route("/user/<int:user_id>", methods=["GET"])
def get_tables_per_user(user_id):
    # update_row = content_controller.update_row(table_id, row_id) 
    # return update_row
    return jsonify({"message": "'Get tables per user' route", "user_id": f"{user_id}"})

@table_routes.route("/<int:table_id>", methods=["GET"])
def get_table(table_id, row_id):
    # update_row = content_controller.update_row(table_id, row_id) 
    # return update_row
    return jsonify({"message": "'Get table' route", "table_id": f"{table_id}"})

@table_routes.route("/", methods=["POST"])
def create_table():
    # update_row = content_controller.update_row(table_id, row_id) 
    # return update_row
    return jsonify({"message": "'Create table' route", "table_id": f"{table_id}"})

@table_routes.route("/update/<int:table_id>", methods=["PUT"])
def update_table(table_id):
    # update_row = content_controller.update_row(table_id, row_id) 
    # return update_row
    return jsonify({"message": "'Update user' route", "table_id": f"{table_id}"})

@table_routes.route("/delete/<int:table_id>>", methods=["DELETE"])
def delete_table(table_id):
    # delete_row = content_controller.delete_row(table_id, row_id) 
    # return delete_row
    return jsonify({"message": "'Delete user' route", "table_id": f"{table_id}"})


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