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

# Create ingredients table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        medication TEXT,
        ingredient TEXT
    )
''')

# ---- Add new columns to ingredients table if missing ----

def column_exists(table, column):
    cursor.execute(f"PRAGMA table_info({table})")
    return column in [row[1] for row in cursor.fetchall()]

if not column_exists("ingredients", "chemical_class"):
    cursor.execute("ALTER TABLE ingredients ADD COLUMN chemical_class TEXT")

if not column_exists("ingredients", "large_availability"):
    cursor.execute("ALTER TABLE ingredients ADD COLUMN large_availability TEXT")

# Commit and close
conn.commit()
conn.close()

print("✅ Database initialized and schema updated")
