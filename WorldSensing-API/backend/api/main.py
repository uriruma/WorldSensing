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

# Default storage 
# sortmaps_array = [
#     {
#         "id": 1,
#         "value": "9876543210"
#     },
#     {
#         "id": 2,
#         "value": "6780432159"
#     }
# ]

# users_array = [
#     {
#         "username" : "admin",
#         "passwd" : "admin"
#     }
# ]

# print (sortmaps_array)
# print(users_array)

# DDBB Creation
create_database()
# conn = connect_to_database()
manual_insert()
sortmaps_array, users_array = get_data_from_ddbb()
# refresh_tables()
# insert_rows("sortmaps", sortmaps_array)
# insert_rows("users", users_array)


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
next_id = max(sortmap["id"] for sortmap in sortmaps_array) + 1 if sortmaps_array else 1

# Get sortmap and User auxiliar functions
def get_sortmapById(sortmap_id):
    for sortmap in sortmaps_array:
        if sortmap ["id"] == sortmap_id:
            return sortmap 

    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND, 
        detail = "sortmap not found"
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

# Get all the sortmaps 
@app.get("/sortmaps")
async def get_sortmaps(current_user: str = Depends(get_current_user)) -> dict:
    if not sortmaps_array:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail = "sortmaps not found/empty"
        )
    # refresh_tables(sortmaps_array, users_array)
    # delete_table_rows("sortmaps")
    # delete_table_rows("users")
    return {"sortmaps": sortmaps_array}

# Get one sortmap based on Id
@app.get("/sortmaps/{sortmap_id}")
async def get_sortmap(sortmap_id: int) -> dict:
    sortmap = get_sortmapById(sortmap_id)
    if sortmap:
        return sortmap


# PUT/POST methods #

# POST request to create a new sortmap 
@app.post("/sortmap")
async def create_sortmap(data: dict) -> dict:
    global next_id  # use the global variable to keep track of Ids
    value = data.get("value")
    if not value:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "sortmap value is required"
        )
    if not isStringNotRepeatedNumbers(value):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "sortmap value must be a sequence of unique digits"
        )
    sortmap = {"id": next_id, "value": value}
    # sortmaps_array.append(sortmap)
    next_id += 1
    insert_row("sortmaps", sortmap)
    return sortmap


# PUT request to update sortmap value
@app.put("/sortmap/{sortmap_id}")
async def update_sortmap(sortmap_id: int, data: dict) -> dict:
    sortmap = get_sortmapById(sortmap_id)
    value = data.get("value")
    if not value:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "sortmap value is required"
        )
    if not isStringNotRepeatedNumbers(value):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "sortmap value must be a sequence of unique digits"
        )
    sortmap["value"] = value
    sortmap_id = sortmap["id"]
    update_row("sortmaps", data, sortmap_id)
    # refresh_tables()
    return sortmap


# POST request to sort a string using a sortmap, 
# in this function it is used sortmap for a more user-friendly url
@app.post("/order")
async def sort_text(sortmap_id: int, request_data: dict) -> dict:
    sortmap = get_sortmapById(sortmap_id)
    if not sortmap:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "sortmap not found"
        )

    request_text = request_data.get("request")
    if not request_text:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Request text is required"
        )

    start_time = time.monotonic()
    sorted_text = sortTextUsingsortmap(sortmap["value"], request_text )
    end_time = time.monotonic()

    response = {
        "sortmap_id": sortmap_id,
        "response": sorted_text,
        "time": int((end_time - start_time) * 1000)
    }
    return response


# DELETE methods #

# Delete sortmap by Id
@app.delete("/sortmap/{sortmap_id}")
async def delete_sortmap(sortmap_id: int) -> dict:
    if delete_row("sortmaps", sortmap_id):
        return {"message": f"sortmap with id: {sortmap_id} deleted with exit!"}
    else:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "sortmap not found",
        )


# Validation of non repeated numbers 
def isStringNotRepeatedNumbers(string: str) -> bool:
    # Check that the value contains only digits
    if not string.isdigit():
        return False
    # Check that the value contains unique digits
    return len(set(string)) == len(string)


# Sort the text
def sortTextUsingsortmap(sortmap, text):
    print("sorting...")
    if any(not x.isdigit() for x in text):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail = "Input text must contain only digits"
            )
    mapping = {num: i for i, num in enumerate(sortmap)}
    return ''. join(sorted(text, key = lambda x: mapping[x]))


sortTextUsingsortmap("6780432159", "135543817")

def my_function():
  print("Hello from a function")

my_function()