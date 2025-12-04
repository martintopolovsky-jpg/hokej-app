import sqlite3

conn = sqlite3.connect("hokej.db")
conn.execute("""
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    position TEXT,
    confirmed INTEGER
)
""")
conn.close()

print("hokej.db vytvorená!")
