import os
from flask import Flask
from config.db_connect import connect_to_db
from routes.index_routes import main_routes

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
        return f'PostgreSQL Database Version: {db_version}'
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
 with app.test_request_context():
   # Generate URLs using url_for()
   homepage = url_for('homepage')
   get_users = url_for('get_users', username='antony')
   get_tables = url_for('get_tables', post_id=456, slug='flask-intro' )

   print("Generated URLs:")
   print("Home URL:", homepage)
   print("Users:", get_users)
   print("Tables::", get_tables)
