# CBE Image Database
<!---
your comment goes here
and here
{% assign variableName = "text etc." %}
{{ nameOfVariableToCapture }}  that prints the content of the variable

-->

## About

### Docker
**TODO:** Pulls from dockerhub with code in directory blah

## Setup: Docker (Databases only)


## Setup: Docker (Web + databases)


## Setup Heroku
### Creating the Heroku app
**TODO**

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
### Making Updates




## Setup Old Stuff
_all commands are run from cbe-image-db/cbeImageDB_
### Setting Up the CBE Machine
1. Clone the repository
```
git clone https://github.com/biofilmDB/cbe-image-db.git
```

2. Create the .env file from the sample files
3. Create the directory(s) to store the database and image files
4. Copy over the initialization files
```
scp -r init_files braid@cbeimagedb.msu.montana.edu:/home/braid/cbe-image-db
```

5. Create the organisms file (must be done on local machine because docker
can't make it)
```
python cbeImageDB/organisms/parse_ncbi.py /path/to/ncbitaxon.owl
```

6. Copy organisms.csv to server machine
```
scp organisms.csv braid@cbeimagedb.msu.montana.edu/home/braid/cbe-image-db/cbeImageDB/organisms
```

7. Create and run the docker containers from cbeImageDB project folder
```
docker-compose -f ../docker-compose.yml -f ../docker-compose-web.yml up
```

8. Initiate the database
```
docker exec -it _container id_ ./init.sh
```

### Deploying Updates
1. Pull the updates from GitHub
2. Rebuild the docker container
```
docker-compose -f ../docker-compose.yml -f ../docker-compose-web.yml build
```

3. Restart the docker container
```
docker-compose -f ../docker-compose.yml -f ../docker-compose-web.yml up
```


### Creating the database
The database is running using Postgresql.
1. Install postgresql
2. Start postgresql server [Docs](https://www.postgresql.org/docs/8.1/postmaster-start.html)
    pg_ctl -D /usr/local/var/postgres start (for mac)
3. Start psql shell
    psql postgres
4. Build database and users
   CREATE USER user_name WITH PASSWORD 'password';
   CREATE DATABASE database_name OWNER user_name;


### Setting up Django

1. Clone the repository
2. Create the conda envrionment:
    conda env create environment.yml
3. Make a copy of the cbeImageDB/.env.sample named .env to store your local environment variables

### Getting the organisms
1. Download the [ncbi taxonomy owl file](http://www.obofoundry.org/ontology/ncbitaxon.html)
2. Inside the organisms folder run the following script:
    python parse_ncbi.py ncbi\_owl\_file\_name
This will output the organisms into a file caled 'organisms.txt'.
This script may take a few minutes. Some organisms are removed
from the original taxonomy and saved in a file called 'bad-organims.txt'.
It is important to not move the 'organisms.txt' file, because the
database intilization portion is looking for the file in its
current location.


### Initializing the database with data
1. To populate the database with testing data run the following
management command:
    python manage.py populatetesting
2. To populate with actual data run
1. To populate the database with information run:
    python manage.py initializedatabase
If you do not want to initialize the organisms add `--noorganisms` flag
to the end of the command. **Initializing the organisms will
take awhile.** The first time I ran it, it took three days.
If you do not need to add all the organisms, either add
organisms using the shell or run the adding organisms to add
some organisms, then hit ^C to stop the program.
