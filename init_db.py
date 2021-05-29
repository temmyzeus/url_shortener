import sqlite3

connection = sqlite3.connect('database.db')#tries to connect to specified DB and creates new DB if not found

# Read DB creation sript from file
with open('schema.sql', mode='r') as f:
    connection.executescript(f.read())

connection.commit()
connection.close() 