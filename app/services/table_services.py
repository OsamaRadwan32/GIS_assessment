"""table_utilities.py"""

from .. import db
from ..models.tables_model import Table

class TableServices:
    """
    Table services class
    """
    
    @staticmethod
    def generate_tablename(user_id, table_name):
        """
        Generates a name for the file that is being uploaded to the server side

        Args:
            user_id (int): User ID.
            table_name (str): Table name.

        Returns:
            str: A string in the format of: id{user_id}_{table_name}.
        """
        return f"id{user_id}_{table_name}"
    
    @staticmethod
    def get_column_type(type):
        """
        Get the corresponding database column type for a given structure type.

        Args:
            type (str): Structure type.

        Returns:
            str: Database column type.
        """
        type_mapping = {
            'number': "INTEGER",
            'decimal': "DOUBLE PRECISION",
            'text': "VARCHAR(255)",
            'date': "DATE",
        }
        return type_mapping.get(type)

    @staticmethod
    def add_table_info(table_name, user_id, structure, reference_file):
        """
        Adds the info of the new table as a record in the 'tables' table
        
        Parameters:
        - table_name (str): The name of the new table.
        - user_id (int): The ID of the user.
        - structure (str): The structure of the table to be created (in JSON format).
        """
        table_record = Table(
                            name            = table_name,
                            user_id         = user_id,
                            structure       = structure,
                            reference_file  = reference_file
                            )
        db.session.add(table_record)
        db.session.commit()
        
    @staticmethod
    def check_tablename_record(user_id, table_name):
        """
        Check if a record with the provided name and user_id exists in the 'tables' table.

        Parameters:
        - user_id (int): The ID of the user.
        - table_name (str): The name attribute to search for in the 'tables' table.

        Returns:
        - bool: True if a record with the provided name and user_id exists, False otherwise.
        """
            # Query the 'tables' table to find a record with the provided name
        table_record = Table.query.filter_by(user_id = user_id, name = table_name).first()
        # Check if the record exists
        if table_record:
            return True
        else: return False
