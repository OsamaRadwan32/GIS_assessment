import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from .config import db_connect

db = SQLAlchemy()
migrate = Migrate()

# Creating app instance with SQLAlchemy database connection
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
    db.init_app(app)
    migrate.init_app(app, db)

    return app

# Connecting to the database without SQLAlchemy
def db_connection():
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        cur.close()
        conn.close()
        return jsonify({'message': f'PostgreSQL Database Version: {db_version}'}) 
    except Exception as e:
        return jsonify({'message': f'Error: {e}' }) 