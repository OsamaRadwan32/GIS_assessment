from flask import Blueprint, request, jsonify
from sqlalchemy import MetaData, Table, Column, Integer, String

import uuid

from .. import app, db
from ..models.tables_model import Table

table_bp = Blueprint('table_bp', __name__)

class TableController:

    @staticmethod
    def create_table_record(table_name, user_id, structure):
        table_record = Table(
                            name        = table_name,
                            user_id     = user_id,
                            structure   = structure
                            )
        db.session.add(table_record)
        db.session.commit()

    @staticmethod
    def create_table(table_name, user_id, structure):
        
        table_columns = {
            'id': db.Column(db.Integer, primary_key=True)
        }

        for col in structure:
            col_name = col['name']
            data_type = col['data_type']
            
            # Map data types to SQLAlchemy types
            if data_type == 'integer':
                column = db.Column(db.Integer)
            elif data_type == 'string':
                column = db.Column(db.String(255))  # Replace 255 with desired string length
            
            table_columns[col_name] = column

        try:
            table = type(table_name, (db.Model), table_columns)
            db.create_all()
            return jsonify({'message': f'Table {table_name} created successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500