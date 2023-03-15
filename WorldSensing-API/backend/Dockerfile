
# Use an official Python runtime as a parent image
FROM python:3.11.2-bullseye

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port that the FastAPI application will run on
EXPOSE 8000

# Start the FastAPI application, probably will change for [python main.py]
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 
CMD ["python", "main.py"]