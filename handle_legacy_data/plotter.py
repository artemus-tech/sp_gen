import os

import numpy as np
import psycopg2
import matplotlib.pyplot as plt

import constants as const



conn = psycopg2.connect(
    host="localhost",
    database="spgen",
    user="postgres",
    password="Dictionary108$"
)
cur = conn.cursor()

# Function to fetch src_path by table name
def fetch_src_path(table_name):
    # Define the SQL query to get the src_path column from the table
    query = f"SELECT src_path FROM {table_name};"

    result=[]

    try:
        # Execute the query
        cur.execute(query)

        # Fetch all rows (if the table has many rows, you can limit the number of results)
        rows = cur.fetchall()

        # Print the results
        for row in rows:
            result.append(row[0])  # assuming src_path is the first column in the row
        return result

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()



for filepath in fetch_src_path(const.tables[0]):
    M=np.loadtxt("C:/"+filepath)
    q_values = M[:,0]
    I_q_values= M[:,1]

    # Create the plot
    plt.plot(q_values, I_q_values, marker='o', linestyle='-', color='b')

    # Label the axes
    plt.xlabel('q (nm⁻¹)')
    plt.ylabel('I(q), arb.units')

    # Add a title
    plt.title('Plot of I(q) vs. q')

    # Display the grid
    plt.grid(True)

    # Show the plot
    plt.savefig(f"C:\\pics\\{os.path.basename(filepath)}.png")




