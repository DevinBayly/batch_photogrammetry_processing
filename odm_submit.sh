#!/bin/bash
echo received "$1" and "$2" for command, original folder $3
echo "starting up"
#rsync -azP "$1/../images" ../tmp/$2
ls $2
# the -1 for memory swap means limitless swap space for xontainer, hopefully this means if the process needed more memory it will just slow down instead of crashing
singularity exec -B ../tmp:/opt/dataset odm_latest.sif python3 /code/run.py --feature-quality medium --project-path "/opt/dataset" $2
## this makes sure we don't lose progress if things don't finish
#watch -n 1800 rsync -azP /tmp/$2 "$1/../results"

