# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Create the directory for the database file and set permissions (if using SQLite)
RUN mkdir -p /usr/src/app/db && chmod -R 777 /usr/src/app/db

# Install any needed packages specified in requirements.txt
RUN apt-get update && apt-get install -y gcc python3-dev musl-dev

# Install base dependencies
RUN pip install --no-cache-dir fastapi[all] uvicorn sqlalchemy pydantic bcrypt requests beautifulsoup4


# Install database-specific dependencies
ARG DB_TYPE=sqlite

RUN if [ "$DB_TYPE" = "postgres" ] ; then \
    pip install --no-cache-dir psycopg2-binary ; \
    elif [ "$DB_TYPE" = "mysql" ] ; then \
    pip install --no-cache-dir pymysql ; \
    elif [ "$DB_TYPE" = "mariadb" ] ; then \
    apt-get install -y mariadb-client libmariadb-dev && \
    pip install --no-cache-dir mariadb ; \
    fi

# Set the PYTHONPATH
ENV PYTHONPATH=/usr/src/app

# Run the initialization script
RUN python app/initialize.py

# Make port 7654 available to the world outside this container
EXPOSE 7654

# Run app.py when the container launches
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7654"]