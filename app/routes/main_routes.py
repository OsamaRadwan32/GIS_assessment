# routes.py
from flask import Blueprint, jsonify
from content_routes import content_routes
from table_routes import table_routes
from user_routes import user_routes

# Create a Blueprint instance
main_routes = Blueprint('main_routes', __name__)

# Define your routes
@main_routes.route('/')
def index():
    return jsonify({'message': 'Welcome to the main page'})

@main_routes.route('/about')
def about():
    return jsonify({'message': 'About page'})

# More routes...
@main_routes.route('/users')
def get_users():
    return 'Users'

@main_routes.route('/users/<int:user_id>')
def get_user(user_id):
    return f'Returning user of id: {user_id}'


@main_routes.route('/tables')
def get_tables():
    return 'Tables'

@main_routes.route('/tables/<int:table_id>')
def get_table(table_id):
    return f'Returning table of id: {table_id}'

app.register_blueprint(content_routes, url_prefix='/content')
app.register_blueprint(content_routes, url_prefix='/table')
app.register_blueprint(content_routes, url_prefix='/user')