"""
File: main.py
Author: Oriol Romagosa
Date: 10 / 03 / 2023
Last Modified: 
Version: 3.11
Description: Basic API interface implementation with interactions on a Database and using Basic Auth

"""

from fastapi import FastAPI
from api.main import app as api_router  # Import the API instance from api/main.py

app = FastAPI()

# Mount the API instance from api/main.py
app.mount("/api", api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host = "0.0.0.0", port = 8000, reload = True)
