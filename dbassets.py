import psycopg2
from psycopg2 import sql


def get_field_data(conn, table_name, field_name):
    # Establish a connection to the database

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # SQL query to select the specified field from the specified table
    query = f"SELECT {field_name} FROM {table_name};"

    # Execute the query
    cursor.execute(query)

    # Fetch all the results
    results = cursor.fetchall()
    # Close the cursor and connection
    cursor.close()
    conn.close()
    return results
##pg_dump -U postgres -h localhost -p 5432 -F p -f backup.sql spgen


def get_conn():
    return  psycopg2.connect(
        host="localhost",
        database="spgen",
        user="postgres",
        password="Dictionary108$"
    )


def execute_query(connection, table_name, column_name, record_id):
    """
    Execute a query to fetch a single record from a table with a specified ID and return it as a dictionary.

    :param connection: Database connection object.
    :param table_name: Name of the table to query.
    :param column_name: Name of the column to filter by.
    :param record_id: ID value to filter data.
    :return: Dictionary containing the row fetched (keys are column names).
    """
    try:
        cursor = connection.cursor()
        query = sql.SQL("""
            SELECT * FROM {table} WHERE {column} = %s
        """).format(
            table=sql.Identifier(table_name),
            column=sql.Identifier(column_name)
        )
        cursor.execute(query, (record_id,))

        # Fetch one row and map it to a dictionary
        row = cursor.fetchone()

        if row:
            # Get column names from cursor description
            columns = [desc[0] for desc in cursor.description]
            # Convert the row to a dictionary with column names as keys
            result = dict(zip(columns, row))
            return result
        else:
            # Return None if no record found
            return None

    except Exception as e:
        print(f"Error executing query: {e}")
        return None

    finally:
        if cursor:
            cursor.close()


def close_conn(connection):
    """
    Close the database connection.

    :param connection: Database connection object.
    """
    try:
        if connection:
            connection.close()
    except Exception as e:
        print(f"Error closing connection: {e}")




def get_data_by_id(table_name, column_name, record_id):
    """
    Fetch all data from a PostgreSQL table with a specified ID using separate functions.

    :param table_name: Name of the table to query.
    :param column_name: Name of the column to filter by.
    :param record_id: ID value to filter data.
    :return: List of tuples containing the rows fetched.
    """
    connection = get_conn()
    if not connection:
        return None

    try:
        rows = execute_query(connection, table_name, column_name, record_id)
        return rows
    finally:
        close_conn(connection)


def get_data_by_id(table_name, column_name, record_id):
    """
    Fetch all data from a PostgreSQL table with a specified ID using separate functions.

    :param table_name: Name of the table to query.
    :param column_name: Name of the column to filter by.
    :param record_id: ID value to filter data.
    :return: List of tuples containing the rows fetched.
    """
    connection = get_conn()
    if not connection:
        return None

    try:
        rows = execute_query(connection, table_name, column_name, record_id)
        return rows
    finally:
        close_conn(connection)




def update_field_double(conn, table, field,id:int ,value):
    """
    Inserts a double value into the specified field of the table.

    Args:
        conn: psycopg2 connection object.
        table: Name of the table (string).
        field: Name of the field (string).
        value: Double value to insert.
    """
    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Build the SQL query
    query = f"UPDATE {table} SET {field} = %s WHERE id={id}"

    cur=conn.cursor()
        # Execute the query
    cur.execute(query,(value,))


    print(f"Inserted value {value} into field {field} of table {table}.")

    # Close the cursor
    cur.close()

def get_fields_data(conn, table_name, field_names):
    # Establish a connection to the database


    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # SQL query to select the specified fields from the specified table
    fields_str = ', '.join(field_names)
    #query = f"SELECT {fields_str} FROM {table_name};"
    query = f"SELECT {fields_str} FROM {table_name} WHERE path like '%_excess_%';"
    #query="select * from sp_gen where path like '%_excess_%'"

    # Execute the query
    cursor.execute(query)

    # Fetch all the results
    rows = cursor.fetchall()

    # Prepare a list of dictionaries, each representing one row
    results = []
    for row in rows:
        row_dict = {field: row[i] for i, field in enumerate(field_names)}
        results.append(row_dict)

    # Close the cursor and connection
    cursor.close()

    return results


def insert_data(table_name, data_dict):
    """
    Insert data into a specified table.

    :param table_name: Name of the table to insert data into.
    :param data_dict: Dictionary containing column names as keys and the values to insert.
    """
    # Database connection parameters
    db_params = {
        'dbname': 'your_database_name',  # replace with your database name
        'user': 'your_user',  # replace with your database username
        'password': 'your_password',  # replace with your database password
        'host': 'localhost',  # replace with your host (or use 'localhost')
        'port': 5432  # replace with your PostgreSQL port, default is 5432
    }

    try:
        # Connect to the PostgreSQL database
        conn = get_conn()
        cursor = conn.cursor()

        # Build the query dynamically using the table and dictionary keys
        columns = data_dict.keys()
        values = tuple(data_dict.values())

        # Create the SQL query for insertion
        query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(table_name),  # Table name
            sql.SQL(', ').join(map(sql.Identifier, columns)),  # Column names
            sql.SQL(', ').join(sql.Placeholder() * len(values))  # Placeholder for values
        )

        # Execute the insert query with the data
        cursor.execute(query, values)

        # Commit the transaction
        conn.commit()

        print(f"Data inserted successfully into {table_name}.")

    except Exception as e:
        print(f"Error occurred: {e}")
        # Rollback the transaction in case of an error
        conn.rollback()

    finally:
        # Close cursor and connection
        cursor.close()
        conn.close()

