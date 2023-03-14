# main.py

import time
from fastapi import FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends
from database.db_controller import *

app = FastAPI()

security = HTTPBasic()

# DDBB Creation
create_database()

# This is amanual insert to have some values by efault
manual_insert()
sortmaps_array, users_array = get_data_from_ddbb() # reload the data in the arrays

print (sortmaps_array)
print(users_array)

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

def get_sortmapById(sortmap_id):
    """
    Returns the sortmap with the given ID.

    Parameters:
        - sortmap_id (int): The ID of the sortmap to get.

    Returns:
        - dict: A dictionary representing the retrieved sortmap.
    """
    sortmaps_array, users_array = get_data_from_ddbb() # reload data in the arrays
    for sortmap in sortmaps_array:
        if sortmap["id"] == sortmap_id:
            return sortmap 

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="sortmap not found"
    )

def get_UserByUsername(username):
    """
    Returns the user with the given username.

    Parameters:
        - username (str): The username of the user to get.

    Returns:
        dict: A dictionary representing the retrieved user.
    """
    sortmaps_array, users_array = get_data_from_ddbb() # reload data in the arrays
    for user in users_array:
        if user["username"] == username:
            return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
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
    """
    Gets all the sortmaps stored in the database.
    
    Returns:
        - dict: A dictionary containing the sortmaps data
    """
    sortmaps_array, users_array = get_data_from_ddbb() # reload data in the arrays
    if not sortmaps_array:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail = "sortmaps not found/empty"
        )
    return {"sortmaps": sortmaps_array}





# Get one sortmap based on Id
@app.get("/sortmaps/{sortmap_id}")
async def get_sortmap(sortmap_id: int) -> dict:
    sortmap = get_sortmapById(sortmap_id)
    if sortmap:
        return sortmap


# PUT/POST methods #

async def create_sortmap(data: dict) -> dict:
    """
    Creates a new sortmap with a unique ID and a specified value.
    
    Parameters:
        - data (dict): A dictionary containing the vale of the new sortmap.
    
    Returns:
        - dict: A dictionary representing the new sortmap, containing an ID and value.
    """
    global next_id  # use the global variable to keep track of Ids

    #Get the value of the request and if not it raises a HTTPEception depending of the needs
    value = data.get("value")
    if not value:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "sortmap value is required"
        )
    if not has_no_repeated_digits(value):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "sortmap value must be a sequence of unique digits"
        )
    
    # Build the new sortmap and insert it into the databasse
    sortmap = {"id": next_id, "value": value}
    next_id += 1
    insert_row("sortmaps", sortmap)
    return sortmap



@app.put("/sortmap/{sortmap_id}")
async def update_sortmap(sortmap_id: int, data: dict) -> dict:
    """
    Updates the value of a sortmap with the given id.
    
    Parameters:
        - sortmap_id (int): The id of the sortmap to be updated.
        - data (dict): A dictionary containing the new value of the sortmap. The dictionary should have a single key "value" with a string value containing the new sortmap value.
    
    Returns:
        - dict: A dictionary containing the updated sortmap. The dictionary will have the keys "id" and "value".
    """
    # Gets the sortmap object and the string from the body request, if not raise an HTTPException 400
    sortmap = get_sortmapById(sortmap_id)
    value = data.get("value")
    if not value:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "sortmap value is required"
        )
    if not has_no_repeated_digits(value):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "sortmap value must be a sequence of unique digits"
        )
    # Sets the new value to the sortmap and it updete the database
    sortmap["value"] = value
    sortmap_id = sortmap["id"]
    update_row("sortmaps", data, sortmap_id)
    return sortmap



@app.post("/order")
async def sort_text(sortmap_id: int, request_data: dict) -> dict:
    """
    Sorts a string of digits according to the order of digits in a sortmap, using a POST request.
    
    Parameters:
        - sortmap_id (int): The ID of the sortmap to be used for sorting.
        - request_data (dict): A dictionary containing the request data, with the following keys:
            - value (str): A string of digits to be sorted.
    
    Returns:
        - dict: A dictionary containing the response data, with the following keys:
            - sortmap_id (int): The ID of the sortmap used for sorting.
            - response (str): The sorted string of digits.
            - time (int): The time taken to sort the string
    """
    # Get a sortmap object with a given ID, if not raise an HTTPException 404
    sortmap = get_sortmapById(sortmap_id)
    if not sortmap:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "sortmap not found"
        )
    # Get the string string requested from the body, if not raise an HTTPException 400
    request_text = request_data.get("value")
    if not request_text:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Request text is required"
        )
    # 
    start_time = time.monotonic()
    sorted_text = sort_text_using_sortmap(sortmap["value"], request_text )
    end_time = time.monotonic()
    # Create the response it is returned
    response = {
    "sortmap_id": sortmap_id,
    "response": sorted_text,
    "time": ((end_time - start_time) * 1000)
    }
    return response



# DELETE methods #

@app.delete("/sortmap/{sortmap_id}")
async def delete_sortmap(sortmap_id: int) -> dict:
    """
    Deletes a sortmap with the given ID from the database.

    Parameters:
        - sortmap_id (int): The ID of the sortmap to be deleted.

    Returns:
        - dict: A dictionary containing a message indicating whether the deletion was successful.
    """
    # Check if the sortmap exists in the database and delete it if it does
    if delete_row("sortmaps", sortmap_id):
        return {"message": f"sortmap with id: {sortmap_id} deleted successfully"}
    
    # If the sortmap doesn't exist, raise an HTTPException 404
    else:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"No sortmap with id: {sortmap_id} found ",
        )



def has_no_repeated_digits(input_string: str) -> bool:
    """
    Checks if a given string contains only unique digits.
    
    Parameters:
    input_string (str): A string containing digits to be checked.
    
    Returns:
    bool: True if the input string contains only unique digits, False otherwise.
    """
    # Check that the input is not empty and contains only digits
    if not input_string or not input_string.isdigit():
        return False
    
    # Check that the value contains unique digits
    return len(set(input_string)) == len(input_string)

def sort_text_using_sortmap(sortmap, text):
    """
    Sorts a string of digits according to the order of digits in a sortmap.
    
    Parameters:
        - sortmap (str): A string of digits specifying the desired sort order.
        - text (str): A string of digits to be sorted.
    
    Returns:
        - str: The sorted string of digits.
    
    Raises:
        - ValueError: If sortmap is empty or contains non-digit characters.
        - ValueError: If text contains non-digit characters.
    """
    # Check that sortmap is not empty and contains only digits
    if not sortmap or any(not x.isdigit() for x in sortmap):
        raise ValueError("sortmap must contain at least one digit and no non-digit characters")
    
    # Check that text contains only digits
    if any(not x.isdigit() for x in text):
        raise ValueError("text must contain only digits")
    
    # Create a dictionary that maps each digit in sortmap to its position
    mapping = {num: i for i, num in enumerate(sortmap)}
    
    # Sort the digits in text based on their position in the mapping dictionary
    sorted_text = ''.join(sorted(text, key = lambda x: mapping.get(x, len(sortmap))))
    
    return sorted_text

sort_text_using_sortmap("6780432159", "135543817")

def my_function():
  print("Hello from a function")

my_function()