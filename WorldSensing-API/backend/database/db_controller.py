import mysql.connector
from fastapi import HTTPException, status
from database.__init__ import DB_HOSTNAME, DB_USERNAME, DB_PASSWORD, DB_NAME, TABLES
import logging

config = {
    'host': DB_HOSTNAME,
    'user': DB_USERNAME,
    'password': DB_PASSWORD
}

database = DB_NAME

tables = TABLES

logging.basicConfig(filename = 'app.log', level = logging.INFO)


# Connect to DDBB
def connect_to_database():
    try:
        conn = mysql.connector.connect(**config, database = database)
        logging.info('Connected to the MySQL server')
        return conn
    except mysql.connector.Error as e:
        logging.error('Error connecting to the MySQL server')
        logging.error(e.msg)
        logging.error('Error code:', e.errno)
        raise


# DDBB Creation with Tables
def create_database():
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Create the database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
        logging.info(f"The {database} database was created")

        # Switch to the specified database
        cursor.execute(f"USE {database}")
        # Delete the tables if they exist:
        delete_table("sortmaps")
        delete_table("users")
        # Create the tables if they don't exist
        for table in tables:
            table_name = table["name"]
            table_fields = table["fields"]
            table_pk = table.get("primary_key", None)

            fields_str = ', '.join(f'{field["name"]} {field["type"]}' for field in table_fields)

            create_table_sql = f'CREATE TABLE IF NOT EXISTS {table_name} ({fields_str}'
            if table_pk is not None:
                create_table_sql += f', PRIMARY KEY ({table_pk}))'
            else:
                create_table_sql += ')'

            cursor.execute(create_table_sql)

            logging.info(f"The {table_name} table was created")

    except mysql.connector.Error as e:
        logging.error(f"Failed to create the {database} database and tables")
        logging.error(e.msg)
        raise

    finally:
        cursor.close()
        conn.close()

# Insert a single row into a DDBB table
def insert_row(table_name, values):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        # Construct the SQL query to insert a row
        field_names = ', '.join(values.keys())
        values_sql = ', '.join(['%s'] * len(values))
        insert_sql = f"INSERT INTO {table_name} ({field_names}) VALUES ({values_sql})"
        
        # Get the values to insert
        values_to_insert = tuple(values.values())

        # Execute the query
        cursor.execute(insert_sql, values_to_insert)
        conn.commit()

        logging.info(f"Inserted row into {table_name} table")

    except mysql.connector.Error as e:
        logging.error(f"Failed to insert row into {table_name} table")
        logging.error(e.msg)
        raise

# DDBB Tables Deletion
def delete_table(table_name):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        # Construct the SQL query to delete the table
        delete_table_sql = f"DROP TABLE IF EXISTS {table_name}"

        # Execute the query
        cursor.execute(delete_table_sql)

        logging.info(f"The {table_name} table was deleted")

    except mysql.connector.Error as e:
        logging.error(f"Failed to delete the {table_name} table")
        logging.error(e.msg)
        raise

    finally:
        cursor.close()
        conn.close()

# DDBB Table Rows Deletion
def delete_table_rows(table_name):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        # Construct the SQL query to delete the table rows
        delete_rows_sql = f"DELETE FROM {table_name}"

        # Execute the query
        cursor.execute(delete_rows_sql)

        logging.info(f"All rows were deleted from the {table_name} table")

    except mysql.connector.Error as e:
        logging.error(f"Failed to delete rows from the {table_name} table")
        logging.error(e.msg)
        raise

    finally:
        cursor.close()
        conn.close()

# Update a row in a table
def update_row(table_name, set_values, id):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        # Construct the SQL query to update a row
        set_clause = ', '.join([f"{field}=%s" for field in set_values.keys()])
        update_sql = f"UPDATE {table_name} SET {set_clause} WHERE id = {id}"

        # Get the values to set from the dictionary
        values_to_set = tuple(set_values.values())

        # Execute the query
        cursor.execute(update_sql, values_to_set)
        conn.commit()

        logging.info(f"Updated row in {table_name} table")

    except mysql.connector.Error as e:
        logging.error(f"Failed to update row in {table_name} table")
        logging.error(e.msg)
        raise


def delete_row(table_name: str, row_id: int) -> bool:
    """ Delete a row with the specified id from the given table."""
    try:
        conn = connect_to_database()
        cur = conn.cursor()
        query = f"DELETE FROM {table_name} WHERE id = %s"
        cur.execute(query, (row_id,))
        conn.commit()
        return cur.rowcount > 0
    finally:
        conn.close()
# sortmaps_array = [{        "id": 1,        "value": "9876543210"    },    {        "id": 2,        "value": "6780432159"    }]

# users_array = [{        "username": "admin",        "passwd": "admin"    },    {        "username": "test",        "passwd": "test"    }]

def get_data_from_ddbb():
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        select_sortmaps_sql = "SELECT * FROM sortmaps"
        select_users_sql = "SELECT * FROM users;"
        cursor.execute(select_users_sql)
        users_result = cursor.fetchall()

        cursor.execute(select_sortmaps_sql)
        sortmaps_result = cursor.fetchall()

        cursor.close()
        connection.close()

        # process result data here
        users = []
        for row in users_result:
            user = {"username": row[0], "passwd": row[1]}
            users.append(user)

        sortmaps = []
        for row in sortmaps_result:
            sortmap = {"id": row[0], "value": row[1]}
            sortmaps.append(sortmap)

        return sortmaps, users

    except mysql.connector.Error as error:
        print(f"Failed to get data from database: {error}")
        return [], []

def manual_insert():
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        # Construct the SQL query to insert rows
        
        insert_sortmaps_sql = "INSERT INTO python_api.sortmaps VALUES (1, '9876543210'), (2, '6780432159');"
        insert_users_sql = "INSERT INTO python_api.users VALUES ('admin', 'admin'), ('test', 'test')"
        # Get the values to insert from the array

        # Execute the query
        cursor.execute(insert_sortmaps_sql)
        cursor.execute(insert_users_sql)
        conn.commit()


    except mysql.connector.Error as e:
        logging.error(f"Failed to insert rows")
        logging.error(e.msg)
        raise

    finally:
        cursor.close()
        conn.close()

        
# create_database()
# # conn = connect_to_database()
# manual_insert()
# sortmaps_array, users_array = get_data_from_ddbb()

# refresh_tables()
# conn.close()


