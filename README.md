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
1. Download the [ncbi taxonomy owl file](http://www.obofoundry.org/ontology/ncbitaxon.html)
2. In side the organisms folder run the following script:
    python parse_ncbi.py ncbi\_owl\_file\_name
This will output the organisms into a file caled 'organisms.txt'. 
This script may take a few minutes. Some organisms are removed 
from the original taxonomy and saved in a file called 'bad-organims.txt'. 
It is important to not move the 'organisms.txt' file, because the 
database intilization portion is looking for the file in its
current location.


##### Initializing the database with data
TODO: Initialize testing information
1. To populate the database with testing data run the following 
management command:
    python manage.py populatetesting
2. To populate with actual data run
1. To populate the database with information run:
    python manage.py initializedatabase
If you do not want to initialize the organisms add --noorganisms 
to the end of the command. **Initializing the organisms will 
take awhile.** The first time I ran it, it took three days.
If you do not need to add all the organisms, either add 
organisms using the shell or run the adding organisms to add
some organisms, then hit ^C to stop the program.
