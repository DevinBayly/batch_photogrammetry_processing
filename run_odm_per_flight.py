#!/usr/bin/python3
from pathlib import Path
import json
import subprocess as sp
import uuid

flights = [Path(flight) for flight in open("staged_flights.txt").read().split("\n")]
pairings = {str(uuid.uuid4()):str(flight) for flight in flights}
print(pairings)
pairings_path = f"pairings_{uuid.uuid4()}.json"
open(pairings_path,"w").write(json.dumps(pairings))
running_tasks = []
for uid_key in pairings:
    cmd = f'sbatch -A cdh -p standard -t 24:00:00 -N 1 -n 16 odm_submit.sh {uid_key} {pairings_path}'
    print(cmd)
    # we must capture the output in order to connect up which sbatch job ids are associated with which uids in the tmp folder
    p = sp.run(cmd,shell=True,capture_output=True)
    jid = p.stdout.decode("utf-8").split(" ")[-1]
    running_tasks.append([jid,uid_key])
    

# at this point pause for a moment and then export a collection of the pids associated with this job
running_path = f"running_jobs_{uuid.uuid4()}.json"
open(running_path,"w").write(json.dumps(running_tasks))

open("staged_flights.txt","w").write("")
