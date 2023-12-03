from flask import Blueprint, request, jsonify
from sqlalchemy import MetaData, Table, Column, Integer, String

import uuid
from .. import app, db
from ..models import tables_model

table_bp = Blueprint('table_bp', __name__)

class TableController:
    @staticmethod
    def create_table(table_name):
        if not request.json:
            return jsonify({'error': 'No data provided'}), 400

        columns = request.json.get('columns')
        datatypes = request.json.get('datatypes')

        if not columns or not datatypes:
            return jsonify({'error': 'Columns or datatypes missing'}), 400

        if len(columns) != len(datatypes):
            return jsonify({'error': 'Mismatch in columns and datatypes'}), 400

        try:
            metadata = MetaData()
            new_table = Table(f'{table_name}', metadata, *[Column(col, getattr(Integer, dtype)) for col, dtype in zip(columns, datatypes)])
            new_table.create(bind=db.engine)
            return jsonify({'message': 'Table created successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500


    @staticmethod
    @table_bp.route('/users', methods=['GET'])
    def get_users():
        # Logic to fetch users from the database
        return 'List of users'

    @staticmethod
    @table_bp.route('/user/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        # Logic to fetch a single user based on user_id
        return f'User with ID {user_id}'

    # Other user-related routes and logic
    # For example, POST, PUT, DELETE methods

# Additional routes can be added in a similar manner in post_controller.py or other controller files.

# ----------------------------------------------- #

# Query Object Methods => https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.Query
# Session Object Methods => https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session
# How to serialize SqlAlchemy PostgreSQL Query to JSON => https://stackoverflow.com/a/46180522

def list_all_accounts_controller():
    accounts = table_model.query.all()
    response = []
    for account in accounts: response.append(account.toDict())
    return jsonify(response)

def create_account_controller():
    request_form = request.form.to_dict()

    id = str(uuid.uuid4())
    new_account = Account(
                          id             = id,
                          email          = request_form['email'],
                          username       = request_form['username'],
                          phone_number   = request_form['phone_number'],
                          )
    db.session.add(new_account)
    db.session.commit()

    response = Account.query.get(id).toDict()
    return jsonify(response)

def retrieve_account_controller(account_id):
    response = Account.query.get(account_id).toDict()
    return jsonify(response)

def update_account_controller(account_id):
    request_form = request.form.to_dict()
    account = Account.query.get(account_id)

    account.email        = request_form['email']
    account.username     = request_form['username']
    account.dob          = request_form['dob']
    account.country      = request_form['country']
    account.phone_number = request_form['phone_number']
    db.session.commit()

    response = Account.query.get(account_id).toDict()
    return jsonify(response)

def delete_account_controller(account_id):
    Account.query.filter_by(id=account_id).delete()
    db.session.commit()

    return ('Account with Id "{}" deleted successfully!').format(account_id)
