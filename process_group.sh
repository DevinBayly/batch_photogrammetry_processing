#!/bin/bash
uid_key=$1

## TODO use the $SLURM_JOB_ID to strt a dependent task that comes and cleans up the opensfm file
#sbatch -A cdh -t 00:20:00 -n 1 -N 1 --dependency=afterany:$SLURM_JOB_ID clean_up.sh $uid_key

echo skipping symlinking for re-run
#python3 sym_link_group.py $uid_key
python3 rclone_group.py $uid_key
# now navigate to that folder and start the processing
python3 odm_group.py $uid_key
