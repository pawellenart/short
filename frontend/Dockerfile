# Use the specified Node.js version as a parent image
FROM node:22.3.0

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container
COPY . .

# Install any needed packages
RUN npm install

# Build the app
RUN npm run build

# Make port 8765 available to the world outside this container
EXPOSE 8765

# Set the environment variable to change the default port
ENV PORT=8765

# Run the app
CMD ["npm", "start"]
