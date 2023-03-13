import logging
import mysql.connector
from database.__init__ import DB_HOSTNAME, DB_USERNAME, DB_PASSWORD, DB_NAME
import logging

config = {
    'host': DB_HOSTNAME,
    'user': DB_USERNAME,
    'password': DB_PASSWORD
}

database = DB_NAME

tables = [
    {
        'name': 'users',
            'fields': [
                {'name': 'username', 'type': 'VARCHAR(255)'},
                {'name': 'passwd', 'type': 'VARCHAR(255)'},
            ],
            
    },
    {
        'name': 'sortMaps',
            'fields': [
                {'name': 'id', 'type': 'INT'},
                {'name': 'value', 'type': 'VARCHAR(255)'}
            ],
            'primary_key': 'id',
    }   
]

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

# Insert values from the array into a DDBB
def insert_rows(table_name, values):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        # Construct the SQL query to insert rows
        field_names = ', '.join(values[0].keys())
        values_sql = ', '.join(['%s'] * len(values))
        insert_sql = f"INSERT INTO {table_name} ({field_names}) VALUES ({values_sql})"
        
        # Get the values to insert from the array
        values_to_insert = [tuple(val.values()) for val in values]

        # Execute the query
        cursor.executemany(insert_sql, values_to_insert)
        conn.commit()

        logging.info(f"Inserted {len(values_to_insert)} rows into {table_name} table")

    except mysql.connector.Error as e:
        logging.error(f"Failed to insert rows into {table_name} table")
        logging.error(e.msg)
        raise

    finally:
        cursor.close()
        conn.close()

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

create_database()
conn = connect_to_database()

sortMaps_array = [
    {
        "id": 1,
        "value": "9876543210"
    },
    {
        "id": 2,
        "value": "6780432159"
    }
]

users_array = [
    {
        "username": 1,
        "passwd": "9876543210"
    },
    {
        "username": 2,
        "passwd": "6780432159"
    }
]

def refresh_tables():
    delete_table_rows("sortmaps")
    delete_table_rows("users")
    insert_rows("sortmaps", sortMaps_array)
    insert_rows("users", users_array)
    logging.info("Tables data refreshed")

# insert_row("sortmaps", array)

# do something with the connection...
conn.close()


