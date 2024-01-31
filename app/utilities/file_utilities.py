"""file_utilities.py"""

import os
from datetime import datetime
from flask import Flask, jsonify
from werkzeug.utils import secure_filename

class FileUtilities:
    """
    FileUtilities class
    """
    def allowed_file_extensions(filename):
        """
        Check the extension of the file uploaded and mak`es sure its a csv one 
        """
        # Allowed file extensions
        ALLOWED_EXTENSIONS = {'csv'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    def generate_filename(user_id, table_name):
        """
        Generates a name for the file that is being uploaded to the server side

        Args:
            user_id (int): _description_
            file_name (str): _description_

        Returns:
            str: a string in the format of: datetime_user_id_original_filename.csv
        """
        project_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        tables_folder_path = f'{project_folder_path}/static/tables/'
        print(f"FOLDER PATH: {tables_folder_path}") 

        current_datetime = datetime.now()
        
        # Custom format: Year-Month-Day Hour:Minute:Second
        formatted_datetime = current_datetime.strftime("%Y-%m-%d-%H-%M-%S")
        new_filename = secure_filename(f'{formatted_datetime}_id{user_id}_{table_name}.csv')
        print(f"FILE NAME: {new_filename}") 

        return os.path.join(tables_folder_path, new_filename)
    
    def check_directory_exists(path):
        """"""
        if os.path.exists(path):
            print(f"The directory '{path}' exists.")
        else:
            print(f"The directory '{path}' does not exist.")
        
    
    def save_uploaded_file(table_name, user_id, file):
        """
        secures the name of the file and then saves it in the static/tables/ folder 
        """
        # Check if the file has an allowed extension
        if file and FileUtilities.allowed_file_extensions(file.filename):
            # Generate a new name for the file to be uploaded on the server
            upload_file = FileUtilities.generate_filename(user_id, table_name)   
            # Save the file to the upload folder
            file.save(upload_file)
        else:
            return jsonify({'error': 'Error uploading file'}), 400

