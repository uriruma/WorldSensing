# __init__.py

# import os
# import mysql.connector

# Get the values of the environment variables

# DB_HOSTNAME = os.getenv('MYSQL_HOST', 'localhost')
# #  = os.getenv('DB_PORT', '3306')
# DB_NAME = os.getenv('MYSQL_DATABASE', 'python_test')
# DB_USERNAME  = os.getenv('MYSQL_USER', 'root')
# DB_PASSWORD = os.getenv('MYSQL_PASSWORD', 'root')
# # Database parameters

DB_HOSTNAME = 'localhost'
DB_USERNAME = 'root'
DB_PASSWORD = 'root'
DB_NAME = 'python_api'

TABLES = [
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