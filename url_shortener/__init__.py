import sqlite3
from flask import Flask
from hashids import Hashids

def get_db_connection():
    '''Connect to database'''
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

app = Flask(__name__)
app.config['SECRET_KEY'] = 'adcc44cbad9ffb87d2b29e554eacefd9d3c8ffaaea7bbf96ee97'
hashids = Hashids(salt=app.config['SECRET_KEY'], min_length=4)