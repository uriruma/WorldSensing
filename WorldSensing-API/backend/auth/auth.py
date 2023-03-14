from database.db_controller import get_data_from_ddbb
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

security = HTTPBasic()

# Line to add if I want AUTH in an endpoint: current_user: str = Depends(get_current_user)

def get_user_by_username(username):
    """
    Returns the user with the given username from the database.

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

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Returns the authenticated user.

    Parameters:
        - credentials (HTTPBasicCredentials): The HTTP basic authentication credentials.

    Returns:
        - str: The username of the authenticated user.
    """
    user = get_user_by_username(credentials.username)
    if credentials.username != user["username"] or credentials.password != user["passwd"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect user or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


