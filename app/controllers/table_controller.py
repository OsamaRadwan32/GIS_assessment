"""table_controller.py"""

import os
from flask import Blueprint, jsonify, current_app
from .. import db
from ..config.db_connect import connect_to_db
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
    def check_tablename_record(user_id, table_name):
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
            table_record = Table.query.filter_by(user_id = user_id, name = table_name).first()

            # Check if the record exists
            if table_record:
                return True
        except Exception as e:
            # Handle exceptions (e.g., database connection issues)
            print(f"Error: {str(e)}")
            return f"Error: {str(e)}"

    @staticmethod
    def check_table_exists(table_name):
        """_summary_

        Args:
            table_name (_type_): _description_

        Returns:
            _type_: _description_
        """
        query  = f"SELECT EXISTS ( "
        query += "SELECT 1 "
        query += "FROM information_schema.tables "
        query += f"WHERE table_schema = '{os.getenv('DATABASE')}' "
        query += f"AND table_name = '{table_name}' );"
        try:
            cursor = connect_to_db().cursor()
            return cursor.execute(query)
        except Exception as e:
            # Handle exceptions (e.g., database connection issues)
            print(f"Error: {str(e)}")
            return f"Error: {str(e)}"

    @staticmethod
    def get_column_type(type):
        type_mapping = {
            'number': "INTEGER",
            'decimal': "DOUBLE PRECISION",
            'text': "VARCHAR(255)",
            'date': "DATE",
        }
        return type_mapping.get(type, String)

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
        TableController.check_tablename_record(user_id, table_name)
        
        # Check if a table with the provided table_name exits in the database 
        TableController.check_table_exists(table_name)

        # Create a cursor to connect to the database
        cursor = connect_to_db.cursor()

        # Build the SQL statement to create the table
        query = f"CREATE TABLE {table_name} ("
        query += "id SERIAL PRIMARY KEY NOT NULL,"
        for column in structure:
            name = column['name']
            data_type = TableController.get_column_type(column['data_type'])
            query += f"{name} {data_type}, "
        query = query.rstrip(', ') + ");"

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


