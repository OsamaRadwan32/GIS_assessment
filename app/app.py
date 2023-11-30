# import os

# app = Flask(__name__)

# if __name__ == '__main__':
#     with app.test_request_context():
#         # Generate URLs using url_for()
#         # content = url_for('homepage')
#         # tables = url_for('get_users', username='antony')
#         # users = url_for('get_tables', post_id=456, slug='flask-intro' )
#         print("Generated URLs:")
#         print("Content URLs:", content)
#         print("Table URLs:", tables)
#         print("User URLs::", usaers)

import os
from flask import Flask, jsonify
from .config.db_connect import connect_to_db
from .routes.main_routes import main_routes

# App Initialization
from . import create_app, db_connection # from __init__ file

app = create_app()

# Register Blueprints (routes)
app.register_blueprint(main_routes)


# Hello World!
@app.route('/')
def hello():
    return "Hello World!"

@app.route('/dbConnect')
def db_connection():
    return db_connection() 

if __name__ == "__main__":
    app.run()