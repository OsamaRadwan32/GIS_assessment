import os
from flask import Flask, jsonify
from .config.db_connect import connect_to_db
from .routes.main_routes import main_routes

app = Flask(__name__)

# Register Blueprints (routes)
app.register_blueprint(main_routes)

@app.route('/dbConnect')
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

if __name__ == '__main__':
    with app.test_request_context():
        # Generate URLs using url_for()
        # content = url_for('homepage')
        # tables = url_for('get_users', username='antony')
        # users = url_for('get_tables', post_id=456, slug='flask-intro' )
        print("Generated URLs:")
        print("Content URLs:", content)
        print("Table URLs:", tables)
        print("User URLs::", users)

