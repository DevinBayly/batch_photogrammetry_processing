#!/bin/bash
echo "received uid key $1 $2"
python3 odm_submit.py $1 $2
# if we make it to here then we are cherry picking files
cd ../tmp/$1
# this seems to take up most of the space
rm -rf opensfm

