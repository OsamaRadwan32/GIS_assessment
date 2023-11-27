import os
from flask import Flask
from app.config.db_connect import connect_to_db
app = Flask(__name__)


@app.route('/')
def homepage():
    return 'Homepage'

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

@app.route('/users')
def get_users():
    return 'Users'

@app.route('/users/<int:user_id>')
def get_user(user_id):
    return f'Returning user of id: {user_id}'


@app.route('/tables')
def get_tables():
    return 'Tables'

@app.route('/tables/<int:table_id>')
def get_table(table_id):
    return f'Returning table of id: {table_id}'

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
