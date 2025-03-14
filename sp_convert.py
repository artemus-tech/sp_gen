import numpy as np
import psycopg2
import io

import dbassets

# Create a NumPy array
#dbassets.update_field_by_unique_field()

dbassets.fetch_all_as_dict(table_name="sp_gen")

# Serialize the array to a byte string
byte_io = io.BytesIO()
np.save(byte_io, array)
byte_string = byte_io.getvalue()

# Connect to PostgreSQL
conn = psycopg2.connect("dbname=test user=postgres password=secret")
cursor = conn.cursor()

# Store the byte string in the database
cursor.execute("INSERT INTO your_table (array_column) VALUES (%s)", (psycopg2.Binary(byte_string),))

# Commit and close the connection
conn.commit()
cursor.close()
conn.close()
