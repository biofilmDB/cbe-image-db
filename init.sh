#!/bin/bash

# Will run all commands needed to start up database
# Make STATIC_ROOT directory
STATIC_ROOT=$(grep STATIC_ROOT cbeImageDB/.env | xargs)
IFS='=' read -ra STATIC_ROOT <<< "$STATIC_ROOT"
STATIC_ROOT=${STATIC_ROOT[1]}

echo "Making STATIC_ROOT directory: $STATIC_ROOT"
mkdir $STATIC_ROOT

manage=cbeImageDB/manage.py
python $manage collectstatic
