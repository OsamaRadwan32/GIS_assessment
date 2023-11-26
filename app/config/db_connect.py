from flask import Flask
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

def connect_to_db():
    conn = psycopg2.connect(
        dbname=os.getenv('DATABASE'),
        user=os.getenv('USERNAME'),
        password=os.getenv('PASSWORD'),
        host=os.getenv('HOST'),
        port=os.getenv('PORT')
    )
    return conn

@app.route('/')
def index():
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
    app.run(debug=True)



app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DEBUG'] = os.getenv('DEBUG')
