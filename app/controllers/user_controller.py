from flask import Blueprint

user_bp = Blueprint('user_bp', __name__)

class UserController:
    @staticmethod
    @user_bp.route('/users', methods=['GET'])
    def get_users():
        # Logic to fetch users from the database
        return 'List of users'

    @staticmethod
    @user_bp.route('/user/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        # Logic to fetch a single user based on user_id
        return f'User with ID {user_id}'

    # Other user-related routes and logic
    # For example, POST, PUT, DELETE methods

# Additional routes can be added in a similar manner in post_controller.py or other controller files.
