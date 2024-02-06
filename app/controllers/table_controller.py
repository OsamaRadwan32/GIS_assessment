"""table_controller.py"""

import csv
import pandas as pd
from .. import db
from flask import Blueprint, jsonify
from ..config.db_connect import connect_to_db
from ..services.table_services import TableServices

table_bp = Blueprint('table_bp', __name__)

class TableController:
    """
    Table controller
    """

    @staticmethod
    def create_table_in_db(table_name, structure):
        """
        Creates a new table in the database given the table_name and structure
        
        Parameters:
            table_name(str): the name of the new table
            structure(str): the structure of the table to be created (in json format)
        """

        try:        
            # Create a cursor to connect to the database
            connection = connect_to_db()
            cursor = connection.cursor()
            query = TableServices.construct_create_query(table_name, structure)
            print(f"Executing query: {query}")
            cursor.execute(query)
            # Check if the query executed successfully (cursor.execute() returns None)
            if cursor.rowcount != -1:
                # If rowcount is -1, it means the query was successfully executed
                return jsonify({"error": "Error creating table"})
            connection.commit()
            TableServices.check_table_exists(table_name)
        except Exception as e:
            # Handle the exception and return a custom response
            error_message = str(e)
            return jsonify({"error": error_message}), 500  

        
        
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

    @staticmethod
    def populate_table(table_name, table_structure, csv_file):
        """
        Adds two numbers and returns the result.

        Parameters:
            a (int): The first number.
            b (int): The second number.

        Returns:
            int: The sum of a and b.
        """        
        table_model = db.Model.metadata.tables.get(table_name)
        
        if not table_model:
            return jsonify({"error": "Table does not exist"}), 404

        with open(csv_file, 'r') as file:
            csv_reader = csv.DictReader(file)
            data = [{col: row[col] for col in columns} for row in csv_reader]

            try:
                db.session.execute(YourTable.insert().values(data))
                db.session.commit()
                return jsonify({"message": f"Data inserted into the table '{table_name}' successfully"})
            except Exception as e:
                db.session.rollback()
                return jsonify({"message": f"Failed to insert CSV data: {str(e)}"}), 500
            finally:
                db.session.close()