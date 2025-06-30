import sqlite3

# Connect to the database (creates file if it doesn't exist)
conn = sqlite3.connect('casper.db')
cursor = conn.cursor()

# Create medication table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS medication (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        medication TEXT,
        date TEXT,
        time TEXT,
        dose REAL,
        units TEXT
    )
''')

# Create urination table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS urination (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        time TEXT,
        size TEXT,
        location TEXT
    )
''')

# Create ingredients table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        medication TEXT,
        ingredient TEXT
    )
''')

# Commit changes and close connection
conn.commit()
conn.close()

print("✅ Database initialized")
