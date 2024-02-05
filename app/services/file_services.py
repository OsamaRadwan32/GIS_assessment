"""file_utilities.py"""

import os
from datetime import datetime
from flask import Flask, jsonify
from werkzeug.utils import secure_filename

class FileServices:
    """
    FileUtilities class
    """
    def allowed_file_extensions(filename):
        """
        Check the extension of the file uploaded and ensures it is a CSV file.

        Args:
            filename (str): The name of the file.

        Returns:
            bool: True if the file extension is allowed, False otherwise.
        """
        # Allowed file extensions
        ALLOWED_EXTENSIONS = {'csv'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    def generate_filename(table_name):
        """
        Generates a name for the file that is being uploaded to the server side.

        Args:
            table_name (str): The name of the table.

        Returns:
            str: A string in the format of: datetime_table_name.csv.
        """
        project_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        tables_folder_path = f'{project_folder_path}/static/tables/'

        current_datetime = datetime.now()
        
        # Custom format: Year-Month-Day Hour:Minute:Second
        formatted_datetime = current_datetime.strftime("%Y-%m-%d-%H-%M-%S")
        new_filename = secure_filename(f'{formatted_datetime}_{table_name}.csv')

        return os.path.join(tables_folder_path, new_filename)
    
    def check_directory_exists(path):
        """
        Checks if a given path really exists or not.

        Args:
            path (str): The path of the directory to search.
        """
        if os.path.exists(path):
            print(f"The directory '{path}' exists.")
        else:
            print(f"The directory '{path}' does not exist.")
        
    
    def save_uploaded_file(filename, file):
        """
        Secures the name of the file and then saves it in the static/tables/ folder.

        Args:
            filename (str): The name of the file.
            file (file): The uploaded file.

        Returns:
            _type_: _description_
        """
        try:
            # Generate a new name for the file to be uploaded on the server
            upload_file = FileServices.generate_filename(filename)   
            # Save the file to the upload folder
            file.save(upload_file)
            return upload_file
        except Exception as e:
            # Handle the exception and return a custom response
            error_message = str(e)
            print(f"Error: {error_message}")
            return jsonify({'error': 'Error uploading file'}), 400
