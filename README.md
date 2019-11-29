# CBE Image Database
## About

## Setup
##### Creating the database
The database is running using Postgresql.
1. Install postgresql
2. Start postgresql server [Docs](https://www.postgresql.org/docs/8.1/postmaster-start.html)
    pg_ctl -D /usr/local/var/postgres start (for mac)
3. Start psql shell
    psql postgres
4. Build database and users
   CREATE USER user_name WITH PASSWORD 'password';
   CREATE DATABASE database_name OWNER user_name;


##### Setting up Django

1. Clone the repository
2. Create the conda envrionment:
    conda env create environment.yml
3. Make a copy of the cbeImageDB/.env.samle named .env to store your local environment variables
   
##### Getting the organisms


##### Initializing the database with data
