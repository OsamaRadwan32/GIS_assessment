"""table_utilities.py"""

import os
from .. import db
from ..models.tables_model import Table
from ..config.db_connect import connect_to_db

class TableServices:
    """
    TableUtilities class
    """
    @staticmethod
    def generate_tablename(user_id, table_name):
        """
        Generates a name for the file that is being uploaded to the server side

        Args:
            user_id (int): 
            table_name (str): 

        Returns:
            str: a string in the format of: user_id_table_name
        """
        return f"id{user_id}_{table_name}"
    
    @staticmethod
    def get_column_type(type):
        type_mapping = {
            'number': "INTEGER",
            'decimal': "DOUBLE PRECISION",
            'text': "VARCHAR(255)",
            'date': "DATE",
        }
        return type_mapping.get(type, String)

    @staticmethod
    def add_table_info(table_name, user_id, structure):
        """
        Adds the info of the new table as a record in the 'tables' table
        
        Parameters:
        - table_name(text): the name of the new table
        - user_id(serial): the id of the user
        - structure(string): the structure of the table to be created (in json format)
        """
        table_record = Table(
                            name        = table_name,
                            user_id     = user_id,
                            structure   = structure
                            )
        db.session.add(table_record)
        db.session.commit()
        
    @staticmethod
    def check_tablename_record(user_id, table_name):
        """
        Retrieve a record from the 'tables' table based on the provided name attribute.

        Parameters:
        - table_name (str): The name attribute to search for in the 'tables' table.

        Returns:
        - Table or None: If a record with the provided name is found, the corresponding
        Table object is returned. If no record is found, None is returned.
        """
            # Query the 'tables' table to find a record with the provided name
        table_record = Table.query.filter_by(user_id = user_id, name = table_name).first()

        # Check if the record exists
        if table_record:
            return True

    @staticmethod
    def check_table_exists(table_name):
        """_summary_

        Args:
            table_name (_type_): _description_

        Returns:
            _type_: _description_
        """
        query  = f"SELECT EXISTS ( "
        query += "SELECT 1 "
        query += "FROM information_schema.tables "
        query += f"WHERE table_schema = '{os.getenv('DATABASE')}' "
        query += f"AND table_name = '{table_name}' );"
        
        cursor = connect_to_db().cursor()
        return cursor.execute(query)
