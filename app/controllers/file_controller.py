from flask import Flask, request, jsonify
import csv
import pandas as pd

from .. import db
from ..models.dynamic_table_model import DynamicTable
from .table_controller import TableController

class FileController:
    @staticmethod
    def process_request(request):
        request_form = request.form.to_dict()

        table_name = request_form['table_name']
        table_structure = request_form['table_structure']
        file_name = request_form['file_name']
        uploaded_file = request.files[f'{file_name}']
        
        # Check if the uploaded file exists and has a CSV extension
        if not uploaded_file.filename or not uploaded_file.filename.endswith('.csv'):
            return jsonify({'error': 'No file provided or wrong file extension!'}), 400
        
        # Save the file in the desired location
        TableController.create_table_record(table_name, 1, table_structure)
        TableController.create_table(table_name, table_structure)
        FileController.populate_table(table_name, table_structure, uploaded_file)

        return jsonify({'message': 'Table created and populated successfully'}), 200

    @staticmethod
    def populate_table(table_name, table_structure, csv_file):        
        TableModel = db.Model.metadata.tables.get(table_name)
        
        if not TableModel:
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
                
