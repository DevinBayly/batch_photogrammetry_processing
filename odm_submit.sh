#!/bin/bash
echo received "$1" and "$2" for command, original folder $3
rsync -azP "$1/../images" /tmp/$2
ls $2
# the -1 for memory swap means limitless swap space for xontainer, hopefully this means if the process needed more memory it will just slow down instead of crashing
singularity exec --writable odm python3 /code/run.py --feature-quality high --project-path "/tmp" $2 &
# this makes sure we don't lose progress if things don't finish
watch -n 1800 rsync -azP /tmp/$2 "$1/../results"

