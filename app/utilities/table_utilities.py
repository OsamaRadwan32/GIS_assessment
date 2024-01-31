"""table_utilities.py"""

class TableUtilities:
    """
    TableUtilities class
    """    
    def generate_tablename(user_id, table_name):
        """
        Generates a name for the file that is being uploaded to the server side

        Args:
            user_id (int): 
            table_name (str): 

        Returns:
            str: a string in the format of: user_id_table_name
        """
        return f"{user_id}_{table_name}"

