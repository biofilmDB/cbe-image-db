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

# Make the migrations
echo -e "\n***** Migrating *****"
python $manage migrate

# Initialize the database
echo -e "\n***** Initialize the database *****"
echo "      Assuming files already copied to docker "
python $manage initdb
