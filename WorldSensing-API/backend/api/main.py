# main.py

import time
from fastapi import FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends
# from pydantic import BaseModel
# from fastapi.responses import JSONResponse
import mysql.connector

app = FastAPI()

security = HTTPBasic()

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = "admin"
    correct_password = "admin"
    if credentials.username != correct_username or credentials.password != correct_password:
        raise HTTPException(
            status_code = 401,
            detail = "Incorrect user or password",
            headers = {"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# Storage 
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

# sortMaps_array = []

# Global variable for not having repeated Id's
next_id = max(sortMap["id"] for sortMap in sortMaps_array) + 1 if sortMaps_array else 1

# Get SortMap from Array by the Id
def get_SortMapById(sortMap_id):
    for sortMap in sortMaps_array:
        if sortMap ["id"] == sortMap_id:
            return sortMap 

    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND, 
        detail = "SortMap not found"
        )  

# Line to add if I want AUTH in an endpoint:
# current_user: str = Depends(get_current_user)

######       Api Endpoints       ######

# Home
# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


# GET methods #

# Get all the sortMaps 
@app.get("/api/sortmaps")
async def get_sortMaps(current_user: str = Depends(get_current_user)) -> dict:
    if not sortMaps_array:
        raise HTTPException(
            status_code = 404, 
            detail = "SortMaps not found/empty"
        )
    return {"sortMaps": sortMaps_array}


# Get one SortMap based on Id
@app.get("/api/sortmaps/{sortMap_id}")
async def get_sortMap(sortMap_id: int) -> dict:
    sortMap = get_SortMapById(sortMap_id)
    if sortMap:
        return sortMap
    else:
        raise HTTPException( #TODO mirar aquesta excepcio ja que potser no cal al tenirla en la funcio get_SortMapById
            status_code = 404, 
            detail = "SortMap not found"
            )


# PUT/POST methods #

# POST request to insert SortMap into the array
@app.post("/api/sortmap")
async def create_sortMap(data: dict) -> dict:
    global next_id  # use the global variable to keep track of Ids
    value = data.get("value")
    if not value:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "SortMap value is required"
        )
    if not isStringNotRepeatedNumbers(value):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "SortMap value must be a sequence of unique digits"
        )
    sortMap = {"id": next_id, "value": value}
    sortMaps_array.append(sortMap)
    next_id += 1
    return sortMap


# PUT request to update SortMap value
@app.put("/api/sortmap/{sortMap_id}")
async def update_sortMap(sortMap_id: int, data: dict) -> dict:
    sortMap = get_SortMapById(sortMap_id)
    value = data.get("value")
    if not value:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "SortMap value is required"
        )
    if not isStringNotRepeatedNumbers(value):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "SortMap value must be a sequence of unique digits"
        )
    sortMap["value"] = value
    return sortMap


# POST request to sort a string using a sortMap
@app.post("/api/order")
async def sort_text(sortmap_id: int, request_data: dict) -> dict:
    sortmap = get_SortMapById(sortmap_id)
    if not sortmap:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "SortMap not found"
        )

    request_text = request_data.get("request")
    if not request_text:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Request text is required"
        )

    start_time = time.monotonic()
    sorted_text = sortTextUsingSortMap(sortmap["value"], request_text )
    end_time = time.monotonic()

    response = {
        "sortmap_id": sortmap_id,
        "response": sorted_text,
        "time": int((end_time - start_time) * 1000)
    }
    return response


# DELETE methods #

# Delete SortMap by Id
@app.delete("/api/sortmap/{sortMap_id}")
async def delete_sortMap(sortMap_id: int) -> dict:
    sortMap = get_SortMapById(sortMap_id)
    if sortMap:
        sortMaps_array.remove(sortMap)
        return {"message" : f"sortMap with id: {sortMap_id} deleted with exit!"}
    else:
        raise HTTPException(
            status_code = 404,
            detail = "SortMap not found"
        )


# Validation of non repeated numbers 
def isStringNotRepeatedNumbers(string: str) -> bool:
    # Check that the value contains only digits
    if not string.isdigit():
        return False
    # Check that the value contains unique digits
    return len(set(string)) == len(string)


# Sort the text
def sortTextUsingSortMap(sortMap, text):
    print("sorting...")
    if any(not x.isdigit() for x in text):
        raise HTTPException(
            status_code = 400, 
            detail = "Input text must contain only digits"
            )
    mapping = {num: i for i, num in enumerate(sortMap)}
    return ''. join(sorted(text, key = lambda x: mapping[x]))


sortTextUsingSortMap("6780432159", "135543817")


def my_function():
  print("Hello from a function")

my_function()




















######       DDBB Conection       ######

# Parameters
hostname = 'localhost'
username = 'root'
password = 'root'
database = 'python_test'

# try:
#    # Executing the SQL command
#    cursor.execute(sql)

#    # Commit your changes in the database
#    conn.commit()

# except:
#    # Rolling back in case of error
#    conn.rollback()

# # Closing the connection
# conn.close()

def conn():
    # Retrieve sensitive information from environment variables
    hostname = "localhost"
    username = "root"
    password = "root"
    database = "python_test"

    # Initialize the connection and cursor variables
    conn = None
    cursor = None

    try:
        # Try to connect to the database
        conn = mysql.connector.connect(
            host = hostname,
            user = username,
            password = password,
            
        )
        print('Connected to the server')

        # Create the database if it doesn't exist
        cursor = conn.cursor()
        sql = f"CREATE DATABASE IF NOT EXISTS {database};"
        cursor.execute(sql)
        print('Database created')

    except mysql.connector.Error as e:
        print('Error connecting to the database:')
        print(e.msg)
        print('Error code:', e.errno)
        
    finally:
        # Close the database connection and cursor
        if cursor is not None:
            cursor.close()
            print('Cursor closed')
        if conn is not None:
            conn.close()
            print('Database connection closed')


######       DDBB Operations       ######


conn()
