"""table_controller.py"""

import os
from flask import Blueprint, jsonify, current_app
from ..config.db_connect import connect_to_db
from ..models.tables_model import Table
from ..services.table_services import TableServices

table_bp = Blueprint('table_bp', __name__)

class TableController:
    """
    Table controller
    """

    @staticmethod
    def create_table_in_db(user_id, table_name, structure):
        """
        Creates a new table in the database given the table_name and structure
        
        Parameters:
            table_name(str): the name of the new table
            structure(str): the structure of the table to be created (in json format)
        """
        
        # Check if their is a record in the 'Tables' table with the provided 
        # user_id and table_name
        TableServices.check_tablename_record(user_id, table_name)
        
        # Check if a table with the provided table_name exits in the database 
        TableServices.check_table_exists(table_name)

        # Create a cursor to connect to the database
        cursor = connect_to_db().cursor()

        # Build the SQL statement to create the table
        query = f"CREATE TABLE {table_name} ("
        query += "id SERIAL PRIMARY KEY NOT NULL,"
        for column in structure:
            name = column['name']
            data_type = TableController.get_column_type(column['data_type'])
            query += f"{name} {data_type}, "
        query = query.rstrip(', ') + ");"
        cursor = connect_to_db().cursor()
        cursor.execute(query)
        
        
        
        # print("STRUCTURE TYPE:")
        # print(type(structure))
        
        # json_structure = jsonify(structure)

        # table_columns = {
        #     'id': db.Column(db.Integer, primary_key=True)
        # }

        # for col in structure:
        #     col_name = col['name']
        #     data_type = col['data_type']
            
        #     # Map data types to SQLAlchemy types
        #     if data_type == 'integer':
        #         column = db.Column(db.Integer)
        #     elif data_type == 'string':
        #         column = db.Column(db.String(255))  # Replace 255 with desired string length
            
        #     table_columns[col_name] = column

        # try:
        #     table = type(table_name, (db.Model,), table_columns)
        #     db.create_all()
        #     return jsonify({'message': f'Table {table_name} created successfully'}), 200
        # except Exception as e:
        #     return jsonify({'error': str(e)}), 500


