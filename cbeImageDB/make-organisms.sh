#!/bin/bash

# Download ncbi taxonomy from PURL link on page:
# http://www.obofoundry.org/ontology/ncbitaxon.html
echo -e "\n***** Downloading NCBI taxonomy *****"
curl -L http://purl.obolibrary.org/obo/ncbitaxon.owl > organisms/ncbitaxon.owl

# Make organism file
echo -e "\n***** Creating organism files *****"
python organisms/parse_ncbi.py organisms/ncbitaxon.owl
