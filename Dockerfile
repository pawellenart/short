# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Create sqlite database with correct permissions
RUN touch short.db && chmod 777 short.db

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the initialization script
RUN python app/initialize.py

# Make port 7654 available to the world outside this container
EXPOSE 7654

# Run app.py when the container launches
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7654"]