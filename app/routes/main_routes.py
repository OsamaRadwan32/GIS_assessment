from flask import Blueprint, jsonify
from ..config.db_connect import connect_to_db
from .. import db_connection

from .content_routes import content_routes
from .tables_routes import table_routes
from .users_routes import user_routes
from .file_routes import file_routes
from .authentication_routes import authentication_routes

# Create a Blueprint instance
main_routes = Blueprint('main_routes', __name__)

# Define your routes
@main_routes.route('/')
def index():
    return jsonify({'message': 'Welcome to the main page'})

@main_routes.route('/dbConnect')
def normal_db_connection():
    return db_connection()

# @main_routes.route('/content')
# def content():
#     return jsonify({'message': 'Content page'})

# @main_routes.route('/tables')
# def get_tables():
#     return jsonify({'message': 'Tables page'})

# @main_routes.route('/users')
# def get_users():
#     return jsonify({'message': 'Users page'})

# @main_routes.route('/auth')
# def get_users():
#     return jsonify({'message': 'Auth page'})

main_routes.register_blueprint(content_routes, url_prefix='/content')
main_routes.register_blueprint(table_routes, url_prefix='/tables')
main_routes.register_blueprint(user_routes, url_prefix='/users')
main_routes.register_blueprint(file_routes, url_prefix='/file')
main_routes.register_blueprint(authentication_routes, url_prefix='/auth')