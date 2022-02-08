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
1. Click the following button to begin Heroku deployment process. This will 
deploy the app as it exists currently. If not currently logged in, you will
first be prompted to log into Heroku.


[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/biofilmDB/cbe-image-db/tree/heroku-deployment)


2. Enter a name for your app. Heroku will tell you if the name is taken or not.
3. Fill in or modify the configure variables.
4. For WEB\_ALLOWED\_HOSTS enter your app name followed by ".herokuapp.com".
All you should have to do is replace the "\_\_\_" in the existing variable name.
5. Click "Deploy App" and Heroku will deploy your app for you. Once finished
you can launch it or manage the settings.
![Successful Deployment](/readme-img/completed-setup.png)


### Create an Admin
6. Click on "Manage App". You will be taken to your app's dashboard.
7. Under "More" on the top right, select "Run Console".
![Run Console](/readme-img/select-command.png)
8. You will be prompted to run a command. You want to type in "bash".
![Bash Command](/readme-img/run-bash.png)


A console window will appear. You are now able to run commands inside a
Heroku Dyno.
![Console loaded](/readme-img/console.png)
10. Run the command:
```
python manage.py createsuperuser
```
11. Follow the prompts on screen to create a superuser. You will be informed
of any errors that occur.
![Superuser Created](/readme-img/created-superuser.png)
12. Log into the websites admin page by adding "/admin" to the end of your
website URL.


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
