import pandas as pd
import sqlite3
from pathlib import Path

# Database and CSV file paths
db_path = Path(__file__).parent.parent /"app" /"db.sqlite"
csv_path = 'flipkart_product_data.csv'

# Connect to SQLite database (creates one if not exists)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Drop existing product table if it exists
cursor.execute('DROP TABLE IF EXISTS product;')

# Create a fresh product table
cursor.execute('''
CREATE TABLE product (
    product_link TEXT,
    title TEXT,
    brand TEXT,
    price INTEGER,
    discount FLOAT,
    avg_rating FLOAT,
    total_ratings INTEGER
);
''')

# Commit the table creation
conn.commit()

# Read CSV file using pandas
df = pd.read_csv(csv_path)

# Insert data into the product table
df.to_sql('product', conn, if_exists='append', index=False)

# Close the connection
conn.close()

print("✅ Data inserted successfully! (Existing table was overwritten.)")