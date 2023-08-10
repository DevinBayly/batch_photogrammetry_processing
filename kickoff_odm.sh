#!/bin/bash
# navigate to the target folder in tmp
uid_key=$1
pushd ../tmp_group_split/$uid_key
ls
#echo 'date+time rss_mem(KB)' > mem_${SLURM_JOB_ID}.out
#watch -n 30 'ps -U ${USER} --no-headers  -o rss | paste -sd+ | bc | xargs -I {} echo "$(date +%D+%T)" {} | tee -a mem_${SLURM_JOB_ID}.out' &> mem_${SLURM_JOB_ID}.err &
popd
## we are now back in the hpc_processing folder
singularity exec -B /tmp:/opt/dataset odm_latest.sif python3 /code/run.py --max-concurrency $SLURM_NTASKS --feature-quality medium --dtm --dsm --rerun odm_dem --project-path "/opt/dataset" $uid_key
## try to remove the opensfm folder that takes up so much space
rm -rf $uid_key/opensfm
rclone copy  /tmp/$uid_key ../tmp_group_split/$uid_key -L --exclude=/opensfm/** --progress --multi-thread-streams=$SLURM_NTASKS
