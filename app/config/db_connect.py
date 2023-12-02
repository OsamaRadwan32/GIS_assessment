from flask import Flask
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

# Normal database connection
def connect_to_db():
    conn = psycopg2.connect(
        dbname=os.getenv('DATABASE'),
        user=os.getenv('USERNAME'),
        password=os.getenv('PASSWORD'),
        host=os.getenv('HOST'),
    )
    return conn



