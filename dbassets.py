from psycopg2 import extras

def get_conn():
    return  psycopg2.connect(
        host="localhost",
        database="spgen",
        user="postgres",
        password="Dictionary108$"
    )

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
        query = sql.SQL("""SELECT * FROM {table} WHERE {column} = %s""").format(table=sql.Identifier(table_name), column=sql.Identifier(column_name))
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

def update_field_by_unique_field(table, target_field, where_field_name, where_field_value ,new_value):
    """
    Update specified field of the table.

    Args:
        table: Name of the table (string).
        field: Name of the field (string).
        value: Double value to insert.
    """
    # Create a cursor object to interact with the database
    try:
        # Connect to the PostgreSQL database
        conn = get_conn()
        cursor = conn.cursor()
        # Build the SQL query
        query = f"UPDATE {table} SET {target_field} = %s WHERE {where_field_name}={where_field_value}"
        # Execute the query
        cursor.execute(query,(new_value,))
        # save changes
        conn.commit()
    except Exception as err:
        print(f"Error occurred: {err}")
        # Rollback the transaction in case of an error
        conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            close_conn(conn)

def get_fields_data(conn, table_name, field_names):
    # Create a cursor object to interact with the database
    cursor = conn.cursor()
    # SQL query to select the specified fields from the specified table
    fields_str = ', '.join(field_names)
    query = f"SELECT {fields_str} FROM {table_name} WHERE real_nc=-1;"
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
    try:
        # Connect to the PostgreSQL database
        conn = get_conn()
        cursor = conn.cursor()

        # Build the query dynamically using the table and dictionary keys
        columns = data_dict.keys()
        values = tuple(data_dict.values())

        # Create the SQL query for insertion
        query = sql.SQL("INSERT INTO {} ({}) VALUES ({}) RETURNING id").format(
            sql.Identifier(table_name),  # Table name
            sql.SQL(', ').join(map(sql.Identifier, columns)),  # Column names
            sql.SQL(', ').join(sql.Placeholder() * len(values))  # Placeholder for values
        )

        # Execute the insert query with the data
        cursor.execute(query, values)
        result = cursor.fetchone()
        inserted_id = result[0] if result else None
        # Commit the transaction
        conn.commit()
        print(inserted_id)
        print(f"Data inserted successfully into {table_name}.")
        return inserted_id

    except Exception as e:
        print(f"Error occurred: {e}")
        # Rollback the transaction in case of an error
        conn.rollback()

    finally:
        # Close cursor and connection
        if cursor:
            cursor.close()
        close_conn(conn)


def fetch_all_as_dict(table_name):
    """
    Fetch all rows from a table and return as a list of dictionaries.

    :param connection: psycopg2 connection object
    :param table_name: str, the name of the table you want to query
    :return: List of dictionaries, where each dictionary represents a row
    """
    try:
        connection = get_conn()
        # Create a cursor with dictionary-based results
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        # Query to fetch all rows from the specified table
        query = f"SELECT * FROM {table_name};"

        # Execute the query
        cursor.execute(query)

        # Fetch all results as a list of dictionaries
        return cursor.fetchall()

    except Exception as e:
        print(f"Error fetching data: {e}")
        return []
    finally:

        # Close the cursor
        cursor.close()
        # Close cursor and connection
        connection.close()


def get_records_by_where(table_name, where_clauses):
    """
    Fetch records from the table based on dynamic where conditions.

    :param conn: Database connection object.
    :param table_name: Name of the table to query.
    :param where_clauses: Dictionary of column: value pairs for the WHERE clause.
    :return: List of dictionaries, each representing a record.
    """
    # Construct the WHERE clause dynamically
    where_conditions = []
    values = []

    for column, value in where_clauses.items():
        where_conditions.append(sql.SQL("{} = %s").format(sql.Identifier(column)))
        values.append(value)

    where_clause = sql.SQL(" AND ").join(where_conditions)

    # Create the final query
    query = sql.SQL("SELECT * FROM {} WHERE {}").format(
        sql.Identifier(table_name),
        where_clause
    )

    try:
        conn = get_conn()

        with conn.cursor() as cursor:
            cursor.execute(query, values)
            columns = [desc[0] for desc in cursor.description]  # Get column names
            rows = cursor.fetchall()
            # Convert rows to list of dictionaries
            result = [dict(zip(columns, row)) for row in rows]
            return result
    except Exception as e:
        print(f"Error executing query: {e}")
        return []

    finally:
        conn.close()


def delete_record_by_id(table_name, record_id):
    """
    Deletes a record from the database table based on the provided record ID.

    :param conn: Database connection object.
    :param table_name: Name of the table from which the record should be deleted.
    :param record_id: The ID of the record to be deleted.
    :return: True if the record was deleted, False if there was an error or no record was found.
    """
    try:
        # Build the query to delete the record
        query = sql.SQL("DELETE FROM {} WHERE id = %s").format(sql.Identifier(table_name))
        conn = get_conn()
        # Execute the query
        with conn.cursor() as cursor:
            cursor.execute(query, (record_id,))

            # Commit the transaction
            conn.commit()

            # Check if any record was deleted
            if cursor.rowcount > 0:
                print(f"Record with id {record_id} deleted successfully.")
                return True
            else:
                print(f"No record found with id {record_id}.")
                return False
    except Exception as e:
        print(f"Error deleting record: {e}")
        return False
    finally:
        close_conn(conn)


import psycopg2
from psycopg2 import sql


def insert_record_and_get_id(table_name, data_dict):
    """
    Insert a record into a specified table using the provided dictionary of column-value pairs,
    and return the auto-incremented ID of the inserted row.

    :param table_name: Name of the table to insert data into.
    :param data_dict: Dictionary containing column names as keys and the values to insert.
    :return: ID of the inserted record, or None if insertion fails.
    """
    try:
        conn=get_conn()
        cursor = conn.cursor()

        # Prepare the columns and values from the data_dict
        columns = data_dict.keys()
        values = tuple(data_dict.values())

        # Dynamically construct the SQL query with placeholders
        query = sql.SQL("INSERT INTO {} ({}) VALUES ({}) RETURNING id").format(
            sql.Identifier(table_name),  # Table name
            sql.SQL(', ').join(map(sql.Identifier, columns)),  # Column names
            sql.SQL(', ').join(sql.Placeholder() * len(values))  # Placeholder for values
        )

        # Execute the insert query
        cursor.execute(query, values)

        # Fetch the inserted record's ID
        inserted_id = cursor.fetchone()[0]

        # Commit the transaction
        conn.commit()

        print(f"Record inserted successfully with ID: {inserted_id}")
        return inserted_id

    except Exception as e:
        print(f"Error occurred: {e}")
        # Rollback the transaction in case of an error
        conn.rollback()
        return None

    finally:
        # Close cursor and connection
        cursor.close()
        close_conn(conn)