#!/usr/bin/env bash

function checkCommandExists() {
  if ! `which $1 > /dev/null` ; then
    echo "Could not find command '$1'. Exiting"
    exit 1
  fi
}

checkCommandExists wget
checkCommandExists bzip2

url="https://www.fuzzwork.co.uk/dump/latest/"

files=(
  industryActivityMaterials.csv
  industryActivityProducts.csv
  invTypes.csv
  invVolumes.csv
)

# create the storage directory and change into it
mkdir -p static_db
pushd static_db

# download files
for file in ${files[@]}; do
  wget ${url}${file}.bz2
done

# uncompress files
bzip2 -d *.bz2

echo Done.
