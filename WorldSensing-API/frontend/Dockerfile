# FRONTEND

# Use an official Node.js runtime as a parent image
FROM node:16.14.0-alpine

# Set the working directory to /app
WORKDIR /app

# Copy the package.json and package-lock.json files into the container
COPY package*.json ./

# Install any needed packages specified in package.json
RUN npm install

# Copy the rest of the application code into the container
COPY . .

# Build the React application for production
RUN npm run build

# Expose the port that the React application will run on
EXPOSE 3000

# Start the React application
CMD ["npm", "run", "start"]

# Success! Created my-api at C:\Users\uriru\OneDrive\Escritorio\worldSensing\WorldSensing-API\frontend\my-api
# Inside that directory, you can run several commands:

#   npm start
#     Starts the development server.

#   npm run build
#     Bundles the app into static files for production.

#   npm test
#     Starts the test runner.

#   npm run eject
#     Removes this tool and copies build dependencies, configuration files
#     and scripts into the app directory. If you do this, you can’t go back!

# We suggest that you begin by typing:

#   cd my-api
#   npm start

# Happy hacking!