class FileUtilities:
    """
    FileUtilities class
    """
    def allowed_file_extensions(filename):
        """
        Check the extension of the file uploaded and makes sure its a csv one 
        """
        # Allowed file extensions
        ALLOWED_EXTENSIONS = {'csv'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    def save_uploaded_file(file):
        """
        save the uploaded folder in the ../static/tables/ folder 
        """
        # Check if the file has an allowed extension
        if file and FileController.allowed_file(file.filename):
            # Generate a secure filename to avoid potential security issues
            filename = secure_filename(file.filename)
            
        # Set the upload folder
        UPLOAD_FOLDER = '../static/tables/'
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        # Save the file to the upload folder
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
