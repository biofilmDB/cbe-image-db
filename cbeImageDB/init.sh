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

# Download ncbi taxonomy from PURL link on page:
# http://www.obofoundry.org/ontology/ncbitaxon.html
# TODO: If this fails, abort rest of script and give error message
echo -e "\n***** Downloading NCBI taxonomy *****"
curl -L http://purl.obolibrary.org/obo/ncbitaxon.owl > organisms/ncbitaxon.owl

# Make organism file
echo -e "\n***** Creating organism files *****"
python organisms/parse_ncbi.py organisms/ncbitaxon.owl
