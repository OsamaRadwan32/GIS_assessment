from flask import Flask, request, jsonify
import csv
import pandas as pd

from .. import db
from .table_controller import TableController

class FileController:
    @staticmethod
    def process_request(request):
        request_form = request.form.to_dict()

        table_name = request_form['table_name']
        table_structure = request_form['table_structure']
        file_name = request_form['file_name']
        uploaded_file = request.files[f'{file_name}']
        
        if not uploaded_file.filename:
            return jsonify({'error': 'No file provided'}), 400
        # Save the file in the desired location
        uploaded_file.save(uploaded_file.filename)
        TableController.create_table_record(table_name, 1, table_structure)
        TableController.create_table(table_name, table_structure)
        FileController.pop
        return 'File uploaded successfully'

    # @staticmethod
    # def populate_table(table_name, uploaded_file):


    @staticmethod
    def upload_file(request):
        table_name = request.name
        # Assuming 'file' is the name of the file input field in the form
        csv_file = request.files['file']
        
        if not csv_file:
            return jsonify({'error': 'No file provided'}), 400
        
        stream = io.StringIO(csv_file.stream.read().decode("UTF8"), newline=None)
        csv_reader = csv.reader(stream)
        next(csv_reader)  # Skip header row if exists
        
        try:
            for row in csv_reader:
                # Assuming columns are in the order: col1, col2, col3, etc.
                new_row = YourTable(col1=row[0], col2=row[1], col3=row[2])  # Replace col1, col2, col3 with your actual column names
                db.session.add(new_row)
            
            db.session.commit()
            return "CSV data inserted into the database successfully"
        except Exception as e:
            db.session.rollback()
            return f"Failed to insert CSV data: {str(e)}", 500
        finally:
            db.session.close()
