# Module imports
import mariadb
import sys
import os

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user=os.environ.get('MARIADB_USER'),
        password=os.environ.get('MARIADB_KEY'),
        host=os.environ.get('MARIADB_HOST'),
        port=int(os.environ.get('MARIADB_PORT')),
        database=os.environ.get('MARIADB_DATABASE')
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()

# SQL

cur.execute('Select distinct entity_id FROM states')

for entity_id in cur:
   print(f"{entity_id}")

conn.close()