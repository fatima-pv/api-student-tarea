
import os
import sqlite3

DB_PATH = os.getenv("DB_PATH", "/data/students.sqlite")

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

sql_query = """
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL,
    gender TEXT NOT NULL,
    age TEXT
);
"""

cursor.execute(sql_query)
conn.commit()
conn.close()
