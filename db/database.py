import sqlite3
import os

DB_PATH = os.path.join("data", "documents.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Document table - Schema
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        path TEXT,
        thumbnail_path TEXT,
        tags TEXT,
        description TEXT,
        upload_date TEXT,
        lecture_date TEXT,
        total_pages INTEGER
        )
    """
    )

    

    conn.commit()
    print("DB operation successfull.")
    conn.close()

