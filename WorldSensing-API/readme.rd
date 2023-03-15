Welcome to the API, here you will find all the needed details.

CONFIGURATION: 

 - Backend:
    If you want to modify any of the DDBB connection parameters, change the 
    variables of the file: /WorldSensing-API/backend/__init__.py 

INSTRUCTIONS:


Once you have opened the WorldSensing-API folder, follow the next steps: (you will need to have installed docker)

    *****- To build the backend Docker image, navigate to the backend directory and run:

        docker build -t backend .***** (*It does not works as I could not implement the installation
        in the Dockerfile of a mysql server)

    - To start the backend first of all start a MYSQL server for example with XAMPP or MAMP.

    Then, once inside the folder /WorldSensing-API/backend run the command: "python main.py".
    Now the Api will be running.


    - To build the frontend Docker image, navigate to the frontend firectory and run:

        docker build -t frontend  .

Now you must run the Docker images once created:

    *****- Run backend image

        docker run -p 8000:8000 backend***** (*It does not works as I could not implement the installation
        in the Dockerfile of a mysql server)

    - Run frontend image

        docker run -p 3000:3000 frontend


GENERAL INFO:


You can see a folder structure like this:

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
│── main.py
│── app.log
│── Dockerfile
└── requirements.txt


frontend/
│
├── my-api/
│   ├── node_modules
│   ├── public
│   └── src
│
│── Dockerfile
└── requirements.txt


Backend:

- api folder: This folder contains the main files for your API. The main.py file is where you define your API routes and the router.py file is where you define your API router. 

- The __init__.py file is an empty file that tells Python that this folder is a Python package.

- database folder: This folder contains the file that defines the database controller (db_controller.py). 

- auth folder: This folder contains the file that defines the authentication functions (auth.py). 

- main.py: This is the main entry point of your application. It is where you start your API server and import the API router.

- Dockerfile: file ready to build and run using Docker (without mysql server)

- requirements.txt: list of dependencies used in fastApi


Frontend:

- my-api folder: This is the react app with its modules, the main App(src) and the entrance point (public)

- Dockerfile: file ready to build and run using Docker