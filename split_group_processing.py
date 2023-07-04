#!/usr/bin/python3
from pathlib import Path
import json
import subprocess as sp
import uuid

# open the split_groups.json
groups = json.loads(Path("../split_groups.json").read_text())

# iterate over the groups, and pass the key to the sbatch process kicked off
# it will then do the ln linking
# for example
for uid_key in groups:
    cmd = f'sbatch -A cdh -p standard -t 12:00:00 -N 1 -n 8 process_group.sh {uid_key}'
    print(cmd)
    # we must capture the output in order to connect up which sbatch job ids are associated with which uids in the tmp folder
    p = sp.run(cmd,shell=True)
