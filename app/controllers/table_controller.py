"""table_controller.py"""

import csv
import json
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
        # Check if the table exists
        table_model = db.Model.metadata.tables.get(table_name)
        if not table_model:
            return jsonify({"error": "Table does not exist"}), 404

        try:
            # Parse table structure from JSON string
            columns = json.loads(table_structure)

            # Open the CSV file
            with open(csv_file, 'r') as file:
                reader = csv.DictReader(file)

                # Iterate over rows in the CSV file
                for row in reader:
                    # Create a dictionary to store column values
                    column_values = {}

                    # Iterate over columns in the table structure
                    for column in columns:
                        # Get the value from the CSV row corresponding to the column name
                        value = row.get(column)

                        # Add the column name and value to the dictionary
                        column_values[column] = value

                    # Create a new record in the table using SQLAlchemy
                    new_record = Table(**column_values)
                    db.session.add(new_record)

            # Commit the transaction
            db.session.commit()

            return jsonify({"message": f"Data added to table {table_name} successfully."}), 200
        except Exception as e:
            # Handle the exception and log or print an error message
            error_message = str(e)
            print(f"Error: {error_message}")

            # Rollback the transaction
            db.session.rollback()

            return jsonify({"error": error_message}), 500
        
    @staticmethod
    def populate_table(table_name, table_structure, csv_file):
        """
        Add data from CSV file to the specified table using SQLAlchemy and PostgreSQL.

        Parameters:
            table_name (str): Name of the table to add data to.
            table_structure (str): JSON string containing the table structure (column names).
            csv_file (str): Path to the CSV file containing data.
            db_uri (str): Database URI for SQLAlchemy to connect to.

        Returns:
            str: Message indicating success or failure.
        """
        try:
            # Parse table structure from JSON string
            columns = json.loads(table_structure)

            # Create SQLAlchemy table object dynamically
            metadata = MetaData()
            table = Table(table_name, metadata, *[Column(column, String) for column in columns])

            # Create SQLAlchemy engine and session
            engine = create_engine(db_uri)
            Session = sessionmaker(bind=engine)
            session = Session()

            # Open the CSV file
            with open(csv_file, 'r') as file:
                reader = csv.DictReader(file)

                # Iterate over rows in the CSV file
                for row in reader:
                    # Create a dictionary to store column values
                    column_values = {}

                    # Iterate over columns in the table structure
                    for column in columns:
                        # Get the value from the CSV row corresponding to the column name
                        value = row.get(column)

                        # Add the column name and value to the dictionary
                        column_values[column] = value

                    # Insert data into the table
                    session.execute(table.insert().values(**column_values))

            # Commit the transaction
            session.commit()

            return jsonify({"message": f"Data added to table {table_name} successfully."}), 200

        except Exception as e:
            # Handle the exception and log or print an error message
            error_message = str(e)
            print(f"Error: {error_message}")

            # Rollback the transaction
            session.rollback()

            return jsonify({"error": error_message}), 500
