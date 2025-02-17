import sqlite3
from flask import g
from app import app
import os

# Point directly to the existing database
import sqlite3
from flask import g
from app import app
import os

# Point to the existing database in the 'data' directory
DATABASE = 'data/data_web.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    # Just establish connection to verify database exists
    db = get_db()
    try:
        # Test connection by querying the sqlite_master table
        db.execute('SELECT name FROM sqlite_master WHERE type="table"').fetchall()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        raise

# Initialize the database when the app starts
with app.app_context():
    init_db()

# Register database close function
app.teardown_appcontext(close_db)