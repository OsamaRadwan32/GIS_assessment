"""table_controller.py"""

import uuid
from flask import Blueprint, jsonify
from .. import db
from ..models.tables_model import Table

table_bp = Blueprint('table_bp', __name__)

class TableController:
    '''Table controller'''
        
    @staticmethod
    def add_table_info(table_name, user_id, structure):
        """
        Adds the info of the new table as a record in the 'tables' table
        
        Parameters:
        - table_name(text): the name of the new table
        - user_id(serial): the id of the user
        - structure(string): the structure of the table to be created (in json format)
        """
        table_record = Table(
                            name        = table_name,
                            user_id     = user_id,
                            structure   = structure
                            )
        db.session.add(table_record)
        db.session.commit()

    @staticmethod
    def get_table_by_name(table_name):
        """
        Retrieve a record from the 'tables' table based on the provided name attribute.

        Parameters:
        - table_name (str): The name attribute to search for in the 'tables' table.

        Returns:
        - Table or None: If a record with the provided name is found, the corresponding
        Table object is returned. If no record is found, None is returned.
        """
        try:
            # Query the 'tables' table to find a record with the provided name
            table_record = Table.query.filter_by(name=table_name).first()

            # Check if the record exists
            if table_record:
                return table_record
        except Exception as e:
            # Handle exceptions (e.g., database connection issues)
            print(f"Error: {str(e)}")
            return f"Error: {str(e)}"


    @staticmethod
    def create_table_in_db(table_name, structure):
        """
        Creates a new table in the database given the table_name and structure
        
        Parameters:
            table_name(str): the name of the new table
            structure(str): the structure of the table to be created (in json format)
        """


        print("STRUCTURE TYPE:")
        print(type(structure))
        
        json_structure = jsonify(structure)

        table_columns = {
            'id': db.Column(db.Integer, primary_key=True)
        }

        for col in structure:
            col_name = col['name']
            data_type = col['data_type']
            
            # Map data types to SQLAlchemy types
            if data_type == 'integer':
                column = db.Column(db.Integer)
            elif data_type == 'string':
                column = db.Column(db.String(255))  # Replace 255 with desired string length
            
            table_columns[col_name] = column

        try:
            table = type(table_name, (db.Model,), table_columns)
            db.create_all()
            return jsonify({'message': f'Table {table_name} created successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500


