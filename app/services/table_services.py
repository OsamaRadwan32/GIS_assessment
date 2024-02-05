"""table_utilities.py"""

import os
import json
from flask import jsonify
from .. import db
from ..models.tables_model import Table
from ..config.db_connect import connect_to_db

class TableServices:
    """
    TableUtilities class
    """
    
    @staticmethod
    def generate_tablename(user_id, table_name):
        """
        Generates a name for the file that is being uploaded to the server side

        Args:
            user_id (int): User ID.
            table_name (str): Table name.

        Returns:
            str: A string in the format of: id{user_id}_{table_name}.
        """
        return f"id{user_id}_{table_name}"
    
    @staticmethod
    def get_column_type(type):
        """
        Get the corresponding database column type for a given structure type.

        Args:
            type (str): Structure type.

        Returns:
            str: Database column type.
        """
        type_mapping = {
            'number': "INTEGER",
            'decimal': "DOUBLE PRECISION",
            'text': "VARCHAR(255)",
            'date': "DATE",
        }
        return type_mapping.get(type)

    @staticmethod
    def add_table_info(table_name, user_id, structure):
        """
        Adds the info of the new table as a record in the 'tables' table
        
        Parameters:
        - table_name (str): The name of the new table.
        - user_id (int): The ID of the user.
        - structure (str): The structure of the table to be created (in JSON format).
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
        Check if a record with the provided name and user_id exists in the 'tables' table.

        Parameters:
        - user_id (int): The ID of the user.
        - table_name (str): The name attribute to search for in the 'tables' table.

        Returns:
        - bool: True if a record with the provided name and user_id exists, False otherwise.
        """
            # Query the 'tables' table to find a record with the provided name
        table_record = Table.query.filter_by(user_id = user_id, name = table_name).first()
        # Check if the record exists
        if table_record:
            return True
        else: return False

    @staticmethod
    def check_table_exists(table_name):
        """
        Check if a table with the provided name exists in the database.

        Args:
            table_name (str): The name of the table.

        Returns:
            bool: True if the table exists, False otherwise.
        """
        query  = f"SELECT EXISTS ( "
        query += "SELECT 1 "
        query += "FROM information_schema.tables "
        query += f"WHERE table_name = '{table_name}' );"
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        connection.commit()
        if result == "(True,)":
            return True
        else: return False

    @staticmethod
    def construct_create_query(table_name, structure):
        # convert the structure string into a dictionary
        structure_dict = json.loads(structure)
        # Build the SQL statement to create the table
        query = f"CREATE TABLE {table_name} ("
        query += " 'id' SERIAL PRIMARY KEY NOT NULL, "
        for column in structure_dict:
            name = column['name']
            data_type = TableServices.get_column_type(column['data_type'])
            if data_type:
                query += f"'{name}' {data_type}, "
            else: return jsonify({'error': 'wrong datatypes provided'}), 400
        query = query.rstrip(', ') + ");"
        print(f"QUERY: {query}")
        return query
