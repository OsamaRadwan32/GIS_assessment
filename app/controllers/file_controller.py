from flask import Flask, request, jsonify
import pandas as pd


class FileController:
    @staticmethod
    def upload_file(file):
        if 'file' not in file:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if file:
            df = pd.read_csv(file)
            column_names = df.columns.tolist()
            return jsonify({'columns': column_names}), 200

        return jsonify({'error': 'Unknown error occurred'}), 500