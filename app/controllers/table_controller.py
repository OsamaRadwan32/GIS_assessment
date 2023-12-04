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
                            name    = table_name,
                            user_id = user_id,
                            )
        db.session.add(table_record)
        db.session.commit()

    @staticmethod
    def create_table(request):
        if not request.json:
            return jsonify({'error': 'No data provided'}), 400

        user_id = request.json.get('user_id')
        table_name = request.json.get('table_name')
        columns = request.json.get('columns')
        datatypes = request.json.get('datatypes')

        if not columns or not datatypes:
            return jsonify({'error': 'Columns or datatypes missing'}), 400

        if len(columns) != len(datatypes):
            return jsonify({'error': 'Mismatch in columns and datatypes'}), 400

        try:
            metadata = MetaData()
            new_table = Table(f'{table_name}', metadata, *[Column(col, getattr(Integer, dtype)) for col, dtype in zip(columns, datatypes)])
            new_table.create(bind=db.engine)
            TableController.create_table_record(table_name, user_id)
            return jsonify({'message': f'Table {table_name} created successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # @staticmethod
    # def populate_table(request):