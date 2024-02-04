""" file_controller.py """

import csv
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify
import pandas as pd
from .. import db
from ..models.dynamic_table_model import DynamicTable
from .table_controller import TableController
from ..services.table_services import TableServices
from ..services.file_services import FileServices

class FileController:
    """
    File Controller class
    """
    @staticmethod
    def process_request(request):
        """
        Adds two numbers and returns the result.

        Parameters:
            request object containing the following attributes:
                - table_name (str): the name of the table to create.
                - table_structure (json): the table structure in json format.
                - file_name (str): the name of the uploaded file.
                - file(file): the actual uploaded file.
        """
        request_form = request.form.to_dict()

        table_name = request_form['table_name']
        table_structure = request_form['table_structure']
        db_table_name = TableServices.generate_tablename(3, table_name)
        
        try:    
            # check if there is a record with the same table name in the 'tables' table
            # and if their is a table holding the db_table_name existing in the database
            table_record_exists = TableServices.check_tablename_record(3, db_table_name)
            table_exists = TableServices.check_table_exists(db_table_name)
            
            if table_record_exists or table_exists:
                return jsonify({"error": "Table already exists in the database. choose another name"}), 400  

            # Creating a record of the table info in the 'tables' table
            TableServices.add_table_info(db_table_name, 3, table_structure)
            
            # Check if the uploaded file exists and has a CSV extension
            file = request.files['file']
            file_name = file.filename
            check_filename = FileServices.allowed_file_extensions(file_name)
            if 'file' not in request.files or not check_filename:
                return jsonify({'error': 'No selected file or wrong file extension!'}), 400
                
            # Save the file in the static/tables folder
            FileServices.save_uploaded_file(db_table_name, file)
    
            TableController.create_table_in_db(db_table_name, table_structure)
            # FileController.populate_table(table_name, table_structure, file)

            return jsonify({'message': 'Table created and populated successfully'}), 200
        except Exception as e:
            # Handle the exception and return a custom response
            error_message = str(e)
            return jsonify({"error": error_message}), 500  
        
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

