import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
''')

# Insert sample user
cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', '1234'))

conn.commit()
conn.close()

print("Database created successfully!")