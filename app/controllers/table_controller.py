"""table_controller.py"""

import csv, json
import pandas as pd
from sqlalchemy import Table, MetaData, create_engine
from sqlalchemy.orm import sessionmaker
from flask import Blueprint, jsonify
from .. import db
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
            query = TableServices.construct_create_query(table_name, structure)
            is_valid = TableServices.execute_query(query)
            table_exists = TableServices.check_table_exists(table_name)
            if is_valid and table_exists:
                return jsonify({'message': f'Table {table_name} created successfully'}), 200
            else:
                print(f"Error: {error_message}")
        except Exception as e:
            # Handle the exception and return a custom response
            error_message = str(e)
            return jsonify({"error": error_message}), 500  

    # @staticmethod
    # def create_table_in_db(table_name, structure):
    #     """
    #     Creates a new table in the database given the table_name and structure
        
    #     Parameters:
    #         table_name(str): the name of the new table
    #         structure(str): the structure of the table to be created (in json format)
    #     """
    #     try:        
    #         # Create a cursor to connect to the database
    #         connection = connect_to_db()
    #         cursor = connection.cursor()
    #         query = TableServices.construct_create_query(table_name, structure)
    #         print(f"Executing query: {query}")
    #         cursor.execute(query)
    #         # Check if the query executed successfully (cursor.execute() returns None)
    #         if cursor.rowcount != -1:
    #             # If rowcount is -1, it means the query was successfully executed
    #             return jsonify({"error": "Error creating table"})
    #         connection.commit()
    #         TableServices.check_table_exists(table_name)
    #     except Exception as e:
    #         # Handle the exception and return a custom response
    #         error_message = str(e)
    #         return jsonify({"error": error_message}), 500  

    @staticmethod
    def populate_table(table_name, structure, csv_file_path):
        try:
            data = TableServices.convert_csv_content_into_tuples(csv_file_path)
            query = TableServices.construct_insert_query(table_name, structure, data)
            is_valid = TableServices.execute_query(query)
            if is_valid:
                return jsonify({'message': f'Table {table_name} populated successfully'}), 200
            else:
                print(f"Error: {error_message}")
        except Exception as e: 
            # Handle the exception and return a custom response
            error_message = str(e)
            return jsonify({"error": error_message}), 500  
