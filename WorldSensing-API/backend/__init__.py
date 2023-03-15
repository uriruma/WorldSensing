# __init__.py

# Database parameters

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