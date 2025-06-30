import sqlite3

conn = sqlite3.connect('casper.db')
c = conn.cursor()

# Add new columns if they don't exist
try:
    c.execute("ALTER TABLE ingredients ADD COLUMN chemical_class TEXT")
except:
    pass

try:
    c.execute("ALTER TABLE ingredients ADD COLUMN large_availability TEXT")
except:
    pass

conn.commit()
conn.close()
print("✅ Ingredients table updated!")