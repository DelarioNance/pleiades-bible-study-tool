#!/bin/bash

sudo apt update # Update package lists to ensure we have the latest information on available packages and their versions.
sudo apt install postgresql postgresql-contrib # Install PostgreSQL and additional utilities that come with it.
sudo service postgresql start # Start the PostgreSQL service so that we can interact with the database server.
sudo -u postgres createuser --superuser delar # Create a new PostgreSQL user named 'delar' with superuser privileges.
createdb pleiades # Create a new PostgreSQL database named 'pleiades' that we will use for our application.
sudo -u postgres psql -c "\du" # List all PostgreSQL users to verify that the 'delar' user was created successfully.
sudo -u postgres psql # Connect to the PostgreSQL server using the 'postgres' user to perform further database operations if needed.
ALTER USER delar WITH PASSWORD '<password>'; # Set a password for the 'delar' user