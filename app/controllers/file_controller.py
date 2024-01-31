""" file_controller.py """

import csv
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify
import pandas as pd
from .. import db
from ..models.dynamic_table_model import DynamicTable
from .table_controller import TableController
from ..utilities.file_utilities import FileUtilities

class FileController:
    """
    File Controller class
    """

    @staticmethod
    def process_request(request):
        """
        Adds two numbers and returns the result.

        Parameters:
        - request object containing the following attributes:
            - table_name (str): the name of the table to create.
            - table_structure (json): the table structure in json format.
            - file_name (str): the name of the uploaded file.
            - file(file): the actual uploaded file.
        """
        request_form = request.form.to_dict()

        table_name = request_form['table_name']
        table_structure = request_form['table_structure']

        # check if there is a record with the same table name in the 'tables' table
        table_exists = TableController.get_table_by_name(table_name)
        if not table_exists:
            # Creating a record of the table info in the 'tables' table
            TableController.add_table_info(table_name, 3, table_structure)
            if 'file' not in request.files:
                return jsonify({'error': 'No file part'}), 400

            file = request.files['file']

            uploaded_file_name = file.filename
            # Check if the uploaded file exists and has a CSV extension
            if uploaded_file_name == '':
                return jsonify({'error': 'No selected file or wrong file extension!'}), 400
            
            # Save the file in the static/tables folder
            FileUtilities.save_uploaded_file(table_name, 3, file)
        else:
            return (jsonify({
                'error': f'Unable to process request, a table of name {table_name} already'
                ' exists in the database'}),
                400)

        # TableController.create_table(table_name, table_structure)
        # FileController.populate_table(table_name, table_structure, file)

        return jsonify({'message': 'Table created and populated successfully'}), 200

    @staticmethod
    def populate_table(table_name, table_structure, csv_file):
        """
        Adds two numbers and returns the result.

        Parameters:
        - a (int): The first number.
        - b (int): The second number.

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

