import pandas as pd
import sqlite3

# Load Excel file
excel_file = 'Casper Data.xlsx'
xl = pd.ExcelFile(excel_file)

# Medication section
med_df = xl.parse('Sheet1').iloc[1:, 0:5]
med_df.columns = ['medication', 'date', 'time', 'dose', 'units']
med_df['date'] = pd.to_datetime(med_df['date']).dt.date  # format to YYYY-MM-DD

# Urination section
uri_df = xl.parse('Sheet1').iloc[1:, 6:10]
uri_df.columns = ['date', 'time', 'size', 'location']
uri_df['date'] = pd.to_datetime(uri_df['date']).dt.date

# Connect to DB
conn = sqlite3.connect('casper.db')
c = conn.cursor()

# Insert medication entries
for _, row in med_df.iterrows():
    if pd.notnull(row['medication']):
        c.execute('''
            INSERT INTO medication (medication, date, time, dose, units)
            VALUES (?, ?, ?, ?, ?)
        ''', (row['medication'], str(row['date']), str(row['time'])  # for both med_df and uri_df inserts
, row['dose'], row['units']))

# Insert urination entries
for _, row in uri_df.iterrows():
    if pd.notnull(row['size']):
        c.execute('''
            INSERT INTO urination (date, time, size, location)
            VALUES (?, ?, ?, ?)
        ''', (str(row['date']), str(row['time'])  # for both med_df and uri_df inserts
, row['size'], row['location']))

conn.commit()
conn.close()

print("✅ Excel data successfully imported into SQLite.")
