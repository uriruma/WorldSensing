"""

File: main.py
Author: Oriol Romagosa
Date: 10 / 03 / 2023
Last Modified: 
Version: 3.11
Description: Basic API interface implementation with interactions on a Database and using Basic Auth

"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.main import app as api_router  # Import the API instance from api/main.py

app = FastAPI()

# Allow CORS for the React App
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

# Mount the API instance from api/main.py
app.mount("/api", api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host = "0.0.0.0", port = 8000, reload = True)
