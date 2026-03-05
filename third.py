import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    group_name TEXT
)
""")

cursor.execute("INSERT INTO students (name, group_name) VALUES (?, ?)", ("Иван", "111"))
cursor.execute("INSERT INTO students (name, group_name) VALUES (?, ?)", ("Катя", "112"))

conn.commit()
conn.close()
