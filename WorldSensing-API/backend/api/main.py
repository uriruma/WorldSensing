# main.py

import time
from fastapi import FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends
# from pydantic import BaseModel
# from fastapi.responses import JSONResponse
from database.db_controller import *

app = FastAPI()

security = HTTPBasic()

# conn()
# createDDBB()
# if conn() is not None:
#     createDDBB()
# Default storage 
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
        "username" : "admin",
        "passwd" : "admin"
    }
]

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = get_UserByUsername(credentials.username)
    if credentials.username != user["username"] or credentials.password != user["passwd"]:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect user or password",
            headers = {"WWW-Authenticate": "Basic"},
        )
    return credentials.username


# Global variable for not having repeated Id's
next_id = max(sortMap["id"] for sortMap in sortMaps_array) + 1 if sortMaps_array else 1

# Get SortMap and User auxiliar functions
def get_SortMapById(sortMap_id):
    for sortMap in sortMaps_array:
        if sortMap ["id"] == sortMap_id:
            return sortMap 

    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND, 
        detail = "SortMap not found"
        )  

def get_UserByUsername(username):
    for user in users_array:
        if user["username"] == username:
            return user
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = "User not found"
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
@app.get("/sortmaps")
async def get_sortMaps(current_user: str = Depends(get_current_user)) -> dict:
    if not sortMaps_array:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail = "SortMaps not found/empty"
        )
    return {"sortMaps": sortMaps_array}


# Get one SortMap based on Id
@app.get("/sortmaps/{sortMap_id}")
async def get_sortMap(sortMap_id: int) -> dict:
    sortMap = get_SortMapById(sortMap_id)
    if sortMap:
        return sortMap


# PUT/POST methods #

# POST request to insert SortMap into the array
@app.post("/sortmap")
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
@app.put("/sortmap/{sortMap_id}")
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


# POST request to sort a string using a sortMap, 
# in this function it is used sortmap for a more user-friendly url
@app.post("/order")
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
@app.delete("/sortmap/{sortMap_id}")
async def delete_sortMap(sortMap_id: int) -> dict:
    sortMap = get_SortMapById(sortMap_id)
    if sortMap:
        sortMaps_array.remove(sortMap)
        return {"message" : f"sortMap with id: {sortMap_id} deleted with exit!"}
    else:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
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
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail = "Input text must contain only digits"
            )
    mapping = {num: i for i, num in enumerate(sortMap)}
    return ''. join(sorted(text, key = lambda x: mapping[x]))


sortTextUsingSortMap("6780432159", "135543817")


def my_function():
  print("Hello from a function")

my_function()





















