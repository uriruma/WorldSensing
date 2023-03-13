Welcome to the API, here you will find all the needed details.

You will find a folder structure like this:

backend/
│
├── api/
│   ├── __init__.py
│   ├── main.py
│   └── router.py
│
├── database/
│   ├── __init__.py
│   └── db_controller.py
│
├── auth/
│   ├── __init__.py
│   └── auth.py
│
└── main.py


api folder: This folder contains the main files for your API. The main.py file is where you define your API routes and the router.py file is where you define your API router. 

The __init__.py file is an empty file that tells Python that this folder is a Python package.

database folder: This folder contains the file that defines the database controller (db_controller.py). 

auth folder: This folder contains the file that defines the authentication functions (auth.py). 

main.py: This is the main entry point of your application. It is where you start your API server and import the API router.


Instructions:

To run the app you should first type pithon main.py in the folder of backend to initiate the API server.
