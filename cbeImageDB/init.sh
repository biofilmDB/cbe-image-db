#!/bin/bash

# Will run all commands needed to start up database
# Make STATIC_ROOT directory
STATIC_ROOT=$(grep STATIC_ROOT .env | xargs)
IFS='=' read -ra STATIC_ROOT <<< "$STATIC_ROOT"
STATIC_ROOT=${STATIC_ROOT[1]}

echo "Making STATIC_ROOT directory: $STATIC_ROOT"
mkdir $STATIC_ROOT

manage=manage.py
echo "***** Collecting static files in STATIC_ROOT *****"
python $manage collectstatic

##### Commenting out organism stuff, because of RAM issues in docker #####
echo -e "\n***** organisms.txt needs to have already been copied over"
# Download ncbi taxonomy from PURL link on page:
# http://www.obofoundry.org/ontology/ncbitaxon.html
#echo -e "\n***** Downloading NCBI taxonomy *****"
#curl -L http://purl.obolibrary.org/obo/ncbitaxon.owl > organisms/ncbitaxon.owl
#
## Make organism file
#echo -e "\n***** Creating organism files *****"
#python organisms/parse_ncbi.py organisms/ncbitaxon.owl
#rm organisms/bad-organisms.csv

# Make the migrations
echo -e "\n***** Migrating *****"
python $manage migrate

# Initialize the database
echo -e "\n***** Initialize the database *****"
echo "      Assuming files already copied to docker "
python $manage initdb
