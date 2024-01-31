"""app.py"""

import os
from flask import Flask, jsonify
from .config.db_connect import connect_to_db
from .routes.main_routes import main_routes
from . import db

# App Initialization
from . import create_app, db_connection # from __init__ file

app = create_app()

if __name__ == "__main__":
    db.create_all()  # Create tables based on models
    app.run()

# Register Blueprints (routes)
app.register_blueprint(main_routes, url_prefix='/')