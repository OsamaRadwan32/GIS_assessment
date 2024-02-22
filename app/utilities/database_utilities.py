"""database_utilities.py"""

import os, json, csv
import psycopg2
from flask import jsonify
from ..config.db_connect import connect_to_db


@staticmethod
def check_table_exists(table_name):
    """
    Check if a table with the provided name exists in the database.

    Args:
        table_name (str): The name of the table.

    Returns:
        bool: True if the table exists, False otherwise.
    """
    query  = f"SELECT EXISTS ( "
    query += "SELECT 1 "
    query += "FROM information_schema.tables "
    query += f"WHERE table_name = '{table_name}' );"
    result = execute_query(query)
    if result == "(True,)":
        return True
    else: return False

@staticmethod
def construct_create_query(table_name, structure):
    # Parse table structure from JSON string
    structure_dict = json.loads(structure)
    # Build the SQL statement to create the table
    query = f"CREATE TABLE {table_name} ("
    query += " id SERIAL PRIMARY KEY NOT NULL, "
    for column in structure_dict:
        name = column['name']
        data_type = TableServices.get_column_type(column['data_type'])
        if data_type:
            query += f"{name} {data_type}, "
        else: return jsonify({'error': 'wrong datatypes provided'}), 400
    query = query.rstrip(', ') + ");"
    return query

@staticmethod
def construct_insert_query(table_name, structure, data):
    # Parse table structure from JSON string
    structure_dict = json.loads(structure)
    # Build the INSERT query
    query = f"INSERT INTO {table_name} ("
    for column in structure_dict:
        name = column['name']
        query += f"{name}, "
    query = query.rstrip(', ')
    query += ") VALUES"
    for row in data:
        values = ', '.join([f"'{value}'" for value in row])
        query += f" ({values}),"
    query = query.rstrip(',') + ";"
    return query

@staticmethod
def execute_query(query):
    try:
        # Create a cursor to connect to the database
        connection = connect_to_db()
        cursor = connection.cursor()
        print(f"Executing Query: {query}")
        cursor.execute(query)
        connection.commit()
        # Check if the query executed successfully (cursor.execute() returns None)
        if cursor.rowcount != -1:
            # If rowcount is -1, it means the query was successfully executed
            return jsonify({"error": "Error executing query"})
        cursor.close()
        connection.close()
        # If no exceptions were raised, the query syntax is valid
        return True, None
    except psycopg2.Error as e:
        # If an exception occurred, handle it and return an error message
        error_message = str(e)
        return False, error_message