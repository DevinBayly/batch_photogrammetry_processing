#!/usr/bin/python3
from pathlib import Path
import json
import subprocess as sp
import uuid

# open the split_groups.json
groups = json.loads(Path("../split_groups_missing.json").read_text())

# iterate over the groups, and pass the key to the sbatch process kicked off
# it will then do the ln linking
# for example
total = len(groups.keys())
will_process =0
# quick hack to make the processing re-run a single step
groups = [folder.name for folder in sorted(Path("../tmp_group_split").iterdir())]
for uid_key in groups:
# check the status of last run by looking for the status file
# only submit if either status is missing, or doesn't show odm_processed complete
  
  pth = Path(f"../tmp_group_split/{uid_key}/status.json")
  should_run = True
  if pth.exists():
    status = json.loads(pth.read_text())
    model_path = Path(f"../tmp_group_split/{uid_key}/odm_texturing/odm_textured_model_geo.obj")
    if status.get("odm_processed",-1) ==-1 and not model_path.exists():
      should_run = True
  else:
    should_run = True

  if should_run: 
    will_process +=1
    cmd = f'sbatch -A cdh -p standard -t 12:00:00 --output slurm_outs/%j.out -N 1 -n 16 process_group.sh {uid_key}'
    print(cmd)
    p = sp.run(cmd,shell=True)

print(f"out of a total {total} groups, will process remaining {will_process}")
