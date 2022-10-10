#!/bin/bash

REPO_URL=https://github.com/JEMHcorpus/corpora.git
N_SUBMODULES_FOUND=$(cat .gitmodules | grep -c 'JEMHcorpus')

if [ $N_SUBMODULES_FOUND == 1 ];
then
    echo 'JEMH already added as submodule'
else
    echo 'JEMH not found as submodule. Adding now...'
    git submodule add --force $REPO_URL
fi

# update submodules recursively
git submodule update --recursive